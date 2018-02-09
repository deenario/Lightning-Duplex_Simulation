import random

with open('coin_toss.txt', 'w') as f:
    for x in range(1000):
        f.write(str(random.randint(0,1)))