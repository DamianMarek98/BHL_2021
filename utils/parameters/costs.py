from datetime import datetime


def get_energy_cost(datetime: datetime, income: bool = False) -> float:
    month = datetime.month
    hour = datetime.hour
    if month in [1, 2, 3, 10, 11, 12]:
        if datetime.isoweekday() <= 5:
            if hour < 6:
                return 1 if income else 0.5
            elif hour < 13:
                return 2.5 if income else 2
            elif hour < 15:
                return 1
            elif hour < 22:
                return 2.5 if income else 2
            else:
                return 0.5 if income else 1
        else:
            return 0.5 if income else 1
    else:
        if datetime.isoweekday() <= 5:
            if hour < 6:
                return 0.5 if income else 1
            elif hour < 15:
                return 2.5 if income else 2
            elif hour < 17:
                return 1
            elif hour < 22:
                return 2.5 if income else 2
            else:
                return 0.5 if income else 1
        else:
            if hour < 12:
                return 0.5 if income else 1
            elif hour < 15:
                return 0.25 if income else 0.5
            else:
                return 0.5 if income else 1
