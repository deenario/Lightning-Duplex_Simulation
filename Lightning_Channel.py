import random
from configparser import ConfigParser

# USER CLASS
class User:
    def __init__(self, coin, name):
        self.coins = coin
        self.name = name
        self.hash_counter = 0
        self.signature_counter = 0
        self.messages = 0

    def sendCoin(self, amount):
        self.coins -= amount

    def recieveCoin(self, amount):
        self.coins += amount

    # Check overflow occurrence before receiving payment
    def checkOverflow(self, amount):
        if self.coins + amount < self.coins:
            return True
        else:
            return False


def payUser(sender, receiver, amount):
    if not (receiver.checkOverflow(amount)):
        print(sender.name, ' computer a hash & a Signature')
        sender.hash_counter += 1
        sender.signature_counter += 1
        sender.messages += 2
        receiver.hash_counter +=1
        receiver.signature_counter +=1
        receiver.messages += 2
        sender.sendCoin(amount)
        receiver.recieveCoin(amount)
        print(sender.name, ' transferred a coin to ', receiver.name)
    else:
        print('Overflow occured')


def printResults():
    print("-------------------LIGHTNING CHANNEL(FILE READ) SIMULATION ENDS--------------------")
    print(no_payments, ' payments completed.')
    print('After simulation Alice has ', alice.coins, ' coins and bob has ', bob.coins, ' coins')
    print("Total Messages transferred were ", alice.messages + bob.messages)
    print("The unbalanced Condition Occurred ", unbalancedCondition, " times.")

    print("---------------Alices' Statistics---------------")
    print("Messages transferred by Alice are: ", alice.messages)
    print("Hashes created by Alice are: ", alice.hash_counter)
    print("Signatures created by Alice are: ", alice.signature_counter)

    print("---------------Bob's Statistics---------------")
    print("Messages transferred by Bob are: ", bob.messages)
    print("Hashes created by Bob are: ", bob.hash_counter)
    print("Signatures created by Bob are: ", bob.signature_counter)


def coin_Toss():
    with open('coin_toss.txt','r') as f:
        for line in f:
            for ch in line:
                coinTossList.append(int(ch))


def writeforGraphs(TotalMessages):
    with open('LightningResults.txt', 'a') as f:
        f.write(str(TotalMessages) + "\n")

cfg = ConfigParser()
cfg.read('config.ini')

# variables needed in the simulation
user1Coins = int(cfg.get('Lightning_Variables','user1coins'))
user2Coins = int(cfg.get('Lightning_Variables','user2coins'))
amount_to_transfer = int(cfg.get('Lightning_Variables','amount_to_transfer'))
_rounds = 0
unbalancedCondition = 0
coinTossList = []
i = 0

# create two objects of the user class
alice = User(user1Coins, 'alice')
bob = User(user2Coins, 'bob')

# input required for the number of payments
print("LIGHTNING CHANNEL SIMULATION")
readFromFile = int(input("Do you want to read coin toss from the file (1 YES , 0 NO): "))
if readFromFile == 1:
    coin_Toss()
    no_payments = len(coinTossList)
else:
    no_payments = int(input("Enter the number of payments you want to Simulate: "))


# for loop to run X times
for x in range(no_payments):
    _rounds += 1
    print('ROUND # ', _rounds)
    # if Alice or Bob gets to an unbalanced state of ZERO coins
    # Alice has Zero Coins
    if 1 > alice.coins:
        print('Unbalanced Condition Alice has no coins')
        payUser(bob, alice, amount_to_transfer)
        unbalancedCondition += 1
    # bob has Zero coins
    elif 1 > bob.coins:
        print('Unbalanced Condition Bob has no coins')
        payUser(alice, bob, amount_to_transfer)
        unbalancedCondition += 1

    else:
        if readFromFile == 1:
            # coin Toss between head and tails.
            # Head = 1 & tail = 0
            coinToss = coinTossList[i]
            # coin toss = 1 = heads . Alice pays bob
            if 1 == coinToss:
                payUser(alice, bob, amount_to_transfer)
            # coin toss = 0 = Tails . Bob pays Alice
            else:
                payUser(bob, alice, amount_to_transfer)
            i += 1
        else:
            # coin Toss between head and tails.
            # Head = 1 & tail = 0
            coinToss = random.randint(0,1)
            # coin toss = 1 = heads . Alice pays bob
            if 1 == coinToss:
                payUser(alice, bob, amount_to_transfer)
            # coin toss = 0 = Tails . Bob pays Alice
            else:
                payUser(bob, alice, amount_to_transfer)

        print('New state of coins is that ', alice.name, ' has ', alice.coins, ' coins and ', bob.name, ' has ', bob.coins,
              ' coins')
    writeforGraphs(alice.messages + bob.messages)

printResults()
