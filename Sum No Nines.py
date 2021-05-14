Sum = 0
c = 1

# Sum of 1/c but only if it doesn't contain 9
for i in range(1000000):
    if '9' not in str(c):
        Sum = Sum + 1/c
    c +=1
        
print(Sum)

    