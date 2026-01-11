from enum import IntEnum

# 反発係数や摩擦の計算方法
class CombineMode(IntEnum):
    AVERAGE = 0
    MIN = 1
    MAX = 2
    MULTIPLY = 3