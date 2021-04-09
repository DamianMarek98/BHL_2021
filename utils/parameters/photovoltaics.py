from datetime import datetime


def get_photovoltaics_production(datetime: datetime, cloud_percentage: int) -> float:
    month = datetime.month
    hour = datetime.hour
    if month in [1, 12]:
        if cloud_percentage >= 90:
            if hour < 8 or hour >= 15:
                return 0
            elif hour in [8, 9, 14]:
                return 1.5
            else:
                return 3
        if cloud_percentage >= 60:
            if hour < 8 or hour >= 15:
                return 0
            elif hour in [8, 9, 14]:
                return 1
            else:
                return 2
        else:
            if hour < 8 or hour >= 15:
                return 0
            elif hour in [8, 9, 14]:
                return 0.5
            else:
                return 1.5
    elif month in [2, 3, 10, 11]:
        if cloud_percentage >= 90:
            if hour < 7 or hour >= 16:
                return 0
            elif hour in [7, 8, 15]:
                return 2
            else:
                return 4
        if cloud_percentage >= 60:
            if hour < 7 or hour >= 16:
                return 0
            elif hour in [7, 8, 15]:
                return 2
            else:
                return 3
        else:
            if hour < 7 or hour >= 16:
                return 0
            elif hour in [7, 8, 15]:
                return 0.5
            else:
                return 1.5
    elif month in [4, 5, 9]:
        if cloud_percentage >= 90:
            if hour < 6 or hour >= 18:
                return 0
            elif hour in [6, 17]:
                return 3.5
            else:
                return 5
        if cloud_percentage >= 60:
            if hour < 6 or hour >= 18:
                return 0
            elif hour in [6, 17]:
                return 3
            else:
                return 4
        else:
            if hour < 6 or hour >= 18:
                return 0
            elif hour in [6, 17]:
                return 1
            else:
                return 2
    else:
        if cloud_percentage >= 90:
            if hour < 5 or hour >= 20:
                return 0
            elif hour in [5, 6, 19]:
                return 3.5
            else:
                return 5
        if cloud_percentage >= 60:
            if hour < 5 or hour >= 20:
                return 0
            elif hour in [5, 6, 19]:
                return 3
            else:
                return 4
        else:
            if hour < 5 or hour >= 20:
                return 0
            elif hour in [5, 6, 19]:
                return 1
            else:
                return 2
