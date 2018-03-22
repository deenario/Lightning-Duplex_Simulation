import random
from configparser import ConfigParser
cfg = ConfigParser()
cfg.read('config.ini')

# USER CLASS
class User:
    def __init__(self, coin, name):
        self.coins = coin
        self.deposited_coins = 0
        self.name = name
        self.hash_counter = 0
        self.signature_counter = 0
        self.messages = 0
        self.refill = 0

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
    if sender.coins == 0:
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


def lightningResetWithPayment(sender, receiver, amount):
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


def lightningResetWithoutPayment(sender, receiver, amount):
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
    else:
        print('Overflow occurred')


def validate_Uncommitted_Coins(sender):
    if sender.deposited_coins > 0:
        return True
    else:
        return False


def validate_Coins(user):
    if user.coins > 0:
        return True
    else:
        return False


def refillChannel(sender,receiver):
    if onewayChannel(sender,receiver,10):
        receiver.refill += 1
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
    print("Refill Occurred in rounds")
    print(refill_Occurred)

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
        with open('Text_Files//DuplexResultsBiased_Messages.txt', 'a') as f:
            f.write(str(alice.messages + bob.messages) + "\n")
        with open('Text_Files//DuplexResultsBiased_Refill.txt', 'w') as f2:
            f2.write("Alice Refill = " + str(alice.refill) + " and Bob Refill " + str(bob.refill) + "\n")

    elif File_Option == 3:
        with open('Text_Files//DuplexResultsUnbiased_Messages.txt', 'a') as f:
            f.write(str(alice.messages + bob.messages) + "\n")
        with open('Text_Files//DuplexResultsUnbiased_Refill.txt', 'w') as f2:
            f2.write("Alice Refill = " + str(alice.refill) + " and Bob Refill " + str(bob.refill) + "\n")

    else:
        with open('Text_Files//DuplexResults.txt', 'a') as f:
            f.write(str(alice.messages + bob.messages) + "\n")
        with open('Text_Files//DuplexResultsUnbiased_Refill.txt', 'w') as f2:
            f2.write("Alice Refill = " + str(alice.refill) + " and Bob Refill " + str(bob.refill) + "\n")


# variables needed in the simulation
user1Coins = int(cfg.get('Lightning_Variables','user1coins'))
user2Coins = int(cfg.get('Lightning_Variables','user2coins'))
amount_to_transfer = int(cfg.get('Lightning_Variables','amount_to_transfer'))
_rounds = 0
lightningResetOccurred = 0
coinTossList = []
i = 0
coinToss = 0
_sender = object
_receiver = object
refill_Occurred = []

# create two objects of the user class
alice = User(user1Coins, 'alice')
bob = User(user2Coins, 'bob')


# input required for the number of payments
print("LIGHTNING DUPLEX SIMULATION")
readFromFile = int(input("Do you want to read coin toss from the file (1 YES , 0 NO): "))
if readFromFile == 1:
    FileOption = int(input("Choose 1 of the following Coin Toss: 1. Biased Alice 2.Biased Bob or 3.Unbiased "))
    coin_Toss(FileOption)
    no_payments = len(coinTossList)
else:
    no_payments = int(input("Enter the number of payments you want to Simulate: "))
payWithReset = int(input("Choose one of the two payment methods. \n 1. Payment + Reset Together \n 2. Payment and "
                         "Reset Separate: "))


# for loop to run X times
for x in range(no_payments):
    if readFromFile == 1:
        coinToss = coinTossList[i]
        if coinToss == 0:
            _sender = alice
            _receiver = bob
        else:
            _sender = bob
            _receiver = alice
        i += 1

    else:
        coinToss = random.randint(0,1)
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
            if payWithReset == 1:
                lightningResetWithPayment(_sender, _receiver, amount_to_transfer)
            else:
                lightningResetWithoutPayment(_sender,_receiver,amount_to_transfer)
        else:
            if validate_Coins(_receiver):
                if refillChannel(_receiver, _sender):
                    print("Refill Occurred ")
                    refill_Occurred.append(x)
                lightningResetWithoutPayment(_sender, _receiver, amount_to_transfer)
            else:
                lightningResetWithoutPayment(_sender,_receiver,amount_to_transfer)
                if refillChannel(_receiver,_sender):
                    print("Refill Occurred ")
                    refill_Occurred.append(x)
                lightningResetWithoutPayment(_sender, _receiver, amount_to_transfer)

    writeforGraphs(FileOption)
    print(alice.name, "has ", alice.coins, " coins to send and has received ", alice.deposited_coins,
          " uncommitted coins and ", bob.name, " has ",
          bob.coins, " coins to send and has received ", bob.deposited_coins, " uncommitted Coins")
printResults()