import pandas as pd
import matplotlib.pyplot as plt
from config import STEPS
from simulation import runExperiments
from analytic_model import analyticModel

rows = []

for c in range(1, 7):
    r, logs = runExperiments(100, masters=c)
    a = analyticModel(c)
    rows.append([c,
                 a["pRefusal"], r.lossRate.mean(),
                 a["kBusy"], (r.busyTime / (STEPS * c)).mean(),
                 a["Lq"], r.avgQueue.mean(),
                 a["profit"], r.profit.mean()])

table = pd.DataFrame(rows, columns=["masters", "lossA", "lossS", "utilA", "utilS", "queueA", "queueS", "profitA", "profitS"])
pd.set_option("display.width", 200)
print("Порівняння аналітичної (A) та імітаційної (S) моделей")
print(table.round(3).to_string(index=False))



fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

ax1.plot(table.masters, table.profitA, marker="o", label="Аналітична модель")
ax1.plot(table.masters, table.profitS, marker="s", label="Імітаційна модель")
ax1.set_title("Чистий прибуток за тиждень")
ax1.set_xlabel("Кількість майстрів (c)")
ax1.set_ylabel("грн")
ax1.legend()
ax1.grid(True)

ax2.plot(table.masters, table.lossA, marker="o", label="Аналітична модель")
ax2.plot(table.masters, table.lossS, marker="s", label="Імітаційна модель")
ax2.set_title("Ймовірність відмови (частка втрачених клієнтів)")
ax2.set_xlabel("Кількість майстрів (c)")
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.savefig("compare_models.png")

plt.show()

fig2, (ax3, ax4) = plt.subplots(1, 2, figsize=(12, 5))

ax3.plot(table.masters, table.utilA, marker="o", label="Аналітична модель", color="#2ca02c")
ax3.plot(table.masters, table.utilS, marker="s", label="Імітаційна модель", color="#d62728")
ax3.set_title("Коефіцієнт завантаженості персоналу")
ax3.set_xlabel("Кількість майстрів (c)")
ax3.set_ylabel("Завантаженість (0-1)")
ax3.axhline(y=0.85, color='gray', linestyle='--', alpha=0.7, label="Комфортний рівень (85%)")
ax3.legend()
ax3.grid(True)

ax4.plot(table.masters, table.queueA, marker="o", label="Аналітична модель", color="#1f77b4")
ax4.plot(table.masters, table.queueS, marker="s", label="Імітаційна модель", color="#ff7f0e")
ax4.set_title("Середня довжина черги")
ax4.set_xlabel("Кількість майстрів (c)")
ax4.set_ylabel("Кількість клієнтів у черзі")
ax4.legend()
ax4.grid(True)

plt.tight_layout()
plt.savefig("additional_comparison.png")

plt.show()