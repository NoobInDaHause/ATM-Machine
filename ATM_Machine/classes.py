import contextlib
import json

from pathlib import Path
from typing import Dict, Union

from errors import AccountNotFoundError, AccountAlreadyExistsError, ExitedError


class ATMCard:
    def __init__(self, card_holder: str, card_number: int) -> None:
        self.card_holder = card_holder
        self.card_number = card_number


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
            raise ExitedError(
                "Thank you for using John's broken but Working ATM Machine!"
            )

        if self.atm_data.get(name):
            raise AccountAlreadyExistsError(
                f"It seems the name {name!r} is already registered please open an account instead."
            )

        pin = 0
        init_dep = 0
        while True:
            try:
                _pin = input("Enter your 4 PIN for this account: ")
                if _pin.lower() == "exit":
                    raise ExitedError(
                        "Thank you for using John's broken but Working ATM Machine!"
                    )
                pin += int(_pin)
                break
            except ValueError:
                print("Invalid input please try again.")
                continue
        while True:
            try:
                _i_d = input("Enter your initial deposit for this account: ")
                if name.lower() == "exit":
                    raise ExitedError(
                        "Thank you for using John's broken but Working ATM Machine!"
                    )
                init_dep += int(_i_d)
                break
            except ValueError:
                print("Invalid input please try again.")
                continue

        self.atm_data[name] = {
            "pin": pin,
            "balance": init_dep,
            "blocked": False
        }
        self.write_data()

        print(
            f"Thank you for creating an account {name}! Be sure to remember your details."
        )

    def open_account(self) -> None:
        print("Welcome to the ATM!")
        name = input("Enter the name of your account: ")

        if name.lower() == "exit":
            raise ExitedError(
                "Thank you for using John's broken but Working ATM Machine!"
            )

        if account := self.atm_data.get(name):
            if account.get("blocked"):
                print("We are sorry but this account is currently blocked. Please contact our customer support.")

            pin = account.get("pin")
            tries = 3
            while True:
                try:
                    _p_n = input("Enter the PIN for this account: ")
                    if _p_n.lower() == "exit":
                        raise ExitedError(
                            "Thank you for using John's broken but Working ATM Machine!"
                        )
                    p_n = int(_p_n)
                    if p_n != pin:
                        tries -= 1
                        if tries <= 0:
                            print("This account is now blocked.")
                            self.atm_data.pop(name, None)
                            return
                        else:
                            print(f"Incorrect PIN you have {tries} more attemps or this account will be blocked.")
                            continue

                    print(f"Welcome {name}!")
                    balance = account.get("balance")
                    

                except ValueError:
                    print("Invalid input please try again.")
                    continue
        else:
            raise AccountNotFoundError(
                f"It seems the name {name!r} is not yet registered please create an account instead."
            )



    def start(self) -> None:
        print("Welcome to John's broken but working ATM Machine.")
        while True:
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
                raise ExitedError(
                    "Thank you for using John's broken but Working ATM Machine!"
                )
            else:
                print("Invalid input please try again.")
                continue
