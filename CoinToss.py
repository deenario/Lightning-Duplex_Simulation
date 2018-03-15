import random

userApays = 0

with open('coin_toss.txt', 'w') as f:
    for x in range(1000):
        if random.randint(0, 1) == 0:
            userApays += 1
        f.write(str(random.randint(0, 1)))

print("User A is paying ", ((userApays / 1000) * 100), " Times and User B is paying ",
      (((1000 - userApays) / 1000) * 100), " times")
