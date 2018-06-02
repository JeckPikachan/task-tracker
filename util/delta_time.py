DAILY = 0
WEEKLY = 1
MONTHLY = 2
YEARLY = 3

DAY = 24 * 60 * 60
WEEK = DAY * 7
MONTH = 30.4375 * DAY
YEAR = 365.25 * DAY

deltas = {DAILY: DAY, WEEKLY: WEEK, MONTHLY: MONTH, YEARLY: YEAR}
deltas_inverted = {DAY: DAILY, WEEK: WEEKLY, MONTH: MONTHLY, YEAR: YEARLY}


def get_time_from_delta(delta):
    return deltas.get(delta)
