__author__ = 'joagy323'
import time

life = list(range(100))
nothing = 0
def the_end(ever):
        if ever % 20 == nothing:
            return "\n"
        if ever % 3 == 0:
            return '  '
        return ' '

for ever in life:
    life.append(ever)
    print("bää", end=the_end(ever))
    time.sleep(0.005)