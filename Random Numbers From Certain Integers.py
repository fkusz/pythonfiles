import random
def randPM(n,d):
    Choices = [2,3,4,6,7,8,9]
    Integers = []
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

    