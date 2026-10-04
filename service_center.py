from config import DAYS, MASTERS


class Order:
    def __init__(self, category, cost, repairTime, arrivalTime):
        self.category = category
        self.cost = cost
        self.repairTime = repairTime
        self.arrivalTime = arrivalTime
        self.remaining = repairTime


class ServiceCenter:
    def __init__(self, queueLimit, wage):
        self.queueLimit = queueLimit
        self.wage = wage
        self.queue = []
        self.current = None
        self.served = 0
        self.lost = 0
        self.revenue = 0
        self.lostProfit = 0
        self.busyTime = 0

    def freeMasters(self):
        if self.current is None:
            return 1
        return 0

    def loseClient(self, order):
        self.lost += 1
        self.lostProfit += order.cost

    def repair(self, hours):
        while hours > 0:
            if self.current is None:
                if len(self.queue) == 0:
                    break
                self.current = self.queue.pop(0)
            work = min(hours, self.current.remaining)
            self.current.remaining -= work
            self.busyTime += work
            hours -= work
            if self.current.remaining <= 0:
                self.served += 1
                self.revenue += self.current.cost
                self.current = None

    def getStatistics(self):
        wages = self.wage * DAYS * MASTERS
        unfinished = len(self.queue)
        if self.current is not None:
            unfinished += 1
        return {
            "served": self.served,
            "lost": self.lost,
            "unfinished": unfinished,
            "revenue": self.revenue,
            "lostProfit": self.lostProfit,
            "wages": wages,
            "profit": self.revenue - wages,
            "busyTime": self.busyTime,
        }