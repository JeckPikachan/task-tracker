DAY = 24 * 60 * 60
WEEK = DAY * 7
MONTH = 30.4375 * DAY
YEAR = 365.25 * DAY

deltas = {0: DAY, 1: WEEK, 2: MONTH, 3: YEAR}


def get_time_from_delta(delta):
    return deltas.get(delta)