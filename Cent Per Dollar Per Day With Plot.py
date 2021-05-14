import math
import matplotlib.pyplot as plt
import numpy as np
t = 1
end = 365
I = 1
array = [I]
while t<end:
    I = I + (0.01)*math.floor(I)
    array.append(I)
    t += 1
plt.xlabel("Day")
plt.ylabel("Cost")
plt.grid(True)
#plt.axis([t,end,array[0],1.05*array[end-1]])
plt.plot(array)
plt.show()
print(I)