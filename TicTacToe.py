from datetime import datetime
#It's starting to seem like a dictionary is a BAD way to code tic tac toe
theBoard = {'a1': ' ' , 'a2': ' ' , 'a3': ' ' ,
            'b1': ' ' , 'b2': ' ' , 'b3': ' ' ,
            'c1': ' ' , 'c2': ' ' , 'c3': ' ' }

# I populated board_keys in a specific order, starting with spaces-
# having the highest utility and ending with the least.
# This will be helpful in the event of alpha-beta pruning
board_keys = ['b2','a1','a3','c1','c3','a2','b1','b3','c2']
# for key in theBoard:
#     board_keys.append(key)

def printBoard(board):
    print('\n')
    print('  1   2   3' )
    print('a ' + board['a1'] + ' | ' + board['a2'] + ' | ' + board['a3'])
    print(' ---+---+---')
    print('b ' + board['b1'] + ' | ' + board['b2'] + ' | ' + board['b3'])
    print(' ---+---+---')
    print('c ' + board['c1'] + ' | ' + board['c2'] + ' | ' + board['c3'])

def CheckWin(board):
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

# ALWAYS CheckWin(board) BEFORE CheckTie(board)
# Did not use if count == 9 to check for a tie because I wanted this to be transferable
# To games where a set number of turns don't cause a tie.
def CheckTie(board):
    for key in board_keys:
        if board[key] == ' ':
            return False
    return True

# Won't work for Alpha Beta Pruning
# def minimax(board, depth, player):
#     Scores = []
#     Moves = validmoves(board, player)
#     if depth == 0:
#         return 0, None
#     if CheckWin(board):
#         return simplescore(board, switchplayers(player)), None
#     for move in Moves:
#         CopyBoard = board.copy()
#         CopyBoard[move] = player
#         Scores.append(minimax(CopyBoard, depth-1, switchplayers(player))[0])
#     if player == 'X':
#         Max = max(Scores)
#         Move = Moves[Scores.index(Max)]
#         return Max, Move
#     else:
#         Min = min(Scores)
#         Move = Moves[Scores.index(Min)]
#         return Min, Move

###############################################################################
#Need to rewrite how it works for Alpha Beta Pruning. This is that attempt
def minimax(board, depth, player):
    Moves = validmoves(board, player)
    if depth == 0:
        return 0, None
    if CheckWin(board):
        return simplescore(board, switchplayers(player)), None
    if player == 'X':
        Max = -100
        for move in Moves:
            CopyBoard = board.copy()
            CopyBoard[move] = player
            Score = minimax(CopyBoard, depth-1, switchplayers(player))[0]
            if Score > Max:
                Max = Score
                Move = move
        return Max, Move
    else:
        Min = 100
        for move in Moves:
            CopyBoard = board.copy()
            CopyBoard[move] = player
            Score = minimax(CopyBoard, depth-1, switchplayers(player))[0]
            if Score < Min:
                Min = Score
                Move = move
        return Min, Move
###############################################################################
def simplescore(board, player):
    return 20 if player == 'X' else -20
def switchplayers(player):
    return 'O' if player == 'X' else 'X'    
def validmoves(board, player):
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

    for i in range(20):
        printBoard(theBoard)
        if turn == 'O':
            print("It's your turn, move to which place?")
            move = input()        
            if keycheck(move):
                if theBoard[move] == ' ':
                    theBoard[move] = turn
                    count += 1
                else:
                    print("That place is already filled.\nMove to which place?")
                    continue
            else:
                continue
        else:
            Start = datetime.now()
            score, bestmove = minimax(theBoard,9-count,turn)
            Stop = datetime.now()
            print(Stop-Start)
            theBoard[bestmove] = turn
            print("The AI moves to " + bestmove)
            count += 1
        # Now we will check if player X or O has won,for every move after 5 moves. 
        if count >= 5:
            if CheckWin(theBoard):
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