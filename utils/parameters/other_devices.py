from datetime import datetime


def get_other_devices_consumption(datetime: datetime, holiday: bool = False) -> float:
    hour = datetime.hour
    if holiday:
        return 0.5
    elif datetime.isoweekday() <= 5:
        if hour < 5:
            return 0.5
        elif hour < 8:
            return 3
        elif hour < 10:
            return 2
        elif hour < 16:
            return 1
        elif hour < 20:
            return 2
        else:
            return 1
    else:
        if hour < 8:
            return 0.5
        elif hour < 12:
            return 3
        elif hour < 17:
            return 1
        else:
            return 2
