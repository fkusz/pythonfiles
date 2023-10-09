import math
from datetime import datetime
import copy

class GamePiece: #Create the GamePiece class which can be used to create new pieces
    def __init__(self,size,color,icon):
        self.size  = size
        self.color = color
        self.icon  = icon

######################## Set up the Game Board ################################
N = GamePiece(0,'NULL',' ') # Create the NULL piece, which is useful for keeping functions consistent
theBoard = {'a1': [N] , 'a2': [N] , 'a3': [N] ,
            'b1': [N] , 'b2': [N] , 'b3': [N] ,
            'c1': [N] , 'c2': [N] , 'c3': [N] , '0': [N] } # position 0 is "off the board"
def printBoard(board):
    print('\n')
    print('  1   2   3' )
    print('a ' + board['a1'][-1].icon + ' | ' + board['a2'][-1].icon + ' | ' + board['a3'][-1].icon)
    print(' ---+---+---')
    print('b ' + board['b1'][-1].icon + ' | ' + board['b2'][-1].icon + ' | ' + board['b3'][-1].icon)
    print(' ---+---+---')
    print('c ' + board['c1'][-1].icon + ' | ' + board['c2'][-1].icon + ' | ' + board['c3'][-1].icon)
    
board_keys = ['b2','a1','a3','c1','c3','a2','b1','b3','c2']
###############################################################################
####################### Handle pieces and the board easier ####################
def BoardColor(board, KEY):
    return board[KEY][-1].color

def keycheck(KEY):
    if theBoard.get(KEY) or KEY == '':
        return True
    print("That's not a valid space!")
    return False

def getpiece(board, color, size = None, FROM = None): # return (Piece, Index)
    if FROM == None:
        UNUSED_PIECES = len(board['0'])
        for item in range(UNUSED_PIECES):
            if (color == board['0'][item].color)\
            and (size == board['0'][item].size):
                    PlayPiece = board['0'][item]
                    return PlayPiece, item
        return None, None
    else:
        return theBoard[FROM][-1] , -1
    
def CheckWin(board, color): #We check each color individually, because a player can win on a turn that isn't theirs.
    if (BoardColor(board, 'a1') == BoardColor(board, 'a2') == BoardColor(board, 'a3') == color)\
    or (BoardColor(board, 'b1') == BoardColor(board, 'b2') == BoardColor(board, 'b3') == color)\
    or (BoardColor(board, 'c1') == BoardColor(board, 'c2') == BoardColor(board, 'c3') == color)\
    or (BoardColor(board, 'c1') == BoardColor(board, 'b1') == BoardColor(board, 'a1') == color)\
    or (BoardColor(board, 'c2') == BoardColor(board, 'b2') == BoardColor(board, 'a2') == color)\
    or (BoardColor(board, 'c3') == BoardColor(board, 'b3') == BoardColor(board, 'a3') == color)\
    or (BoardColor(board, 'a1') == BoardColor(board, 'b2') == BoardColor(board, 'c3') == color)\
    or (BoardColor(board, 'c1') == BoardColor(board, 'b2') == BoardColor(board, 'a3') == color):
        return True
    return False
#####################################################################
################# Minimax functions ####################################
def minimax(board, depth, player):
    Moves = validmoves(board, player)
    length = len(Moves)
    if CheckWin(board, 'Blue') or CheckWin(board, 'Black'):
        return simplescore(board, switchplayers(player)), None
    if depth == 0 or length == 0:
        return 0, None
    if player == 'Blue':
        Max = -100
        for move in Moves:
            CopyBoard = copy.deepcopy(board)
            Play, Index = getpiece(board, player, size = move[1])
            CopyBoard[move[0]].append(Play)
            CopyBoard['0'].pop(Index)
            Score = minimax(CopyBoard, depth-1, switchplayers(player))[0]
            if Score > Max:
                Max = Score
                Move = move
                if Max == 50:
                    return Max, Move
        return Max, Move
    else:
        Min = 100
        for move in Moves:
            CopyBoard = copy.deepcopy(board)
            #printBoard(CopyBoard)
            Play, Index = getpiece(CopyBoard, player, size = move[1])
            CopyBoard[move[0]].append(Play)
            CopyBoard['0'].pop(Index)
            Score = minimax(CopyBoard, depth-1, switchplayers(player))[0]
            if Score < Min:
                Min = Score
                Move = move
                if Min == -50:
                    return Min, Move
        return Min, Move
    
    
