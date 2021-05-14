import math
# 't' should start at 1 and 'T' should be time in days between t and T. "I"
# should be the initial amount owed in dollars.
t = 1
T = 365
I = 2
while t<T:
    I = I + (0.01)*math.floor(I)
    t += 1
print(I)