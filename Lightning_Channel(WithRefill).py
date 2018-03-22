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
        self.refil = 0

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


def refill(sender,receiver):
    if 0 == sender.coins:
        payUser(receiver,sender,10)
        sender.refil += 1
        return True;
    else:
        return False;


def payUser(sender, receiver, amount):
    if not (receiver.checkOverflow(amount)):
        print(sender.name, ' computer a hash & a Signature')
        sender.hash_counter += 1
        sender.signature_counter += 1
        sender.messages += 2
        receiver.hash_counter += 1
        receiver.signature_counter += 1
        receiver.messages += 2
        sender.sendCoin(amount)
        receiver.recieveCoin(amount)
        print(sender.name, ' transferred a coin to ', receiver.name)
    else:
        print('Overflow occurred')


def printResults():
    print("-------------------LIGHTNING CHANNEL(FILE READ) SIMULATION ENDS--------------------")
    print(no_payments, ' payments completed.')
    print('After simulation Alice has ', alice.coins, ' coins and bob has ', bob.coins, ' coins')
    print("Total Messages transferred were ", alice.messages + bob.messages)

    print("---------------Alice's Statistics---------------")
    print("Messages transferred by Alice are: ", alice.messages)
    print("Hashes created by Alice are: ", alice.hash_counter)
    print("Signatures created by Alice are: ", alice.signature_counter)
    print("Alice refilled her channel ", alice.refil , " times.")

    print("---------------Bob's Statistics---------------")
    print("Messages transferred by Bob are: ", bob.messages)
    print("Hashes created by Bob are: ", bob.hash_counter)
    print("Signatures created by Bob are: ", bob.signature_counter)
    print("Bob refilled his channel ", bob.refil , " times.")


def coin_Toss(Fileoption):
    alicePays = 0
    if Fileoption == 1:
        with open('Text_Files//AlicePaysMore.txt', 'r') as f:
            for line in f:
                for ch in line:
                    coinTossList.append(int(ch))
                    if int(ch) == 0:
                        alicePays += 1
    elif Fileoption == 2:
        with open('Text_Files//BobPaysMore.txt', 'r') as f:
            for line in f:
                for ch in line:
                    coinTossList.append(int(ch))
                    if int(ch) == 0:
                        alicePays += 1
    elif Fileoption == 3:
        with open('Text_Files//UnbaisedCoinToss.txt', 'r') as f:
            for line in f:
                for ch in line:
                    coinTossList.append(int(ch))
                    if int(ch) == 0:
                        alicePays += 1
    else:
        print("Wrong Input run the program again.")
    print("Alice is paying ", ((alicePays / 1000) * 100), " Times and Bob is paying ",
          (((1000 - alicePays) / 1000) * 100), " times")


def writeforGraphs(File_Option):
    if File_Option == 1:
        with open('Text_Files//LightningResultsBiased_Messages.txt', 'a') as f:
            f.write(str(alice.messages + bob.messages) + "\n")
        with open('Text_Files//LightningResultsBiased_Refill.txt', 'w') as f2:
            f2.write("Alice Refill = " + str(alice.refil) + " and Bob Refill " + str(bob.refil) + "\n")

    elif File_Option == 3:
        with open('Text_Files//LightningResultsUnbiased_Messages.txt', 'a') as f:
            f.write(str(alice.messages + bob.messages) + "\n")
        with open('Text_Files//LightningResultsUnbiased_Refill.txt', 'w') as f2:
            f2.write("Alice Refill = " + str(alice.refil) + " and Bob Refill " + str(bob.refil) + "\n")

    else:
        with open('Text_Files//LightningResults.txt', 'a') as f:
            f.write(str(alice.messages + bob.messages) + "\n")
        with open('Text_Files//LightningResultsUnbiased_Refill.txt', 'w') as f2:
            f2.write("Alice Refill = " + str(alice.refil) + " and Bob Refill " + str(bob.refil) + "\n")


cfg = ConfigParser()
cfg.read('config.ini')

# variables needed in the simulation
user1Coins = int(cfg.get('Lightning_Variables', 'user1coins'))
user2Coins = int(cfg.get('Lightning_Variables', 'user2coins'))
amount_to_transfer = int(cfg.get('Lightning_Variables', 'amount_to_transfer'))
_rounds = 0
unbalancedCondition = 0
coinTossList = []
i = 0

# create two objects of the user class
alice = User(user1Coins, 'alice',)
bob = User(user2Coins, 'bob',)

# input required for the number of payments
print("LIGHTNING CHANNEL SIMULATION")
readFromFile = int(input("Do you want to read coin toss from the file (1 YES , 0 NO): "))
if readFromFile == 1:
    FileOption = int(input("Choose 1 of the following Coin Toss: 1. Biased Alice 2.Biased Bob or 3.Unbiased "))
    coin_Toss(FileOption)
    no_payments = len(coinTossList)
else:
    no_payments = int(input("Enter the number of payments you want to Simulate: "))

# for loop to run X times
for x in range(no_payments):
    _rounds += 1
    print('ROUND # ', _rounds)
    # if Alice or Bob gets to an unbalanced state of ZERO coins
    # Alice has Zero Coins

    if refill(alice,bob):
        print('Alice Refilled Her Channel')

    elif refill(bob,alice):
        print('Bob Refilled Her Channel')

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
            coinToss = random.randint(0, 1)
            # coin toss = 1 = heads . Alice pays bob
            if 1 == coinToss:
                payUser(alice, bob, amount_to_transfer)
            # coin toss = 0 = Tails . Bob pays Alice
            else:
                payUser(bob, alice, amount_to_transfer)

    print('New state of coins is that ', alice.name, ' has ', alice.coins, ' coins and ', bob.name, ' has ',
          bob.coins,
          ' coins')
    writeforGraphs(FileOption)

printResults()