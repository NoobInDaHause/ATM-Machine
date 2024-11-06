import contextlib
import json

from pathlib import Path
from typing import Dict, Tuple, Union

from errors import AccountNotFoundError, AccountAlreadyExistsError, ExitedError


class ATMMachine:
    def __init__(self) -> None:
        self.atm_data = self.get_data()

    @staticmethod
    def get_data() -> Dict[str, Dict[str, Union[str, int]]]:
        with contextlib.suppress(json.JSONDecodeError, FileNotFoundError):
            with open(Path(__file__).parent / "atm_data.json", "r") as atm_data_file:
                return json.loads(atm_data_file.read())
        return {}

    def write_data(self) -> None:
        with open(Path(__file__).parent / "atm_data.json", "w") as atm_data_file:
            atm_data_file.write(json.dumps(self.atm_data.copy()))

    def create_account(self) -> None:
        print("Welcome to ATM Machine account creation!")
        name = input("Enter the name for your account: ")

        if name.lower() == "exit":
            raise ExitedError("Thank you for using John's broken but Working ATM Machine!")

        if name in self.atm_data:
            raise AccountAlreadyExistsError(f"It seems the name {name!r} is already registered please open an account instead.")

        address = input("Enter your full address: ")
        if address.lower() == "exit":
            raise ExitedError("Thank you for using John's broken but Working ATM Machine!")
        acc_pin = []
        init_dep = []
        while True:
            try:
                _pin = input("Enter your 4 PIN for this account: ")
                if _pin.lower() == "exit":
                    raise ExitedError("Thank you for using John's broken but Working ATM Machine!")
                pin = int(_pin)
            except ValueError:
                print("Invalid input please try again.")
                continue
            else:
                acc_pin.append(pin)
                break
        while True:
            try:
                _i_d = input("Enter your initial deposit for this account: ")
                if name.lower() == "exit":
                    raise ExitedError("Thank you for using John's broken but Working ATM Machine!")
                i_d = int(_i_d)
            except ValueError:
                print("Invalid input please try again.")
                continue
            else:
                init_dep.append(i_d)
                break

        self.atm_data[name] = {
            "address": address,
            "pin": acc_pin[0],
            "balance": init_dep[0],
        }
        self.write_data()

        print(f"Thank you for creating an account {name}! Be sure to remember your details.")

    def open_account(self) -> None:
        print("Welcome to the ATM!")
        name = input("Enter the name of your account: ")

        if name.lower() == "exit":
            raise ExitedError("Thank you for using John's broken but Working ATM Machine!")
        if name not in self.atm_data:
            raise AccountNotFoundError(f"It seems the name {name!r} is not yet registered please create an account instead.")

    def start(self) -> None:
        print("Welcome to John's broken but working ATM Machine.")
        while True:
            try:
                _type = input(
                    "\nChoose an action below. (input 'exit' anytime to exit the ATM Machine.)\n\n1. Create an account.\n2. Open an account."
                    "\n\nInput action number: "
                )

                if _type == "1":
                    try:
                        self.create_account()
                    except AccountAlreadyExistsError as aaee:
                        print(str(aaee))
                    continue
                elif _type == "2":
                    try:
                        self.open_account()
                    except AccountNotFoundError as anfe:
                        print(str(anfe))
                        continue
                elif _type.lower() == "exit":
                    raise ExitedError("Thank you for using John's broken but Working ATM Machine!")
                else:
                    print("Invalid input please try again.")
                    continue
            except ExitedError as ee:
                print(str(ee))
                break
