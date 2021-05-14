c = 0

for i in range(2021):
    for j in range(0,i):
        string = "1" * (j+1) + "0" * (i-j-1)
        num = int(string)
        if num % 2020 == 0:
            c += 1

print(c)
    
