I = []
def per(n,C=0):
    if len(str(n)) == 1:
        print(str(I[0]) + ' took ' + str(C) + ' steps to terminate!')
        return 'DONE'
    digits = [int(i) for i in str(n)]
    result = 1
    I.append(n)
    for j in digits:
        result *= j  
    print(result)
    per(result,C+1)
