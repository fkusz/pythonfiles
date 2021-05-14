import random
delta = .5
x = 1
C = 0
T = 0
M = 0
A = [1,0,0,0]
Trials = 1000000
for i in range(Trials):
    while x > delta:
        x = x*random.random()
        C += 1
    if C > M:
        M = C
    T += C
    C = 0
    x = 1

Z = T/Trials
print(Z)
print(M)
    
        
    