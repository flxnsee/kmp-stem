import matplotlib.pyplot as plt
import numpy as np
from simulation import runModel, runExperiments
import pandas as pd

N = 100
SEED = 2 # None

results, logs = runExperiments(N)
_, single_log = runModel(seed = SEED)

def plot_hypothesis_proofs():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    hourly_lost = logs.groupby('hour')['lost'].mean()
    hours = hourly_lost.index

    bars = ax1.bar(hours, hourly_lost, color='#d62728', edgecolor='black', alpha=0.8)
    
    ax1.set_title('Вузьке місце: У які години клієнти йдуть до конкурентів?', pad=15)
    ax1.set_xlabel('Робочі години')
    ax1.set_ylabel('Середня кількість відмов (втрачених клієнтів)')
    
    ax1.set_xticks(range(9, 18))
    ax1.set_xticklabels([f"{h}:00-{h+1}:00" for h in range(9, 18)], rotation=45, ha='right')
    ax1.grid(axis='y', linestyle='--', alpha=0.7)
    
    avg_ticket = 1600 
    
    daily_stats = single_log.groupby('day').agg({
        'served': 'sum',
        'lost': 'sum'
    })
    
    # Розраховуємо гроші
    daily_revenue = daily_stats['served'] * avg_ticket
    daily_lost_profit = daily_stats['lost'] * avg_ticket
    days = daily_stats.index
    
    ax2.bar(days, daily_revenue, label='Отриманий дохід', color='#2ca02c', edgecolor='black', alpha=0.8)
    ax2.bar(days, daily_lost_profit, bottom=daily_revenue, label='Недоотриманий прибуток', color='#ff7f0e', edgecolor='black', alpha=0.8)
    
    ax2.set_title('Щоденна економічна ефективність: Дохід проти Збитків', pad=15)
    ax2.set_xlabel('Дні робочого тижня')
    ax2.set_ylabel('Сума (грн)')
    ax2.set_xticks(days)
    ax2.set_xticklabels([f'День {d}' for d in days])
    
    ax2.legend()
    ax2.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.show()

