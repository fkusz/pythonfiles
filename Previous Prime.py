import math
print("Input now")
number = int(input())
n = number - 1
count = 0
while (n >= 1):
    m = 2
    while (m <= math.floor(math.sqrt(n))):
        if (n % m == 0):
            count += 1
            break
        m += 1
    if count == 0:
        if n == 1:
            print("No prime number less than " + str(number))
            break
        print(str(n) + " is the first prime number before " + str(number))
        break
    n -= 1
    count = 0