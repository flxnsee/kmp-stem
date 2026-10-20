from math import factorial
import pandas as pd
from config import PERIODS, CATEGORIES, HOURS_PER_DAY, STEPS, WAGE, QUEUE_LIMIT

LAMBDA = sum((end - start) * lam for start, end, lam in PERIODS) / HOURS_PER_DAY
MU = 1 / sum(probability * meanTime for name, probability, cost, meanTime in CATEGORIES)
MEAN_COST = sum(probability * cost for name, probability, cost, meanTime in CATEGORIES)

def analyticModel(c, lam=LAMBDA, mu=MU, m=QUEUE_LIMIT):
    r = lam / mu
    rho = r / c
    a = r ** c / factorial(c)

    if rho != 1:
        q0 = 1 / (sum(r ** k / factorial(k) for k in range(c)) + a * (1 - rho ** (m + 1)) / (1 - rho))
        pQueue = a * (1 - rho ** m) / (1 - rho) * q0
        lq = a * rho * (1 - rho ** m - m * rho ** m * (1 - rho)) / (1 - rho) ** 2 * q0
    else:
        q0 = 1 / (sum(r ** k / factorial(k) for k in range(c)) + a * (m + 1))
        pQueue = a * m * q0
        lq = a * m * (m + 1) / 2 * q0

    pRefusal = a * rho ** m * q0
    Q = 1 - pRefusal
    A = lam * Q
    nBusy = A / mu
    ls = lq + nBusy

    return {
        "masters": c,
        "q0": q0,
        "pQueue": pQueue,
        "pRefusal": pRefusal,
        "Q": Q,
        "A": A,
        "nBusy": nBusy,
        "nFree": c - nBusy,
        "kBusy": nBusy / c,
        "Lq": lq,
        "Ls": ls,
        "Wq": lq / lam,
        "Ws": ls / lam,
        "profit": (MEAN_COST * A - WAGE / HOURS_PER_DAY * c) * STEPS
    }


if __name__ == "__main__":
    pd.set_option("display.width", 200)
    print(f"lambda = {LAMBDA:.4f} клієнта/год, mu = {MU:.4f} ремонту/год, r = {LAMBDA / MU:.4f}, середня вартість = {MEAN_COST:.0f} грн")

    table = pd.DataFrame([analyticModel(c) for c in range(1, 7)])
    print(table.round(4).to_string(index=False))