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


def track_points(time, parameters):
    """Part 2"""
    import math
    if len(parameters) == 3:
        if time_to_seconds(time) > parameters[1]:
            return 0
        return math.floor(parameters[0] * math.pow((parameters[1] - time_to_seconds(time)), parameters[2]))
    else:
        raise ValueError("Wrong format for the parameters.")


def compute_score(record):
    """Part 3"""
    POINT_PARAMETERS = {"200m": (4.99087, 42.5, 1.81),
                        "800m": (0.11193, 254.0, 1.88),
                        "110m": (9.23076, 26.7, 1.835)}

    items = record.strip().split(',')
    if len(items) != 4:
        raise ValueError('Invalid number of entries.')

    points_200 = track_points(items[1].strip(), POINT_PARAMETERS['200m'])
    points_110 = track_points(items[2].strip(), POINT_PARAMETERS['110m'])
    points_800 = track_points(items[3].strip(), POINT_PARAMETERS['800m'])

    return (items[0].strip(), points_200, points_110, points_800, points_200 + points_110 + points_800)