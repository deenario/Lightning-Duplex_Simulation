
import matplotlib.pyplot as plt
import matplotlib.pyplot as mpl

Duplex = []
Lightning = []
payments = []
i = 4
with open('Results//DuplexMessages.txt', 'r') as f:
    for line in f:
        line, none0, none1 = line.partition(".")
        try:
            if i == 4:
                Duplex.append(int(line))
                i = 0
            else:
                i += 1
        except ValueError:
            continue
i = 4

#with open('Results//LightningMessages.txt', 'r') as f1:
#    for line in f1:
#        line, none0, none1 = line.partition(".")
#        try:
#            if i == 4:
#                Lightning.append(int(line))
#                i = 0
#            else:
#                i += 1
#        except ValueError:
#            continue

i = 5

for x in range(11):
    x = x*5
    alice_Pays = x+50
    bob_Pays = (50-x)
    payments.append(str(alice_Pays) + "/" + str(bob_Pays))

payments[10] = '999100/0'
print(payments)
print(Lightning)
print(Duplex)


plt.plot(payments, Duplex, 'bo', linestyle="-", label='Duplex Channel')
#for xy in zip(payments,Duplex):                                       # <--
#    plt.annotate('(%s, %s)' % xy, xy=xy, textcoords='data')


#plt.plot(payments, Lightning, 'bo', linestyle="-", color='r', label='Lightning Channel')
#for xy in zip(payments,Lightning):                                       # <--
#    plt.annotate('(%s, %s)' % xy, xy=xy, textcoords='data')

# ax = plt.gca()
# ax.tick_params(axis='x', which='major', labelsize=5)

plt.xlabel('Simulations')
plt.ylabel('Messages')
plt.title('Lightning & Duplex Comparision')
plt.grid()
plt.show()