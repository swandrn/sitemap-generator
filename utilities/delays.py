import time
import random

def clickDelay() -> float:
    return random.uniform(0.8, 1.2)

def randomFloat(min: float, max: float) -> float:
    return random.uniform(min, max)