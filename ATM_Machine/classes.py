import contextlib
import json

from pathlib import Path
from typing import Dict, Tuple, Union

from ATM_Machine.errors import AccountNotFoundError, AccountAlreadyExistsError


ATM_DATA_PATH = Path(__file__).parent / "atm_data.json"


class ATMCard:
    def __init__(self, holder_name: str):
        self.holder_name = holder_name


class ATMMachine:
    def __init__(self):
        self.atm_data = self.get_data()

    @staticmethod
    def get_data() -> Dict[str, Dict[str, Union[str, int]]]:
        with contextlib.suppress(json.JSONDecodeError, FileNotFoundError):
            with open(ATM_DATA_PATH, "r") as atm_data_file:
                return json.loads(atm_data_file.read())
        return {}

    def write_data(self) -> None:
        with open(ATM_DATA_PATH, "w") as atm_data_file:
            atm_data_file.write(json.dumps(self.atm_data))

    def create_account(self) -> Tuple[Union[str, int]]:
        print("Welcome to ATM Machine account creation!")
        name = input("Enter the name for your account: ")

        if name in self.atm_data:
            raise AccountAlreadyExistsError(f"It seems the name {name!r} is already registered please open an account instead.")

        address = input("Enter your full address: ")
        acc_pin = []
        init_dep = []
        while True:
            try:
                pin = int(input("Enter your 4 PIN for this account: "))
            except ValueError:
                print("Invalid input please try again.")
                continue
            else:
                acc_pin.append(pin)
                break
        while True:
            try:
                i_d = int(input("Enter your initial deposit for this account: "))
            except ValueError:
                print("Invalid input please try again.")
                continue
            else:
                init_dep.append(i_d)
                break
        return name, address, acc_pin[0], init_dep[0]

    def open_account(self) -> None:
        print("Welcome to the ATM!")
        name = input("Enter the name of your account: ")

        if name not in self.atm_data:
            raise AccountNotFoundError(f"It seems the name {name!r} is not yet registered please create an account instead.")

    def start(self) -> None:
        print("Welcome to John's Broken but working ATM Machine.")
        while True:
            _type = input(
                "\nChoose an action below.\n\n1. Create an account.\n2. Open an account.\n3. Exit.\n\nInput action number: "
            )

            if _type == "1":
                try:
                    name, address, pin, initial_depost = self.create_account()
                except AccountAlreadyExistsError as aaee:
                    print(str(aaee))
                    continue

                self.atm_data[name] = {
                    "address": address,
                    "pin": pin,
                    "balance": initial_depost,
                }
                print(
                    f"Thank you for creating an account {name}! Be sure to remember your details."
                )
                continue
            elif _type == "2":
                try:
                    self.open_account()
                except AccountNotFoundError as anfe:
                    print(str(anfe))
                    continue
            elif _type == "3":
                print("Thank you for using the ATM Machine!")
                break
            else:
                print("Invalid input please try again.")
                continue
