STEP = 1
START_HOUR = 9
HOURS_PER_DAY = 9
DAYS = 5
STEPS = DAYS * HOURS_PER_DAY
PERIODS = [
    (9, 10, 1.25),
    (10, 13, 1.0),
    (13, 15, 2.0),
    (15, 17, 1.0),
    (17, 18, 1.25)
]
CATEGORIES = [
    ("Смартфон", 0.45, 1200, 1.0),
    ("Ноутбук", 0.30, 2000, 2.0),
    ("Планшет", 0.15, 1500, 1.5),
    ("Ігрова консоль", 0.10, 1800, 1.75)
]
SIGMA = 0.4
WAGE = 2000
QUEUE_LIMIT = 6
MASTERS = 1