def simplescore(board, player):
    return 50 if player == 'Blue' else -50
    
def switchplayers(player):
    return 'Black' if player == 'Blue' else 'Blue'    
def validmoves(board, player):
    sizes = getsizes(board,player)
    validmoves = []
    for size in sizes:
        for key in board_keys:
            if board[key][-1].size < size:
                validmoves.append([key,size])
    return validmoves

def getsizes(board, player):
    sizes = []
    for piece in board['0']:
        if piece.color == player:
            sizes.append(piece.size)
    sizes = list(dict.fromkeys(sizes))
    sizes.reverse()
    return(sizes)
###############################################################################
######################## Generate all of the game pieces ######################
def generate_pieces():
    Colors = ['Blue','Black']
    Sizes = [1,2,3]
    Icons = ['1','2','3','A','B','C']        
    for i in range(6): # 6 = len(Icons)
            size  = Sizes[i%3]
            color = Colors[(math.floor(i/3))%2]
            icon  = Icons[i%6]
            GAME_PIECE_TEMP = GamePiece(size, color, icon)
            theBoard['0'].append(GAME_PIECE_TEMP) #Create two of the same pieces.
            theBoard['0'].append(GAME_PIECE_TEMP) #Create two of the same pieces.
    theBoard['0'].pop(0)
###############################################################################

def game():
    generate_pieces()
    game_over = False
    turn = 'Blue'
    count = 0
    
    while game_over == False:
        origin = ''
        size = None
        move = None
        printBoard(theBoard)
        #Ask which piece to move
        if turn == 'Black':
            if count > 1: # Only ask if a piece should be moved after both players have had a turn
                origin = input(turn + ", if you want to move a piece, where from?\n(Just press enter if you do not want to move a piece)\n")
                if not keycheck(origin):
                    continue
                
            #Ask where to move the piece
            move = input("It's your turn, " + turn + ", Move to which place?\n")
            if not keycheck(move):
                    continue
                
            #Ask what size piece to move    
            if origin == '': #If no origin space is given, we need to ask what size piece should be played
                origin = '0'
                size = int(input("What size piece?\n"))
                Play, Index = getpiece(theBoard,turn,size)
            else: #Otherwise we don't ask a size, we play the top piece from the origin space
                Play, Index = getpiece(theBoard,turn, FROM = origin)
                if Play.color != turn: # Check if the piece is the player's color
                    print("That's not your piece! You can't move that!")
                    continue
            
            #Handle the piece we found
            if Play == None: #Stop the player if he tries to play a 3rd new piece of a size
                print("You don't have any more pieces of that size!")
                continue
            else: #Play the piece. this branch removes that piece from where it was and places it in a new spot.
                if theBoard[move][-1].size < Play.size:
                    theBoard[origin].pop(Index)
                    theBoard[move].append(Play)
                    count += 1
                else:
                    print("You can't put that there! Your piece isn't large enough!")
                    continue
        else:
            Start = datetime.now()
            score, bestmove = minimax(theBoard,4+count,turn)
            Stop = datetime.now()
            print(Stop-Start)
            print(score)
            Play, Index = getpiece(theBoard,turn,bestmove[1])
            theBoard[bestmove[0]].append(Play)
            theBoard['0'].pop(Index)
            print("The AI moves size " + str(bestmove[1]) + " to " + bestmove[0])
            count += 1

        #Check both colors for win conditions. Call it a tie if both win simultaneously. 
        if count >= 5:
            Blackwins = CheckWin(theBoard, 'Black')
            Bluewins  = CheckWin(theBoard, 'Blue')
            if Blackwins or Bluewins:
                game_over = True
                winner = 'Black' if Blackwins else 'Blue'
                printBoard(theBoard)
                print("\nGame Over.\n")                
                if (Blackwins and Bluewins):
                    print(" **** It's a tie! ****")
                    break
                print(" **** " +winner + " won. ****")        
                break

        #Change the player after each move.
        turn = switchplayers(turn)   
    
    #Ask if player wants to restart the game or not.
    restart = input("Do want to play Again?(y/n)\n")
    if restart == "y" or restart == "Y":
        for key in board_keys:
            theBoard[key] = [N]
            theBoard['0'] = [N]
        game()

if __name__ == "__main__":
    game()
