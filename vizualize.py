import matplotlib.pyplot as plt
import numpy as np
from simulation import runModel, runExperiments

def plot_hypothesis_proofs():
    results, logs = runExperiments(100)
    
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

    _, single_log = runModel(seed=42)
    
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

def plot_scatter_profit():
    results, _ = runExperiments(100)
    
    # Створюємо окреме вікно
    plt.figure(figsize=(10, 6))
    
    plt.scatter(results['lost'], results['profit'], color='#9467bd', alpha=0.7, edgecolors='black')
    
    z = np.polyfit(results['lost'], results['profit'], 1)
    p = np.poly1d(z)
    plt.plot(results['lost'], p(results['lost']), "r--", linewidth=2, label='Лінія тренду')
    
    plt.title('Залежність прибутку від втрат клієнтів (за 100 тижнів)')
    plt.xlabel('Кількість втрачених клієнтів (за тиждень)')
    plt.ylabel('Чистий прибуток (грн)')
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)
    
    plt.tight_layout()
    plt.show()

import matplotlib.pyplot as plt
from simulation import runModel

def plot_combined_timeline():
    _, single_log = runModel(seed=42)

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

if __name__ == "__main__":
    print("Будуємо графік залежності прибутку...")
    plot_scatter_profit()

    plot_combined_timeline()

    plot_hypothesis_proofs()
    
