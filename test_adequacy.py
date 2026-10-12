import numpy as np
import pandas as pd
from config import PERIODS, CATEGORIES, STEPS, DAYS, WAGE, QUEUE_LIMIT
from simulation import runExperiments

N = 100
C_LIST = [1, 2, 3]
ZERO_FLOW = [(start, end, 0) for start, end, lam in PERIODS]
HEAVY_FLOW = [(start, end, lam * 10) for start, end, lam in PERIODS]
EXPENSIVE = [(name, probability, cost * 1000, meanTime) for name, probability, cost, meanTime in CATEGORIES]
COUNTS = ["clients", "served", "lost", "unfinished"]
STAGE1 = {"clients": 55.45, "served": 30.16, "lost": 19.74, "revenue": 46374, "lostProfit": 30767}

def checkBalance(r):
    assert (r.clients == r.served + r.lost + r.unfinished).all()


def test_sameAsStage1():
    r, logs = runExperiments(N, masters=1)

    for key, value in STAGE1.items():
        assert round(r[key].mean(), 2) == value


def test_zeroFlow():
    for c in C_LIST:
        r, logs = runExperiments(N, periods=ZERO_FLOW, masters=c)

        assert (r[COUNTS + ["revenue", "lostProfit", "busyTime"]] == 0).all().all()
        assert np.allclose(r.profit, -DAYS * WAGE * c)


def test_expensiveRepair():
    for c in C_LIST:
        base, logs = runExperiments(N, masters=c)
        r, logs = runExperiments(N, categories=EXPENSIVE, masters=c)
        assert (r[COUNTS] == base[COUNTS]).all().all()

        assert np.allclose(r.revenue, base.revenue * 1000)
        assert np.allclose(r.lostProfit, base.lostProfit * 1000)
        assert np.allclose(r.profit, r.revenue - r.wages)

        checkBalance(r)


def test_heavyFlow():
    for c in C_LIST:
        r, logs = runExperiments(N, periods=HEAVY_FLOW, masters=c)
        utilization = r.busyTime / (STEPS * c)

        assert (utilization.round(6) <= 1).all()
        assert utilization.mean() > 0.99
        assert r.lossRate.mean() > 0.8
        assert logs.queue.max() <= QUEUE_LIMIT

        checkBalance(r)


def test_manyMasters():
    r, logs = runExperiments(N, masters=20)

    assert (r.lost == 0).all()
    checkBalance(r)


def test_moreMasters():
    prev = None

    for c in range(1, 7):
        r, logs = runExperiments(N, masters=c)
        assert (logs.groupby("run").size() == STEPS).all()

        if prev is not None:
            assert (r.clients == prev.clients).all()
            assert r.lost.mean() <= prev.lost.mean()
            assert r.wages.mean() > prev.wages.mean()

        prev = r


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

    for c in C_LIST:
        for name, params in scenarios:
            r, logs = runExperiments(N, masters=c, **params)
            r["utilization"] = r.busyTime / (STEPS * c)
            table.append(r[columns].mean().rename(f"{name}, c={c}"))

    print(f"Середні значення за {N} прогонів")
    print(pd.DataFrame(table).round(3).to_string())

    test_sameAsStage1()
    test_zeroFlow()
    test_expensiveRepair()
    test_heavyFlow()
    test_manyMasters()
    test_moreMasters()

    print("Усі перевірки пройдено")