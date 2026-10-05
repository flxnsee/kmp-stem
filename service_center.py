# service_center.py
from config import HOURS_PER_DAY

class Order:
    def __init__(self, name, cost, repairTime, arrivalTime):
        self.name = name
        self.cost = cost
        self.repairTime = repairTime
        self.arrivalTime = arrivalTime

class ServiceCenter:
    def __init__(self, queueLimit, wage):
        self.queueLimit = queueLimit
        self.wage = wage
        self.queue = []
        
        self.served = 0
        self.lost = 0
        self.lostProfit = 0.0
        self.revenue = 0.0
        self.busyTime = 0.0
        self.wages = 0.0
        self.current_order = None

    def freeMasters(self):
        return 1 if self.current_order is None else 0

    def loseClient(self, order):
        self.lost += 1
        self.lostProfit += order.cost

    def repair(self, step):
        self.wages += self.wage / HOURS_PER_DAY
        
        remaining_time = step
        
        while remaining_time > 0:
            # Якщо майстер вільний і є черга — беремо перший пристрій
            if self.current_order is None and len(self.queue) > 0:
                self.current_order = self.queue.pop(0)
                
            # Якщо майстер має пристрій для ремонту
            if self.current_order is not None:
                worked = min(remaining_time, self.current_order.repairTime)
                self.busyTime += worked
                self.current_order.repairTime -= worked
                remaining_time -= worked # Віднімаємо витрачений час від нашої 1 години
                
                # Якщо ремонт завершено
                if self.current_order.repairTime <= 0:
                    self.served += 1
                    self.revenue += self.current_order.cost
                    self.current_order = None
            else:
                break

    def getStatistics(self):
        return {
            "served": self.served,
            "lost": self.lost,
            "unfinished": len(self.queue) + (1 if self.current_order is not None else 0),
            "revenue": self.revenue,
            "lostProfit": self.lostProfit,
            "busyTime": self.busyTime,
            "wages": self.wages,
            "profit": self.revenue - self.wages
        }