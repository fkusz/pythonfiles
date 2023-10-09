import matplotlib.pyplot as plt

def game(Money, Turn, End):
    if Turn == End:
        return Money     
    return(game(Money + 1, Turn + 1, End) + game(1/Money,Turn + 1,End))

y=[]
for i in range(24):
    y.append(game(100,0,i)/(2**i))
    print(y[i])
        
plt.plot(y)