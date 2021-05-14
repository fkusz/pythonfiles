import random

#Setup the function, "per" which multiplies the digits of a number and returns
#until it is 1 digit long
I = []
def per(n,C=0):
    if len(str(n)) == 1:
        if C > 10:
            print(str(I[0]) + ' took ' + str(C) + ' steps to terminate!')
            return C
            return 'Done'
        else:
            return 'Done'
    digits = [int(i) for i in str(n)]
    result = 1
    I.append(n)
    for j in digits:
        result *= j
    per(result,C+1)
    
# Create 'n' random integers we like with length 'd'
Integers = []
def randPM(n,d):
    Choices = [2,3,4,6,7,8,9]
    s=''
    h = 1
    while h <= n:
        Con = []
        for x in range(d):
            rand = random.randint(0,6)
            Con.append(str(Choices[rand]))
        h += 1
        Int = int(s.join(Con))
        Integers.append(Int)
    return(Integers)
    
# Generate numbers with randPM  
randPM(50000,20)
    
#Run per() for each of the random numbers generated!
for l in Integers:
    I = []
    per(l)
print('Finished!')
    
