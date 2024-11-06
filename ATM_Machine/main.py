from classes import ATMMachine
from errors import ExitedError

if __name__ == "__main__":
    try:
        atm_machine = ATMMachine()
        atm_machine.start()
    except ExitedError as EE:
        print(str(EE))
