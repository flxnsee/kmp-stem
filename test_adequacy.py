import numpy as np
import pandas as pd
from config import PERIODS, CATEGORIES, STEPS, MASTERS
from simulation import runExperiments

N = 100
ZERO_FLOW = [(start, end, 0) for start, end, lam in PERIODS]
HEAVY_FLOW = [(start, end, lam * 10) for start, end, lam in PERIODS]
EXPENSIVE = [(name, probability, cost * 1000, meanTime) for name, probability, cost, meanTime in CATEGORIES]
COUNTS = ["clients", "served", "lost", "unfinished"]

def checkBalance(r):
    assert (r.clients == r.served + r.lost + r.unfinished).all()


def test_zeroFlow():
    r, logs = runExperiments(N, periods=ZERO_FLOW)

    assert (r[COUNTS + ["revenue", "lostProfit", "busyTime"]] == 0).all().all()
    assert (r.profit == -r.wages).all()


def test_expensiveRepair():
    base, logs = runExperiments(N)
    r, logs = runExperiments(N, categories=EXPENSIVE)
    assert (r[COUNTS] == base[COUNTS]).all().all()

    assert np.allclose(r.revenue, base.revenue * 1000)
    assert np.allclose(r.lostProfit, base.lostProfit * 1000)
    assert np.allclose(r.profit, r.revenue - r.wages)

    checkBalance(r)


def test_heavyFlow():
    r, logs = runExperiments(N, periods=HEAVY_FLOW)

    assert (r.busyTime.round(6) <= STEPS * MASTERS).all()
    assert r.utilization.mean() > 0.99
    assert r.lossRate.mean() > 0.8

    checkBalance(r)


if __name__ == "__main__":
    pd.set_option("display.width", 200)
    scenarios = [
        ("базовий", {}),
        ("нульовий потік", {"periods": ZERO_FLOW}),
        ("вартість x1000", {"categories": EXPENSIVE}),
        ("потік x10", {"periods": HEAVY_FLOW}),
    ]
    columns = ["clients", "served", "lost", "lossRate", "revenue", "lostProfit", "wages", "profit", "utilization", "avgQueue"]
    table = []

    for name, params in scenarios:
        r, logs = runExperiments(N, **params)
        table.append(r[columns].mean().rename(name))

    print(f"Середні значення за {N} прогонів")
    print(pd.DataFrame(table).round(3).to_string())

    test_zeroFlow()
    test_expensiveRepair()
    test_heavyFlow()

    print("Усі перевірки пройдено")