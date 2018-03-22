import random

userApays = 0
rand = 0

with open('coin_toss.txt', 'w') as f:
    for x in range(1000):
        rand = random.randint(0, 1)
        if rand == 0:
            userApays += 1
        f.write(str(rand))

print("User A is paying ", ((userApays / 1000) * 100), " Times and User B is paying ",
      (((1000 - userApays) / 1000) * 100), " times")