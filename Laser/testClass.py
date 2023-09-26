import laser
from time import sleep

l = laser.laser()
distList = []
# print(l)

"""te = [0b10101010, 0b10101010]

if [b&0x80 for b in te].count(0x80) > 1:
    print("Two L-Bytes")

l.setMovingAverage(1)
"""
# print(l.get_info())
"""while True:
    print(l.measure())
    sleep(2)
"""

for _ in range(1000):
    sleep(3)
    a = l.measure()
    print(a)
    print(type(a))
    if type(a) == float:
        distList.append(a)
