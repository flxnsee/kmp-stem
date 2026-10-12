import pandas as pd
from simulation import runExperiments

WAGES = [1500, 2000, 3000]
rows = []

for wage in WAGES:
    for c in range(1, 7):
        r, logs = runExperiments(100, masters=c, wage=wage)
        rows.append([wage, c, r.revenue.mean(), r.lostProfit.mean(), r.wages.mean(), r.profit.mean()])

table = pd.DataFrame(rows, columns=["wage", "masters", "revenue", "lostProfit", "wages", "profit"])
print(table.round(0).to_string(index=False))

best = table.loc[table.groupby("wage").profit.idxmax()]
print("Найвигідніша кількість майстрів для кожної зарплати")
print(best[["wage", "masters", "profit"]].round(0).to_string(index=False))