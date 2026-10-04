import math
import numpy as np
from config import PERIODS, CATEGORIES, SIGMA
from service_center import Order

def getLambda(hour, periods=PERIODS):
    for start, end, lam in periods:
        if start <= hour < end:
            return lam
    return 0

def generateClientsCount(hour, periods=PERIODS):
    return np.random.poisson(getLambda(hour, periods))

def generateOrder(arrivalTime, categories=CATEGORIES, sigma=SIGMA):
    probabilities = [category[1] for category in categories]
    i = np.random.choice(len(categories), p=probabilities)
    name, probability, cost, meanTime = categories[i]
    mu = math.log(meanTime) - sigma ** 2 / 2
    repairTime = np.random.lognormal(mu, sigma)
    return Order(name, cost, repairTime, arrivalTime)