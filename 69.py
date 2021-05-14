from datetime import datetime
startTime = datetime.now()

n = 9
C = 0
p = 2

while p <= 7:
    while n < 10**p:
        if '69' in str(n):
            pos = str(n).find('69')
            if pos == p-2:
                n += 10
                C += 1
            else:
                n += 10**(p-pos-2)
                C += 10**(p-pos-2)
        else:
            n += 10
    print('Count is ' + str(C))
    print('Percentage is ' + str(C/(10**p)))
    p += 1
    print('Runtime: ' + str(datetime.now() - startTime))