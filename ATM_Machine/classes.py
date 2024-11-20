import contextlib
import json

from pathlib import Path
from typing import Dict, Union

from errors import (
    AccountNotFoundError,
    AccountAlreadyExistsError,
    AccountBlockedError,
    ExitedError,
)


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
        name = self.get_name(
            "Welcome to ATM Machine account creation!",
            "Enter the name for your account: ",
        )

        if not name:
            return

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
                pinn = int(_pin)
                if len(str(pinn)) < 4 or len(str(pinn)) > 4:
                    print("PIN must be 4 numbers no more no less.")
                    continue
                pin += pinn
                break
            except ValueError:
                print("Invalid input please try again.")
                continue
        while True:
            try:
                _i_d = input("Enter your initial deposit for this account: ")
                if _i_d.lower() == "exit":
                    raise ExitedError(
                        "Thank you for using John's broken but Working ATM Machine!"
                    )
                in_d = int(_i_d)
                if in_d <= 0:
                    print("You can not deposit less than or equal to 0 amount.")
                    continue
                init_dep += in_d
                break
            except ValueError:
                print("Invalid input please try again.")
                continue

        self.atm_data[name] = {
            "pin": pin,
            "balance": init_dep,
            "blocked": False,
            "savings": 0,
        }
        self.write_data()

        print(
            f"Thank you for creating an account {name}! Be sure to remember your details."
        )

    def open_account(self) -> None:
        name = self.get_name("Welcome to the ATM!", "Enter the name of your account: ")

        if not name:
            return

        if not (account := self.atm_data.get(name)):
            raise AccountNotFoundError(
                f"It seems the name {name!r} is not yet registered please create an account instead."
            )
        if account.get("blocked"):
            raise AccountBlockedError(
                "We are sorry but this account is currently blocked. Please contact our customer support."
            )

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
                        account["blocked"] = True
                        self.write_data()
                        return
                    else:
                        print(
                            f"Incorrect PIN you have {tries} more attemps or this account will be blocked."
                        )
                        continue

                while True:
                    print(f"\nWelcome {name}!")
                    a = input(
                        "1. Check Balance.\n2. Withdraw.\n3. Deposit.\n4. Check Savings.\n5. Withdraw Savings.\n6. Deposit Savings.\n\n"
                        "What would you like to do: "
                    )
                    balance = account.get("balance")
                    savings = account.get("savings")
                    if a == "1":
                        print(f"Your current balance is: {balance:,}")
                    elif a == "2":
                        to_withdraw = self.get_withdraw_or_deposit_ammount()

                        if to_withdraw > balance:
                            print(
                                f"You can not withdraw that many since you only have {balance:,} in your account."
                            )
                            continue
                        if to_withdraw <= 0:
                            print("You can not withdraw below or equal to 0 amount.")
                            continue

                        new_balance = balance - to_withdraw
                        account["balance"] = new_balance
                        self.write_data()
                        print(
                            f"You have withdrawn {to_withdraw:,}, your total balance is now {new_balance:,}."
                        )
                    elif a == "3":
                        to_deposit = self.get_withdraw_or_deposit_ammount()

                        if to_deposit <= 0:
                            print("You can not deposit less than or equal to 0 amount.")
                            continue

                        new_balance = balance + to_deposit
                        account["balance"] = new_balance
                        self.write_data()
                        print(
                            f"You have deposited {to_deposit:,}, your total balance is now {new_balance:,}"
                        )
                    elif a == "4":
                        print(f"Your current savings is: {savings:,}")
                    elif a == "5":
                        saving_with = self.get_withdraw_or_deposit_ammount()

                        if saving_with > savings:
                            print(
                                f"You can not withdraw that many savings since you only have a savings balance of {savings:,}"
                            )
                            continue
                        if saving_with <= 0:
                            print(
                                "You can not withdraw less than or equal to 0 amount."
                            )
                            continue

                        new_savings = savings - saving_with
                        account["savings"] = new_savings
                        new_bal = balance + saving_with
                        account["balance"] = new_bal
                        self.write_data()
                        print(
                            f"You have withdrawn {saving_with:,} from your savings to balance.\nCurrent Savings: {new_savings:,}\nCurrent Balance: "
                            f"{new_bal:,}."
                        )
                    elif a == "6":
                        saving_dep = self.get_withdraw_or_deposit_ammount()

                        if saving_dep > balance:
                            print(
                                f"You only have a balance of {balance:,}, you can not deposit that many."
                            )
                            continue
                        if saving_dep <= 0:
                            print("You can not deposit less than or equal to 0 amount.")
                            continue

                        new_savings = savings + saving_dep
                        account["savings"] = new_savings
                        new_bal = balance - saving_dep
                        account["balance"] = new_bal
                        self.write_data()
                        print(
                            f"You have deposited {saving_dep:,} from your savings to balance.\nCurrent Savings: {new_savings:,}\nCurrent Balance: "
                            f"{new_bal:,}."
                        )
                    elif a.lower() == "exit":
                        raise ExitedError(
                            "Thank you for using John's broken but Working ATM Machine!"
                        )
                    else:
                        print("Invalid input please try again.")

            except ValueError:
                print("Invalid input please try again.")

    def get_withdraw_or_deposit_ammount(self) -> int:
        while True:
            try:
                __d = input("Enter the ammount that you want to withdraw: ")
                if __d.lower() == "exit":
                    raise ExitedError(
                        "Thank you for using John's broken but Working ATM Machine!"
                    )
                return int(__d)
            except ValueError:
                print("Invalid input please try again.")

    def get_name(self, arg0: str, arg1: str) -> str:
        print(arg0)
        result = input(arg1)
        if result.lower() == "exit":
            raise ExitedError(
                "Thank you for using John's broken but Working ATM Machine!"
            )
        return result

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
                    print(aaee)
            elif _type == "2":
                try:
                    self.open_account()
                except (AccountNotFoundError, AccountBlockedError) as anfe:
                    print(anfe)
            elif _type.lower() == "exit":
                raise ExitedError(
                    "Thank you for using John's broken but Working ATM Machine!"
                )
            else:
                print("Invalid input please try again.")

            continue
