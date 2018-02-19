
import matplotlib.pyplot as plt

Duplex = []
Lightning = []
payments = []

with open('DuplexResults.txt', 'r') as f:
    for line in f:
        Duplex.append(int(line))

with open('LightningResults.txt', 'r') as f:
    for line in f:
        Lightning.append(int(line))

for x in range(1000):
    payments.append(x+1)

plt.plot(payments,Duplex, label='Duplex Channel')
plt.plot(payments,Lightning, label='Lightning Channel')
plt.xlabel('Payments')
plt.ylabel('Messages')
plt.title('Lightning & Duplex Comparision')
plt.legend()
plt.show()