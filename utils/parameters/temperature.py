from datetime import datetime
from typing import Optional


default_expected_temperature = {
    "night": 20,
    "day": 23,
    "holiday": 12
}


def get_expected_temperature(datetime: datetime = datetime.now(), holiday: bool = False, expected_temperature: dict = default_expected_temperature) -> int:
    if holiday:
        return expected_temperature["holiday"]
    else:
        if datetime.isoweekday() <= 5:
            if datetime.hour < 5:
                return expected_temperature["night"]
            else:
                return expected_temperature["day"]
        else:
            if datetime.hour < 8:
                return expected_temperature["night"]
            else:
                return expected_temperature["day"]


default_temp_utils = {
    "o20": {
        "hold": 0,
        "increase": None,
        "decrease_time": None
    },
    "15-20": {
        "hold": 0.5,
        "increase": 2,
        "decrease_time": 6
    },
    "5-15": {
        "hold": 1,
        "increase": 4,
        "decrease_time": 4
    },
    "0-5": {
        "hold": 2,
        "increase": 5,
        "decrease_time": 3
    },
    "m5-0": {
        "hold": 3,
        "increase": 6,
        "decrease_time": 2
    },
    "m10-m5": {
        "hold": 5,
        "increase": 7,
        "decrease_time": 1
    },
    "m20-m10": {
        "hold": 7,
        "increase": 10,
        "decrease_time": 0.5
    },
    "bm20": {
        "hold": 9,
        "increase": 12,
        "decrease_time": 0.25
    }
}


def power_to_hold_temperature(temperature: float, parameter: str, temp_utils: dict = default_temp_utils) -> Optional[float]:
    """
    Parameter must be one of
    - hold
    - increase
    - decrease_time
    """

    if parameter not in ["hold", "increase", "decrease_time"]:
        return None
    if temperature >= 20:
        return temp_utils["o20"][parameter]
    elif temperature >= 15:
        return temp_utils["15-20"][parameter]
    elif temperature >= 5:
        return temp_utils["5-15"][parameter]
    elif temperature >= 0:
        return temp_utils["0-5"][parameter]
    elif temperature >= -5:
        return temp_utils["m5-0"][parameter]
    elif temperature >= -10:
        return temp_utils["m10-m5"][parameter]
    elif temperature > -20:
        return temp_utils["m20-m10"][parameter]
    else:
        return temp_utils["bm20"][parameter]


if __name__ == "__main__":

    # Basic tests
    assert get_expected_temperature(holiday=True) == 12
    assert get_expected_temperature(datetime=datetime(2021, 1, 1, 1, 1)) == 20

    assert power_to_hold_temperature(12, "hold") == 1
    assert power_to_hold_temperature(20, "increase") == None
    assert power_to_hold_temperature(13, "asdasd") == None
