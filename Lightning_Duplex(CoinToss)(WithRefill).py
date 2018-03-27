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


def refillChannel(sender, receiver):
    if onewayChannel(sender, receiver, 10):
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


def coin_Toss(no_of_file):
    alicePays = 0
    bobpays = 0
    coinTossList.clear()
    with open('Text_Files//coin_toss' + str(no_of_file) + '.txt', 'r') as f:
        for line in f:
            for ch in line:
                coinTossList.append(int(ch))
                if int(ch) == 0:
                    alicePays += 1

    bobpays = (((1000 - alicePays) / 1000) * 100)
    alicePays = ((alicePays / 1000) * 100)
    bobpays = round(bobpays)
    alicePays = round(alicePays)

    with open('Text_Files//DuplexResults.txt', 'a') as f:
        f.write(
            "Alice is paying {0}% of the Time and Bob is paying {1}% of the Time \n".format(str(alicePays),
                                                                                            str(bobpays)))


def write_for_Graphs():
    with open('Text_Files//DuplexResults.txt', 'a') as f:
        f.write(
            'Messages = {0}\nTotal Refill = {1}\nAlice Refill = {2} and Bob Refill {3}'.format(
                str(alice.messages + bob.messages), str(alice.refill + bob.refill), str(alice.refill), str(bob.refill)))
        f.write("\n\n")


def simulation_Duplex():
    i = 0
    global payWithReset,no_payments
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
            coinToss = random.randint(0, 1)
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
                    lightningResetWithoutPayment(_sender, _receiver, amount_to_transfer)
            else:
                if validate_Coins(_receiver):
                    if refillChannel(_receiver, _sender):
                        print("Refill Occurred ")
                        refill_Occurred.append(x)
                    lightningResetWithoutPayment(_sender, _receiver, amount_to_transfer)
                else:
                    lightningResetWithoutPayment(_sender, _receiver, amount_to_transfer)
                    if refillChannel(_receiver, _sender):
                        print("Refill Occurred ")
                        refill_Occurred.append(x)
                    lightningResetWithoutPayment(_sender, _receiver, amount_to_transfer)

        print(alice.name, "has ", alice.coins, " coins to send and has received ", alice.deposited_coins,
              " uncommitted coins and ", bob.name, " has ",
              bob.coins, " coins to send and has received ", bob.deposited_coins, " uncommitted Coins")



def reset_variables():
    global _rounds, lightningResetOccurred, no_payments
    _rounds = 0
    lightningResetOccurred = 0
    no_payments = 0
    alice.coins = 10
    alice.messages = 0
    alice.refil = 0
    alice.signature_counter = 0
    alice.hash_counter = 0
    bob.coins = 10
    bob.messages = 0
    bob.refil = 0
    bob.signature_counter = 0
    bob.hash_counter = 0


# variables needed in the simulation
user1Coins = int(cfg.get('Lightning_Variables', 'user1coins'))
user2Coins = int(cfg.get('Lightning_Variables', 'user2coins'))
amount_to_transfer = int(cfg.get('Lightning_Variables', 'amount_to_transfer'))
_rounds = 0
lightningResetOccurred = 0
coinTossList = []
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
payWithReset = int(input("Choose one of the two payment methods. \n 1. Payment + Reset Together \n 2. Payment and "
                         "Reset Separate: "))


if readFromFile == 1:
    for x in range(11):
        coin_Toss(x)
        no_payments = len(coinTossList)
        simulation_Duplex()
        printResults()
        write_for_Graphs()
        reset_variables()
else:
    no_payments = int(input("Enter the number of payments you want to Simulate: "))
    simulation_Duplex()
    printResults()
