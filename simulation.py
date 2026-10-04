import numpy as np
import pandas as pd
from config import STEP, START_HOUR, HOURS_PER_DAY, STEPS, PERIODS, CATEGORIES, QUEUE_LIMIT, WAGE, MASTERS
from service_center import ServiceCenter
from random_values import generateClientsCount, generateOrder

def clientArrived(center, order):
    if len(center.queue) < center.queueLimit + center.freeMasters():
        center.queue.append(order)
        return True

    center.loseClient(order)
    return False

def runModel(periods=PERIODS, categories=CATEGORIES, queueLimit=QUEUE_LIMIT, wage=WAGE, seed=None):
    if seed is not None:
        np.random.seed(seed)

    center = ServiceCenter(queueLimit, wage)
    log = []

    for step in range(STEPS):
        day = step // HOURS_PER_DAY + 1
        hour = START_HOUR + step % HOURS_PER_DAY
        arrived = generateClientsCount(hour, periods)
        lost = 0

        for i in range(arrived):
            if not clientArrived(center, generateOrder(step, categories)):
                lost += 1

        servedBefore = center.served
        center.repair(STEP)
        log.append([day, hour, arrived, lost, center.served - servedBefore, len(center.queue)])

    log = pd.DataFrame(log, columns=["day", "hour", "arrived", "lost", "served", "queue"])
    stats = {"clients": log.arrived.sum()}
    stats.update(center.getStatistics())
    stats["avgQueue"] = log.queue.mean()
    return stats, log

def runExperiments(n=100, **params):
    results = []
    logs = []

    for i in range(n):
        stats, log = runModel(seed=i, **params)
        log["run"] = i
        results.append(stats)
        logs.append(log)

    results = pd.DataFrame(results)
    results["lossRate"] = results.lost / results.clients
    results["utilization"] = results.busyTime / (STEPS * MASTERS)
    return results, pd.concat(logs, ignore_index=True)

if __name__ == "__main__":
    pd.set_option("display.width", 200)
    stats, log = runModel(seed=0)

    print("Лог першого дня одного прогону")
    print(log[log.day == 1].to_string(index=False))
    print("Підсумки прогону")

    for key, value in stats.items():
        print(key, round(float(value), 2))

    results, logs = runExperiments(100)

    print("Середні показники за 100 прогонів")
    print(results.describe().loc[["mean", "std", "min", "max"]].T.round(3).to_string())
    print("Середні значення за годинами доби")
    print(logs.groupby("hour")[["arrived", "lost", "served", "queue"]].mean().round(3).to_string())