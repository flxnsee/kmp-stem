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

def runModel(periods=PERIODS, categories=CATEGORIES, queueLimit=QUEUE_LIMIT, wage=WAGE, masters=MASTERS, seed=None):
    if seed is not None:
        np.random.seed(seed)

    center = ServiceCenter(queueLimit, wage, masters)
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
        work_time = sum(order.repairTime for order in center.queue)
        work_time += sum(order.repairTime for order in center.masters if order is not None)
            
        log.append([day, hour, arrived, lost, center.served - servedBefore, len(center.queue), work_time])

    log = pd.DataFrame(log, columns=["day", "hour", "arrived", "lost", "served", "queue", "queue_time"])
    stats = {"clients": log.arrived.sum()}
    stats.update(center.getStatistics())
    stats["avgQueue"] = log.queue.mean()
    return stats, log

"""if __name__ == "__main__":
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
    print(logs.groupby("hour")[["arrived", "lost", "served", "queue"]].mean().round(3).to_string())"""

####### Етап 2 #######

def runExperiments(n=100, **params):
    results = []
    logs = []
    
    masters = params.get('masters', 1)

    for i in range(n):
        stats, log = runModel(seed=i, **params)
        log["run"] = i
        results.append(stats)
        logs.append(log)

    results = pd.DataFrame(results)
    results["lossRate"] = results.lost / results.clients
    
    results['utilization'] = results['busyTime'] / (STEPS * masters)
    
    return results, pd.concat(logs, ignore_index=True)

def run_all_masters(max_masters=6, n=100, **params):
    all_data = pd.DataFrame()
    all_logs = pd.DataFrame() 
    
    for c in range(1, max_masters + 1):
        results, logs = runExperiments(n=n, masters=c, **params)
        
        results['masters'] = c
        logs['masters'] = c 
        
        all_data = pd.concat([all_data, results], ignore_index=True)
        all_logs = pd.concat([all_logs, logs], ignore_index=True) 
        
    all_data.to_csv('monte_carlo_results.csv', index=False)
    all_logs.to_csv('monte_carlo_logs.csv', index=False)
    
    summary = all_data.groupby('masters').mean().reset_index()
    return all_data, summary

def run_experiments_matrix():
    flow_multipliers = [0.5, 1.0, 1.5, 2.0]
    queue_capacities = [3, 6, 10]
    all_experiments_data = pd.DataFrame()
    
    for m in queue_capacities:
        for multiplier in flow_multipliers:
            print(f"Запуск: черга m={m}, потік x{multiplier}")
            
            current_periods = [(start, end, lam * multiplier) for start, end, lam in PERIODS]
            
            for c in range(1, 7):
                results, logs = runExperiments(n=100, masters=c, queueLimit=m, periods=current_periods)
                
                results['masters'] = c
                results['queueLimit'] = m
                results['lambda_multiplier'] = multiplier
                
                all_experiments_data = pd.concat([all_experiments_data, results], ignore_index=True)
                
    all_experiments_data.to_csv('experiments_matrix.csv', index=False)
    summary = all_experiments_data.groupby(['queueLimit', 'lambda_multiplier', 'masters']).mean().reset_index()
    return summary


if __name__ == "__main__":
    print("Запуск прогонів для c = 1...6...")
    
    all_data, summary_data = run_all_masters(max_masters=6)
    
    print("\nСередні показники для кожної кількості майстрів:")
    print(summary_data[['masters', 'lost', 'profit', 'utilization']])
    
    print("\nЗапуск матриці експериментів (потік + черга)...")
    matrix_summary = run_experiments_matrix()
    
    print("\nЕксперименти завершено! Дані збережено у CSV-файли.")
