import time
import random

def clickDelay() -> int:
    return random.randint(80, 120)

def randomFloat(min: float, max: float) -> float:
    return random.uniform(min, max)