from datetime import datetime

#It's starting to seem like a dictionary is a BAD way to code tic tac toe
theBoard = {'a1': ' ' , 'a2': ' ' , 'a3': ' ' ,
            'b1': ' ' , 'b2': ' ' , 'b3': ' ' ,
            'c1': ' ' , 'c2': ' ' , 'c3': ' ' }

letters = ['a','b','c']
numbers = ['1','2','3']
# I populated board_keys in a specific order, starting with spaces-
# having the highest utility and ending with the least.
# This will be helpful in the event of alpha-beta pruning
board_keys = ['b2','a1','a3','c1','c3','a2','b1','b3','c2']
# for key in theBoard:
#     board_keys.append(key)
        

def counts(move, turn, counter):
    #The counter is [0,0,0,0,0,0,0,0] where the first three entries are the rows from top to bottom
    #the next three entries are the columns from left to right, and the final two entries are diagonal
    #top left to bottom right then top right to bottom left.
    letter, number = list(move)
    letter_index = letters.index(letter)
    number_index = numbers.index(number)
    counter[letter_index]   += 1*turn
    counter[3+number_index] += 1*turn
    if letter_index == number_index:
        counter[6] += 1*turn
    if letter_index == (2-number_index):
        counter[7] += 1*turn
        
def printBoard(board):
    print('\n')
    print('  1   2   3' )
    print('a ' + board['a1'] + ' | ' + board['a2'] + ' | ' + board['a3'])
    print(' ---+---+---')
    print('b ' + board['b1'] + ' | ' + board['b2'] + ' | ' + board['b3'])
    print(' ---+---+---')
    print('c ' + board['c1'] + ' | ' + board['c2'] + ' | ' + board['c3'])


def CheckWin(counter):
    for count in counter:
        if abs(count) == 3:
            return True
    return False

def CheckWinBoard(board):
    if (board['a1'] == board['a2'] == board['a3'] != ' ')\
    or (board['b1'] == board['b2'] == board['b3'] != ' ')\
    or (board['c1'] == board['c2'] == board['c3'] != ' ')\
    or (board['c1'] == board['b1'] == board['a1'] != ' ')\
    or (board['c2'] == board['b2'] == board['a2'] != ' ')\
    or (board['c3'] == board['b3'] == board['a3'] != ' ')\
    or (board['a1'] == board['b2'] == board['c3'] != ' ')\
    or (board['c1'] == board['b2'] == board['a3'] != ' '):
        return True
    return False

# Did not use if count == 9 to check for a tie because I wanted this to be transferable
# To games where a set number of turns don't cause a tie.
def CheckTie(board):
    for key in board_keys:
        if board[key] == ' ':
            return False
    return True

#Need to rewrite how it works for Alpha Beta Pruning. This is that attempt
def minimax(board, depth, player, counter):
    Moves = validmoves(board)
    length = len(Moves)
    if CheckWin(counter):
        return 20+depth, None
    if length == 0 or depth == 0:
        return 0, None
    Max = -100
    for move in Moves:
        CopyCounter = counter.copy()
        theBoard[move] = player
        counts(move, player, CopyCounter)
        Score = minimax(theBoard, depth-1, -player, CopyCounter)[0]
        theBoard[move] = ' '
        if Score > Max:
            Max = Score
            Move = move
            if Max >= 20:
                break
    return -Max, Move
###############################################################################
def switchplayers(player):
    return 'O' if player == 'X' else 'X'    
def validmoves(board):
    validmoves = []
    for key in board_keys:
        if board[key] == ' ':
            validmoves.append(key)
    return validmoves
def keycheck(KEY):
    if theBoard.get(KEY):
        return True
    print("That's not a valid space!")
    return False
# Now we'll write the main function which has all the gameplay functionality.
def game():

    turn = 'X'
    count = 0
    counter = [0,0,0,0,0,0,0,0]
    
    for i in range(20):
        printBoard(theBoard)
        if turn == 'O':
            print("It's your turn, move to which place?")
            move = input()        
            if keycheck(move):
                if theBoard[move] == ' ':
                    theBoard[move] = turn
                    counts(move, -1, counter)
                    count += 1
                else:
                    print("That place is already filled.\nMove to which place?")
                    continue
            else:
                continue
        else:
            Start = datetime.now()
            score, bestmove = minimax(theBoard, 9, 1, counter)
            Stop = datetime.now()
            print(-score, bestmove)
            print(Stop-Start)
            theBoard[bestmove] = turn
            counts(bestmove, 1, counter)
            print("The AI moves to " + bestmove)
            count += 1
            
        # Now we will check if player X or O has won,for every move after 5 moves. 
        if CheckWinBoard(theBoard):
            printBoard(theBoard)
            print("\nGame Over.\n")                
            print(" **** " +turn + " won. ****")
            break 
        if CheckTie(theBoard):
            printBoard(theBoard)
            print("\nGame Over.\n")                
            print("It's a Tie!!")
            break
            
        # Now we have to change the player after every move.
        turn = switchplayers(turn)        
    
    # Now we will ask if player wants to restart the game or not.
    if count == 20 and not CheckTie(theBoard):
        print("How'd you manage to type the wrong space that many times? Your game is canceled!")
    else:
        restart = input("Do want to play Again? (y/n)")
        if restart == "y" or restart == "Y":  
            for key in board_keys:
                theBoard[key] = " "
    
            game()

if __name__ == "__main__":
    game()