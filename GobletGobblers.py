import math
from datetime import datetime

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
    
board_keys = [] #This will be used later to wipe the board in the event of a replay
for key in theBoard:
    board_keys.append(key)
###############################################################################
####################### Handle pieces and the board easier ####################
def BoardColor(KEY):
    return theBoard[KEY][-1].color

def keycheck(KEY):
    if theBoard.get(KEY) or KEY == '':
        return True
    print("That's not a valid space!")
    return False

def getpiece(color, size = None, FROM = None): # return (Piece, Index)
    if FROM == None:
        UNUSED_PIECES = len(theBoard['0'])
        for item in range(UNUSED_PIECES):
            if (color == theBoard['0'][item].color)\
            and (size == theBoard['0'][item].size):
                    PlayPiece = theBoard['0'][item]
                    return PlayPiece, item
        return None, None
    else:
        return theBoard[FROM][-1] , -1
    
def CheckWin(color): #We check each color individually, because a player can win on a turn that isn't theirs.
    if (BoardColor('a1') == BoardColor('a2') == BoardColor('a3') == color)\
    or (BoardColor('b1') == BoardColor('b2') == BoardColor('b3') == color)\
    or (BoardColor('c1') == BoardColor('c2') == BoardColor('c3') == color)\
    or (BoardColor('c1') == BoardColor('b1') == BoardColor('a1') == color)\
    or (BoardColor('c2') == BoardColor('b2') == BoardColor('a2') == color)\
    or (BoardColor('c3') == BoardColor('b3') == BoardColor('a3') == color)\
    or (BoardColor('a1') == BoardColor('b2') == BoardColor('c3') == color)\
    or (BoardColor('c1') == BoardColor('b2') == BoardColor('a3') == color):
        return True
    return False
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
            Play, Index = getpiece(turn,size)
        else: #Otherwise we don't ask a size, we play the top piece from the origin space
            Play, Index = getpiece(turn, FROM = origin)
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

        #Check both colors for win conditions. Call it a tie if both win simultaneously. 
        if count >= 5:
            Blackwins = CheckWin('Black')
            Bluewins  = CheckWin('Blue')
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
        turn = 'Black' if (turn == 'Blue') else 'Blue'   
    
    #Ask if player wants to restart the game or not.
    restart = input("Do want to play Again?(y/n)\n")
    if restart == "y" or restart == "Y":
        for key in board_keys:
            theBoard[key] = [N]
        game()

if __name__ == "__main__":
    game()
