import random


# USER CLASS
class User:
    def __init__(self, coin, name):
        self.coins = coin
        self.deposited_coins = 0
        self.name = name
        self.hash_counter = 0
        self.signature_counter = 0
        self.messages = 0

    def sendCoin(self, amount):
        self.coins -= amount

    def recieveCoin(self, amount):
        self.deposited_coins += amount

    # Check overflow occurrence before receiving payment
    def checkOverflow(self, amount):
        if self.coins + amount < self.coins:
            return True
        else:
            return False


def onewayChannel(sender, receiver, amount):
    if sender.coins < 1:
        return False
    else:
        if not (receiver.checkOverflow(amount)):
            print(sender.name, ' computes 2 Signatures')
            sender.signature_counter += 2
            sender.messages += 1
            sender.sendCoin(amount)
            receiver.recieveCoin(amount)
            print(sender.name, ' transferred a coin to ', receiver.name)
        else:
            print('Overflow occurred')
        return True


def lightningReset(sender, receiver, amount):
    global lightningResetOccurred
    if not (receiver.checkOverflow(amount)):
        print(sender.name, ' computes a hash & a Signature')
        sender.hash_counter += 1
        sender.signature_counter += 1
        sender.messages += 2
        receiver.signature_counter += 1
        receiver.hash_counter += 1
        receiver.messages += 2
        sender.coins = sender.deposited_coins + sender.coins
        receiver.coins = receiver.deposited_coins + receiver.coins
        receiver.deposited_coins = 0
        sender.deposited_coins = 0
        print("Lightning reset Occurred now ")
        lightningResetOccurred += 1
    if onewayChannel(sender, receiver, amount):
        pass
    else:
        print('Overflow occurred')


def validate_Uncommitted_Coins(sender):
    if sender.deposited_coins > 1:
        return True
    else:
        return False


def printResults():
    print("-------------------LIGHTNING DUPLEX WITH COIN TOSS (FILE READ) SIMULATION ENDS--------------------")
    print(no_payments, ' payments completed.')
    print("After Simulation:")
    print('Alice has ', alice.coins, ' coins and bob has ', bob.coins, ' coins')
    print("Alice has received ", alice.deposited_coins, " uncommitted coin and bob has received ", bob.deposited_coins,
          " uncommitted coin")

    print("Total Messages transferred were ", alice.messages + bob.messages)
    print("Lightning Reset Occurred ", lightningResetOccurred, " times.")

    print("---------------Alices' Statistics---------------")
    print("Messages transferred by Alice are: ", alice.messages)
    print("Hashes created by Alice are: ", alice.hash_counter)
    print("Signatures created by Alice are: ", alice.signature_counter)

    print("---------------Bob's Statistics---------------")
    print("Messages transferred by Bob are: ", bob.messages)
    print("Hashes created by Bob are: ", bob.hash_counter)
    print("Signatures created by Bob are: ", bob.signature_counter)


def coin_Toss():
    with open('coin_toss.txt', 'r') as f:
        for line in f:
            for ch in line:
                cointTossList.append(int(ch))


# input required for the number of payments
print("LIGHTNING DUPLEX SIMULATION")
user1Coins = 10  # int(input("Enter the amount of coins that Alice will have: "))
user2Coins = 0  # int(input("Enter the amount of coins that Bob will have: "))
no_payments = int(input("Enter the number of payments you want to Simulate: "))
amount_to_transfer = 1  # int(input("Enter the the transaction amount: "))

# create two objects of the user class
alice = User(user1Coins, 'alice')
bob = User(user2Coins, 'bob')

# variables needed in the simulation
_rounds = 0
lightningResetOccurred = 0
cointTossList = []
coin_Toss()
i = 0
coinToss = 0
_sender = object
_receiver = object

# for loop to run X times
for x in range(no_payments):

    coinToss = cointTossList[i]

    if coinToss == 0:
        _sender = alice
        _receiver = bob
    else:
        _sender = bob
        _receiver = alice

    if onewayChannel(_sender, _receiver, amount_to_transfer):
        print("One way Transfer Occurred")
        print()
    else:
        if validate_Uncommitted_Coins(_sender):
            lightningReset(_sender, _receiver, amount_to_transfer)
        else:
            onewayChannel(_receiver, _sender, amount_to_transfer)

    print(alice.name, "has ", alice.coins, " coins to send and has received ", alice.deposited_coins,
          " uncommitted coins and ", bob.name, " has ",
          bob.coins, " coins to send and has received ", bob.deposited_coins, " uncommitted Coins")
    i += 1

printResults()