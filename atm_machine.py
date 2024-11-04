import contextlib
import json

from pathlib import Path
from typing import Dict

PINS_PATH = Path(__file__).parent / "pins_data.json"


def get_pins_data() -> Dict[str, int]:  # {"name": pin}
    with contextlib.suppress(json.JSONDecodeError, FileNotFoundError):
        with open(PINS_PATH, "r") as read_pins:
            return json.loads(read_pins.read())
    return {}


def write_pins_data(pins_data: Dict[str, int]) -> None:
    with open(PINS_PATH, "w") as write_pins:
        write_pins.write(json.dumps(pins_data))


class ATMMachine:
    def __init__(self) -> None:
        self.pins_data = get_pins_data()

    def save_pins(self) -> None:
        write_pins_data(self.pins_data.copy())

    def start(self) -> None:
        print("started")  # temporary code for now
        print(self.pins_data)
        self.pins_data["john"] = 2645
        self.save_pins()


atm_machine = ATMMachine()
atm_machine.start()
