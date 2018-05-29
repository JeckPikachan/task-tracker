DAY = 24 * 60 * 60
WEEK = DAY * 7
MONTH = 30.4375 * DAY
YEAR = 365.25 * DAY

deltas = {0: DAY, 1: WEEK, 2: MONTH, 3: YEAR}
deltas_reversed = {DAY: 0, WEEK: 1, MONTH: 2, YEAR: 3}


def get_time_from_delta(delta):
    return deltas.get(delta)


def get_delta_from_time(timestamp):
    return deltas_reversed.get(timestamp)
