import transistor as t
from time import sleep

t.init()

while True:
    t.laserON()
    sleep(2)
    t.laserOff()
    sleep(2)
