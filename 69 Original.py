from datetime import datetime
startTime = datetime.now()

n = 1
C = 0
p = 2

while p <= 7:
    while n < 10**p:
        if '69' in str(n):
            C += 1
        n += 1
    print('Count is ' + str(C))
    print('Percentage is ' + str(C/(10**p)))
    p += 1
    print('Runtime: ' + str(datetime.now() - startTime))