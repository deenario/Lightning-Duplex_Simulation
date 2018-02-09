import random

# USER CLASS
class User:
    def __init__(self, coin, name):
        self.coins = coin
        self.name = name
        self.hash_counter = 0
        self.signature_counter = 0

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
        sender.sendCoin(amount)
        receiver.recieveCoin(amount)
        print(sender.name, ' transferred a coin to ', receiver.name)
    else:
        print('Overflow occured')


# create two objects of the user class
alice = User(10, 'alice')
bob = User(10, 'bob')

# varialbles needed in the simulation
_rounds = 0
unbalancedCondition = 0

# input required for the number of payments
print("LIGHTNING CHANNEL SIMULATION")
no_payments = int(input("Enter the number of payments you want to Simulate: "))
amount_to_transfer = int(input("Enter the the transaction amount: "))

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
        # coin Toss between head and tails.
        # Head = 1 & tail = 0
        coinToss = random.randint(0, 1)
        # coin toss = 1 = heads . Alice pays bob
        if 1 == coinToss:
            payUser(alice, bob, amount_to_transfer)
        # coin toss = 0 = Tails . Bob pays Alice
        else:
            payUser(bob, alice, amount_to_transfer)
    print('New state of coins is that ', alice.name, ' has ', alice.coins, ' coins and ', bob.name, ' has ', bob.coins,
          ' coins')

print("-------------------LIGHTNING CHANNEL SIMULATION ENDS--------------------")
print(no_payments, ' payments completed.')
print('After simulation Alice has ', alice.coins, ' coins and bob has ', bob.coins, ' coins')
print("Total Messages transferred were ",
      alice.hash_counter + alice.signature_counter + bob.hash_counter + bob.signature_counter)
print("The unbalanced Condition Occurred ", unbalancedCondition, " times.")

print("---------------Alices' Statistics---------------")
print("Messages transferred by Alice are: ", alice.hash_counter + alice.signature_counter)
print("Hashes created by Alice are: ", alice.hash_counter)
print("Signatures created by Alice are: ", alice.signature_counter)

print("---------------Bob's Statistics---------------")
print("Messages transferred by Bob are: ", bob.hash_counter + bob.signature_counter)
print("Hashes created by Bob are: ", bob.hash_counter)
print("Signatures created by Bob are: ", bob.signature_counter)
