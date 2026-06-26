import numpy as np

avg = 35


def temperatur_score(avg):
    if avg < 0:
        return 0.0
    elif 0 <= avg < 10:
        return 10 + (avg/10) * 30
    elif 10 <= avg < 20:
        return 40 + ((avg - 10) / 10) * 40
    elif 20 <= avg <= 25:
        return 100.0
    elif 25 < avg <= 35:
        return 80 - ((avg - 25/10))


np.interp(avg, [0, 10, 20, 25, 35], [10, 40, 80, 100, 40])
