from datetime import datetime
import math
print("Generate Primes Below:")
n = int(input())
startTime = datetime.now()
primes = []

def is_prime(number):   
    for i in range(3, math.ceil(math.sqrt(number))+1,2):       
        if number % i == 0:           
            return False   
    primes.append(number)

if (n % 2 == 0):    #This makes sure you always start with an odd number. We only want to check odd numbers for prime-ness
    n = n+1
n -= 2


while n >= 3:   #This first while loop continues checking down for primes until we reach n = 2
    is_prime(n)
    n -= 2
    

primes.append(2)
print(primes)
print(str(len(primes)) + " Primes Found")
print('Runtime: ' + str(datetime.now() - startTime))