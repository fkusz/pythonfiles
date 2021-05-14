import random
import matplotlib.pyplot as plt

size = 100

x = [i for i in range(size)]
y = [0 for i in x]
x2 = [i for i in range(size)]
y2 = [(1+.03)**i for i in x2]
for j in range(1):
    A = 1
    for i in x:
        r = random.randint(1,5)
        A = A*(1+r/100)
        y[i] = A
    plt.plot(x,y)
plt.plot(x2,y2)
