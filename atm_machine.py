import contextlib
import json

from pathlib import Path
from typing import Dict, Tuple, Union

from .errors import AccountNotFoundError

PINS_PATH = Path(__file__).parent / "atm_data.json"

class ATMCard:
    def __init__(self):
        pass

class ATMMachine:
    def __init__(self) -> None:
        self.atm_data = self.get_atm_data()

    @staticmethod
    def get_atm_data() -> Dict[str, Dict[str, Union[str, int]]]:
        with contextlib.suppress(json.JSONDecodeError, FileNotFoundError):
            with open(PINS_PATH, "r") as read_pins:
                return json.loads(read_pins.read())
        return {}

    @staticmethod
    def write_atm_data(atm_data: Dict[str, int]) -> None:
        with open(PINS_PATH, "w") as write_pins:
            write_pins.write(json.dumps(atm_data))

    def save_pins(self) -> None:
        self.write_atm_data(self.atm_data.copy())

    def create_account(self) -> Tuple[Union[str, int]]:
        print("Welcome to ATM Machine acount creation!")
        name = input("Enter the name for your account: ")
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
        name = input("Please enter the name of your account: ")

        account_data = self.atm_data.get(name, None)
        if account_data is None:
            raise AccountNotFoundError("It seems this account name does not exist.")

        pini = []
        while True:
            try:
                i_d = int(input(""))
            except ValueError:
                print("Invalid input please try again.")
                continue
            else:
                pini.append(i_d)
                break

        

    def start(self) -> None:
        print("Welcome to the ATM Machine.")
        while True:
            _type = input(
                "\nChoose an action below.\n\n1. Create an account.\n2. Open an account.\n3. Exit.\n\nInput action number: "
            )

            if _type == "1":
                name, address, pin, initial_depost = self.create_account()
                if name in self.atm_data:
                    print(f"It seems the name {name!r} is already registered.")
                    continue
                self.atm_data[name] = {"address": address, "pin": pin, "balance": initial_depost}
                print(f"Thank you for creating an account {name}! Be sure to remember your details.")
                continue
            elif _type == "2":
                self.open_account()
            elif _type == "3":
                print("Thank you for using the ATM Machine!")
                break
            else:
                print("Invalid input please try again.")
                continue
            

if __name__ == "__main__":
    atm_machine = ATMMachine()
    atm_machine.start()
