from datetime import datetime
import math
p = 1
Time = []
def is_prime(number):   
    for i in range(3, math.ceil(math.sqrt(number))+1,2):       
        if number % i == 0:           
            return False   
    primes.append(number)

while p <= 10:
    startTime = datetime.now()
    number = 1000000
    n = number
    primes = []    
#----------------------INSERT FUNCTION BETWEEN LINES----------------------------------------   
    if (n % 2 == 0):    #This makes sure you always start with an odd number. We only want to check odd numbers for prime-ness
        n = n+1
    n -= 2
    while n >= 3:   #This first while loop continues checking down for primes until we reach n = 2
        is_prime(n)
        n -= 2
    print('Runtime: ' + str(datetime.now() - startTime))
#----------------------INSERT FUNCTION BETWEEN LINES-----------------------------------------------
    p += 1
    Time.append(str(datetime.now()-startTime))
totalSecs = 0
for tm in Time:
    timeParts = [float(s) for s in tm.split(':')]
    totalSecs += (timeParts[0] * 60 + timeParts[1]) * 60 + timeParts[2]
First = totalSecs/len(Time)
print("Average Runtime: " + str(First) + " Seconds")


p = 1
Time = []

while p <= 10:
    startTime = datetime.now()
    n = 1000000
    primes = []
#----------------------INSERT FUNCTION BETWEEN LINES---------------------------------------- 
    if (n % 2 == 0):    #This makes sure you always start with an odd number. We only want to check odd numbers for prime-ness
        n = n-1
    for n in range(n , 2 , -2):   #This first while loop continues checking down for primes until we reach n = 2
        is_prime(n)
    print('Runtime: ' + str(datetime.now() - startTime))
#----------------------INSERT FUNCTION BETWEEN LINES-----------------------------------------------
    p += 1
    Time.append(str(datetime.now()-startTime))
totalSecs = 0
for tm in Time:
    timeParts = [float(s) for s in tm.split(':')]
    totalSecs += (timeParts[0] * 60 + timeParts[1]) * 60 + timeParts[2]
Second = totalSecs/len(Time)
print("Average Runtime: " + str(Second) + " Seconds")

print("The Average Difference Between First and Second is " + str(First-Second))
print("Second is " + str(First/Second) + " times faster")