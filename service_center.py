from config import HOURS_PER_DAY

class Order:
    def __init__(self, name, cost, repairTime, arrivalTime):
        self.name = name
        self.cost = cost
        self.repairTime = repairTime
        self.arrivalTime = arrivalTime

class ServiceCenter:
    def __init__(self, queueLimit, wage, masters=1):
        self.queueLimit = queueLimit
        self.wage = wage
        self.queue = []
        self.masters = [None] * masters

        self.served = 0
        self.lost = 0
        self.lostProfit = 0.0
        self.revenue = 0.0
        self.busyTime = 0.0
        self.wages = 0.0

    def freeMasters(self):
        return self.masters.count(None)

    def loseClient(self, order):
        self.lost += 1
        self.lostProfit += order.cost

    def work(self, i, start, step):
        order = self.masters[i]
        worked = min(step - start, order.repairTime)
        order.repairTime -= worked
        self.busyTime += worked

        if order.repairTime > 0:
            return step

        self.served += 1
        self.revenue += order.cost
        self.masters[i] = None

        return start + worked

    def repair(self, step):
        self.wages += self.wage * len(self.masters) / HOURS_PER_DAY
        freeAt = [0.0] * len(self.masters)

        for i in range(len(self.masters)):
            if self.masters[i] is not None:
                freeAt[i] = self.work(i, 0, step)

        while self.queue:
            i = freeAt.index(min(freeAt))

            if freeAt[i] >= step:
                break

            self.masters[i] = self.queue.pop(0)
            freeAt[i] = self.work(i, freeAt[i], step)

    def getStatistics(self):
        return {
            "served": self.served,
            "lost": self.lost,
            "unfinished": len(self.queue) + len(self.masters) - self.freeMasters(),
            "revenue": self.revenue,
            "lostProfit": self.lostProfit,
            "busyTime": self.busyTime,
            "wages": self.wages,
            "profit": self.revenue - self.wages
        }