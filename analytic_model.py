from math import factorial
import pandas as pd
from config import PERIODS, CATEGORIES, HOURS_PER_DAY, STEPS, WAGE, QUEUE_LIMIT

LAMBDA = sum((end - start) * lam for start, end, lam in PERIODS) / HOURS_PER_DAY
MU = 1 / sum(probability * meanTime for name, probability, cost, meanTime in CATEGORIES)
MEAN_COST = sum(probability * cost for name, probability, cost, meanTime in CATEGORIES)


def calculate_load(c, lam=LAMBDA, mu=MU):
    r = lam / mu
    rho = r / c
    return r, rho


def calculate_q0(c, m, r, rho):
    a = (r ** c) / factorial(c)
    sum_channels = sum((r ** k) / factorial(k) for k in range(c))
    
    if rho != 1:
        sum_queue = a * ((1 - rho ** (m + 1)) / (1 - rho))
    else:
        sum_queue = a * (m + 1)
        
    q0 = 1 / (sum_channels + sum_queue)
    return q0


def calculate_probabilities(c, m, r, rho, q0):
    a = (r ** c) / factorial(c)
    
    if rho != 1:
        pQueue = a * ((1 - rho ** m) / (1 - rho)) * q0
    else:
        pQueue = a * m * q0

    pRefusal = a * (rho ** m) * q0
    
    Q = 1 - pRefusal
    return pQueue, pRefusal, Q


def calculate_queue_and_time(c, m, r, rho, q0, lam, mu, Q):
    a = (r ** c) / factorial(c)
    
    if rho != 1:
        lq = a * rho * (1 - rho ** m - m * (rho ** m) * (1 - rho)) / ((1 - rho) ** 2) * q0
    else:
        lq = a * m * (m + 1) / 2 * q0
        
    A = lam * Q
    nBusy = A / mu
    ls = lq + nBusy
    
    return {
        "lq": lq,
        "ls": ls,
        "nBusy": nBusy,
        "kBusy": nBusy / c,
        "Wq": lq / lam if lam > 0 else 0,
        "Ws": ls / lam if lam > 0 else 0
    }


def calculate_economics(A, c):
    wage_week = (WAGE / HOURS_PER_DAY) * HOURS_PER_DAY * 5 * c 
    revenue = STEPS * A * MEAN_COST
    profit = revenue - wage_week
    return revenue, profit

def analyticModel(c, lam=LAMBDA, mu=MU, m=QUEUE_LIMIT):
    r, rho = calculate_load(c, lam, mu)
    q0 = calculate_q0(c, m, r, rho)
    pQueue, pRefusal, Q = calculate_probabilities(c, m, r, rho, q0)
    
    metrics = calculate_queue_and_time(c, m, r, rho, q0, lam, mu, Q)
    _, profit = calculate_economics(metrics["nBusy"] * mu, c)
    
    return {
        "masters": c,
        "q0": q0,
        "pQueue": pQueue,
        "pRefusal": pRefusal,
        "Q": Q,
        "A": metrics["nBusy"] * mu,
        "nBusy": metrics["nBusy"],
        "nFree": c - metrics["nBusy"],
        "kBusy": metrics["kBusy"],
        "Lq": metrics["lq"],
        "Ls": metrics["ls"],
        "Wq": metrics["Wq"],
        "Ws": metrics["Ws"],
        "profit": profit
    }


if __name__ == "__main__":
    pd.set_option("display.width", 200)
    print(f"lambda = {LAMBDA:.4f} кл/год, mu = {MU:.4f} рем/год, середня вартість = {MEAN_COST:.0f} грн")
    
    table = pd.DataFrame([analyticModel(c) for c in range(1, 7)])
    print(table.round(4).to_string(index=False))