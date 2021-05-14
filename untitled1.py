Square_State = [1,2,3,'a','b','c',[1,2],[1,3],[1,'b'],[1,'c'],['a',2],['a',3],
                ['a','b'],['a','c'],[2,3],[2,'c'],['b',3],['b','c'],[1,2,3],
                [1,2,'c'],[1,'b',3],[1,'b','c'],['a',2,3],['a',2,'c'],
                ['a','b',3],['a','b','c']]

theBoard = {'7': [' '] , '8': [' '] , '9': [' '] ,
            '4': [' '] , '5': [' '] , '6': [' '] ,
            '1': [' '] , '2': [' '] , '3': [' '] }

print(len(theBoard['7']))
board_keys = []
for key in theBoard:
    board_keys.append(key)

def printBoard(board):
    print(board['7'][0] + '|' + board['8'][0] + '|' + board['9'][0])
    print('-+-+-')
    print(board['4'][0] + '|' + board['5'][0] + '|' + board['6'][0])
    print('-+-+-')
    print(board['1'][0] + '|' + board['2'][0] + '|' + board['3'][0])

colors = ['White','Black']
Sizes = [1,2,3]
class GamePiece:
    def __init__(self,size,color):
        self.size = size
        self.color = color

w1=0
w2=0
w3=0
b1=0
b2=0
b3=0
    
Pieces = [GamePiece(size,color) for size in Sizes for color in colors]
Labels = [w1,w2,w3,b1,b2,b3]
w1 = Pieces[0]
print(vars(w1))

def game():

    turn = 'X'
    count = 0


    for i in range(10):
        printBoard(theBoard)
        print("It's your turn, " + turn + " Move to which place?")

        move, FROM, size = input()        

        if theBoard[move] == [' ']:
            theBoard[move][0] == turn
            count += 1
        elif theBoard[move][0] < size:
            theBoard[move].append(turn)
            count += 1
        else:
            print("You can't put that there!.\nMove to which place?")
            continue

        # Now we will check if player X or O has won,for every move after 5 moves. 
        if count >= 5:
            if theBoard['7'] == theBoard['8'] == theBoard['9'] != ' ': # across the top
                printBoard(theBoard)
                print("\nGame Over.\n")                
                print(" **** " +turn + " won. ****")                
                break
            elif theBoard['4'] == theBoard['5'] == theBoard['6'] != ' ': # across the middle
                printBoard(theBoard)
                print("\nGame Over.\n")                
                print(" **** " +turn + " won. ****")
                break
            elif theBoard['1'] == theBoard['2'] == theBoard['3'] != ' ': # across the bottom
                printBoard(theBoard)
                print("\nGame Over.\n")                
                print(" **** " +turn + " won. ****")
                break
            elif theBoard['1'] == theBoard['4'] == theBoard['7'] != ' ': # down the left side
                printBoard(theBoard)
                print("\nGame Over.\n")                
                print(" **** " +turn + " won. ****")
                break
            elif theBoard['2'] == theBoard['5'] == theBoard['8'] != ' ': # down the middle
                printBoard(theBoard)
                print("\nGame Over.\n")                
                print(" **** " +turn + " won. ****")
                break
            elif theBoard['3'] == theBoard['6'] == theBoard['9'] != ' ': # down the right side
                printBoard(theBoard)
                print("\nGame Over.\n")                
                print(" **** " +turn + " won. ****")
                break 
            elif theBoard['7'] == theBoard['5'] == theBoard['3'] != ' ': # diagonal
                printBoard(theBoard)
                print("\nGame Over.\n")                
                print(" **** " +turn + " won. ****")
                break
            elif theBoard['1'] == theBoard['5'] == theBoard['9'] != ' ': # diagonal
                printBoard(theBoard)
                print("\nGame Over.\n")                
                print(" **** " +turn + " won. ****")
                break 

        # If neither X nor O wins and the board is full, we'll declare the result as 'tie'.
        if count == 9:
            print("\nGame Over.\n")                
            print("It's a Tie!!")

        # Now we have to change the player after every move.
        if turn =='X':
            turn = 'O'
        else:
            turn = 'X'        
    
    # Now we will ask if player wants to restart the game or not.
    restart = input("Do want to play Again?(y/n)")
    if restart == "y" or restart == "Y":  
        for key in board_keys:
            theBoard[key] = " "

        game()

if __name__ == "__main__":
    game()
