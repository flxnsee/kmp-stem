import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

def print_pretty_tables():
    print(" 1. Кількість майстрів (monte_carlo_results.csv)")
    try:
        df_results = pd.read_csv('monte_carlo_results.csv')
        summary_results = df_results.groupby('masters').agg({
            'clients': 'mean',
            'served': 'mean',
            'lost': 'mean',
            'revenue': 'mean',
            'lostProfit': 'mean',
            'wages': 'mean',
            'utilization': 'mean'
        }).reset_index()
        
        summary_results['profit'] = summary_results['revenue'] - summary_results['wages']
        
        summary_results.columns = ['Майстри (c)', 'Клієнти', 'Обслуговано', 'Втрачено', 'Виручка (грн)', 'Збитки (грн)', 'Зарплата (грн)', 'Завантаж.', 'Прибуток (грн)']
        print(summary_results.to_string(index=False))
    except FileNotFoundError:
        print("Файл monte_carlo_results.csv не знайдено. Спочатку запустіть simulation.py")

    print(" 2. Оптимум штату для найбільшого прибутку (experiments_matrix.csv)")
    try:
        df_matrix = pd.read_csv('experiments_matrix.csv')
        
        base_queue = df_matrix[df_matrix['queueLimit'] == 6].groupby(['lambda_multiplier', 'masters']).mean().reset_index()
        
        idx_max = base_queue.groupby('lambda_multiplier')['profit'].idxmax()
        optimal_table = base_queue.loc[idx_max, ['lambda_multiplier', 'masters', 'served', 'lost', 'profit', 'utilization']]
        
        optimal_table.columns = ['Множник потоку (x)', 'Оптимум майстрів (c)', 'Обслуговано', 'Втрачено', 'Макс. прибуток (грн)', 'Завантаж.']
        print("Оптимальна кількість майстрів залежно від інтенсивності вхідного потоку (при m=6):")
        print(optimal_table.to_string(index=False))
        
        
    except FileNotFoundError:
        print("Файл experiments_matrix.csv не знайдено. Спочатку запустіть simulation.py")

if __name__ == "__main__":
    print_pretty_tables()