import random
import os

os.system("cls")
userApays = 0
rand = [0 for x in range(1000)]


# writing to file
def writeToFile(no_of_file):
    global rand
    with open('Text_Files\\coin_toss' + str(no_of_file) + '.txt', 'a') as f:
        for x in range(1000):
            f.write(str(rand[x]))
        f.write('\n')
    return


# counting values in array
def countValues():
    global userApays
    global rand
    userApays = 0
    for x in range(1000):
        if rand[x] == 0:
            userApays += 1


# printing count percentage


def printCount():
    global userApays

    print("User A is paying ", round(((userApays / 1000) * 100), 2), " Times and User B is paying ",
          round((((1000 - userApays) / 1000) * 100), 2), " times")
    return


def countAndPrint():
    countValues()
    printCount()
    return


# set values count
def setValueCount(zeroes=50):
    zeroes *= 10
    global userApays
    global rand
    for z in range(1000):
        rand[z] = random.randint(0, 1)
    countValues()
    while userApays < zeroes:
        # if zeros are less
        r = random.randint(0, 999)
        if rand[r] == 1:
            rand[r] = 0
            userApays += 1
    while userApays > zeroes:
        # if ones are less
        r = random.randint(0, 999)
        if rand[r] == 0:
            rand[r] = 1
            userApays -= 1


####################################################
####################################################
####################################################
# initializing random array


countAndPrint()
# equating the equation
for x in range(51):
    for y in range(100):
        setValueCount(x + 50)
        countAndPrint()
        writeToFile(x)