def plot_combined_timeline():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
    hours_timeline = range(1, 46)
    

    ax1.plot(hours_timeline, single_log['queue'], color='#1f77b4', marker='o', markersize=4, linestyle='-', label='Розмір черги')
    ax1.axhline(y=6, color='#d62728', linestyle='--', linewidth=2, label='Ліміт черги (m=6)')
    
    for day_end in [9, 18, 27, 36]:
        ax1.axvline(x=day_end, color='gray', linestyle=':', alpha=0.7)
        ax1.text(day_end - 4.5, 6.5, f'День {day_end//9}', ha='center', va='bottom', color='gray', fontsize=10, fontweight='bold')
    ax1.text(45 - 4.5, 6.5, 'День 5', ha='center', va='bottom', color='gray', fontsize=10, fontweight='bold')
        
    ax1.set_title('Динаміка розміру черги протягом одного тижня')
    ax1.set_ylabel('Кількість техніки в черзі')
    ax1.set_yticks(range(8)) 
    ax1.legend(loc='lower right')
    ax1.grid(True, axis='y', linestyle='--', alpha=0.7)


    ax2.plot(hours_timeline, single_log['queue_time'], color='#ff7f0e', marker='o', markersize=4, linestyle='-', label='Залишок роботи (годин)')
    
    max_time = single_log['queue_time'].max()
    text_y_pos = max_time * 0.95 if max_time > 0 else 10
    
    for day_end in [9, 18, 27, 36]:
        ax2.axvline(x=day_end, color='gray', linestyle=':', alpha=0.7)

        ax2.text(day_end - 4.5, text_y_pos, f'День {day_end//9}', ha='center', va='bottom', color='gray', fontsize=10, fontweight='bold')
    ax2.text(45 - 4.5, text_y_pos, 'День 5', ha='center', va='bottom', color='gray', fontsize=10, fontweight='bold')
        
    ax2.set_title('Накопичення «боргу» по роботі (годин ремонту в черзі) протягом тижня')
    ax2.set_xlabel('Модельний час')
    ax2.set_ylabel('Загальний час ремонту в черзі (годин)')
    
    ax2.set_xticks(range(1, 46))
    ax2.set_xticklabels(range(1, 46), rotation=90, fontsize=9)
    
    ax2.legend(loc='lower right')
    ax2.grid(True, axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()

""" Етап 1
if __name__ == "__main__":
    plot_combined_timeline()

    plot_hypothesis_proofs()"""

######## Етап 2 ########

def plot_queue_dynamics(queue_df):
    plt.figure(figsize=(12, 6))
    
    plt.plot(queue_df['hour'], queue_df['c=1'], label='1 майстер', marker='o', color='salmon')
    plt.plot(queue_df['hour'], queue_df['c=2'], label='2 майстри', marker='s', color='skyblue')
    plt.plot(queue_df['hour'], queue_df['c=3'], label='3 майстри', marker='^', color='green')
    plt.plot(queue_df['hour'], queue_df['c=4'], label='4 майстри', marker='d', color='purple')
    
    plt.axhline(y=6, color='red', linestyle='--', label='Ліміт черги (m=6)')
    plt.title('Динаміка розміру черги протягом одного тижня')
    plt.xlabel('Модельний час (години)')
    plt.ylabel('Кількість техніки в черзі')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('queue_dynamics.png')
    plt.show()

def plot_lost_hourly(lost_hourly_df):
    plt.figure(figsize=(12, 6))
    
    x = np.arange(len(lost_hourly_df['hour']))
    width = 0.2 
    
    plt.bar(x - width*1.5, lost_hourly_df['c=1'], width, label='1 майстер', color='salmon')
    plt.bar(x - width*0.5, lost_hourly_df['c=2'], width, label='2 майстри', color='skyblue')
    plt.bar(x + width*0.5, lost_hourly_df['c=3'], width, label='3 майстри', color='green')
    plt.bar(x + width*1.5, lost_hourly_df['c=4'], width, label='4 майстри', color='purple')
    
    plt.title('Вузьке місце: У які години клієнти йдуть до конкурентів?')
    plt.xlabel('Година доби')
    plt.ylabel('Середня кількість відмов')
    plt.xticks(x, [f"{h}:00-{h+1}:00" for h in lost_hourly_df['hour']], rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig('lost_hourly.png')
    plt.show()

def plot_financials(summary_df):
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    color = 'tab:green'
    ax1.set_xlabel('Кількість майстрів (c)')
    ax1.set_ylabel('Фінансові показники (грн)', color=color)
    line1 = ax1.plot(summary_df['masters'], summary_df['profit'], color=color, marker='o', linewidth=2, label='Прибуток')
    line_rev = ax1.plot(summary_df['masters'], summary_df['revenue'], color='tab:blue', marker='s', label='Виручка (D)')
    ax1.tick_params(axis='y', labelcolor=color)
    
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Витрати та збитки (грн)', color=color)
    line2 = ax2.plot(summary_df['masters'], summary_df['wages'], color=color, marker='x', linestyle='--', label='Витрати на зарплату')
    line_lost = ax2.plot(summary_df['masters'], summary_df['lostProfit'], color='orange', marker='^', linestyle='-.', label='Недоотриманий прибуток (U)')
    ax2.tick_params(axis='y', labelcolor=color)
    
    lines = line1 + line_rev + line2 + line_lost
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left')
    
    plt.title('Залежність фінансових показників від розміру штату')
    plt.xticks(summary_df['masters'])
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('financials_vs_c.png')
    plt.show()

def plot_utilization(summary_df):
    plt.figure(figsize=(8, 5))
    plt.plot(summary_df['masters'], summary_df['utilization'], marker='D', color='purple', linewidth=2)
    plt.axhline(y=0.75, color='orange', linestyle='--', label='Оптимальна завантаженість (75%)')
    
    plt.title('Завантаженість майстрів залежно від їх кількості')
    plt.xlabel('Кількість майстрів (c)')
    plt.ylabel('Коефіцієнт завантаженості (0-1)')
    plt.xticks(summary_df['masters'])
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('utilization.png')
    plt.show()

if __name__ == "__main__":

    raw_df = pd.read_csv('monte_carlo_results.csv')
    summary_df = raw_df.groupby('masters').mean().reset_index()
    summary_df['profit'] = summary_df['revenue'] - summary_df['wages']
        
    plot_financials(summary_df)
    plot_utilization(summary_df)

    logs_df = pd.read_csv('monte_carlo_logs.csv')

    logs_df['step'] = (logs_df['day'] - 1) * 9 + (logs_df['hour'] - 9) + 1
        
    queue_avg = logs_df.groupby(['masters', 'step'])['queue'].mean().reset_index()
        
    queue_df = pd.DataFrame({'hour': range(1, 46)})
    for c in [1, 2, 3, 4]:
        c_data = queue_avg[queue_avg['masters'] == c]
        queue_df[f'c={c}'] = c_data['queue'].values if not c_data.empty else np.zeros(45)

    plot_queue_dynamics(queue_df)
        
        
    lost_avg = logs_df.groupby(['masters', 'hour'])['lost'].mean().reset_index()
        
    hours_list = sorted(logs_df['hour'].unique())
    lost_hourly_df = pd.DataFrame({'hour': hours_list})
    for c in [1, 2, 3, 4]: 
        c_data = lost_avg[lost_avg['masters'] == c]
        lost_hourly_df[f'c={c}'] = c_data['lost'].values if not c_data.empty else np.zeros(len(hours_list))
                    
    plot_lost_hourly(lost_hourly_df)


