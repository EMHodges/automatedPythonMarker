import re


def time_to_seconds(time):
    """Part 1"""
    time_split = time.split(':')

    if len(time_split) == 2:
        seconds_split = time_split[1].strip().split('.')
        if (len(time_split[0]) == 2
                and len(seconds_split) == 2
                and len(seconds_split[0]) == 2
                and len(seconds_split[1]) == 3
                and 0 <= float(time_split[1]) < 60):
            return float(time_split[0]) * 60.0 + float(time_split[1])
        else:
            raise ValueError("Invalide time format...")

    elif len(time_split) == 1:
        seconds_split = time_split[0].strip().split('.')
        if (len(seconds_split) == 2
                and len(seconds_split[0]) == 2
                and len(seconds_split[1]) == 3
                and 0 <= float(time_split[0]) < 60):
            return float(time_split[0])
        else:
            raise ValueError("Invalide time format...")
    else:
        raise ValueError("Invalide time format...")


def track_points(time, event_parameters):
   timeSeconds = time_to_seconds(time)
   points = round(event_parameters[0] * ((event_parameters[1] - timeSeconds))**event_parameters[2])
   if points < 0:
       points = 0
   return points

if __name__ == "__main__":
    print(track_points('13.480', (9.23076, 26.7, 1.835)))