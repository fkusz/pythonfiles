import random
global_memo = {}

def flatten(matrix):
    return [item for sublist in matrix for item in sublist]


class Player:
    #Start each player with a name, ID, and if they're a human player or not.
    def __init__(self, name, identifier, is_AI=False):
        self.name = name
        self.identifier = identifier
        self.pieces = {"1": 2, "2": 2, "3": 2}
        self.AI = is_AI

    def get_pieces(self):
        return [int(size) for size in self.pieces if not self.pieces[size] <= 0]

    def use_piece(self, size):
        if self.pieces[str(size)] > 0:
            self.pieces[str(size)] -= 1
            return Piece(size, self.identifier)
        return None

class Piece:
    def __init__(self, size, owner):
        self.size = size #Size can be 1, 2, or 3 representing small, medium, and large pieces.
        self.owner = owner # Owner can be 0 or 1 representing player 1 and 2

    def __repr__(self):
        return f"{self.owner}{self.size}"


class Stack: 
    
    def __init__(self, stack = None): 
        if stack == None:
            stack = []
        self.pieces = stack
        self.owner = self.top_piece().owner
        self.size = self.top_piece().size

    def add_piece(self, piece):
        if not self.pieces or self.top_piece().size < piece.size:
            self.pieces.append(piece)
            return True
        return False

    def remove_piece(self):
        if self.pieces:
            return self.pieces.pop()
        return None

    def top_piece(self):
        if self.pieces:
            return self.pieces[-1]
        return Piece(0,None)
    
    def Hash(self):
        return "".join(str(p) for p in self.pieces)
    
    def is_empty(self):
        return len(self.pieces) == 0

    def __repr__(self):
        return str(self.pieces[-1]) if self.pieces else "."


class Board:
    def __init__(self):
        self.board = [[Stack() for _ in range(3)] for _ in range(3)]

    def add_piece(self, x, y, piece):
        return self.board[x][y].add_piece(piece)

    def move_piece(self, x1, y1, x2, y2):
        piece = self.board[x1][y1].remove_piece()
        if piece and self.board[x2][y2].add_piece(piece):
            return True
        if piece:
            self.board[x1][y1].add_piece(piece)
        return False

    def check_winner(self):
        lines = []
    
        # The positions to check for wins on the Rows, columns, and diagonals
        lines.extend([[self.board[x][y] for x in range(len(self.board))] for y in range(len(self.board))])
        lines.extend([[self.board[x][y] for y in range(len(self.board))] for x in range(len(self.board))])
        lines.append([self.board[i][i] for i in range(len(self.board))])
        lines.append([self.board[i][len(self.board) - 1 - i] for i in range(len(self.board))])

        for line in lines:
            tops = [stack.top_piece() for stack in line if not stack.is_empty()]
            if len(tops) == len(self.board) and len(set((p.owner for p in tops))) == 1:
                return (True, tops[0].owner)
    
        return (False, None)
    
    def Hash(self):
        return "".join(stack.Hash() for stack in flatten(self.board))

    def __repr__(self):
        return '\n'.join([' '.join([str(cell) for cell in row]) for row in self.board])


class Game:
    def __init__(self):
        self.board = Board()
        self.players = [Player('Player 1', 0, False), Player('Player 2', 1, True)]
        self.current_player_idx = self.players[0].identifier
        self.turn_count = 0

    def switch_player(self):
        self.current_player_idx = 1 - self.current_player_idx

    def current_player(self):
        return self.players[self.current_player_idx]
    
    def check_winner(self):
        return self.board.check_winner()

    def run(self):
        while not self.check_winner()[0]:
            self.play_turn()
            self.switch_player()
            self.turn_count += 1
            print(f"Turn: {self.turn_count}")

        print(self.board)
        print(f"The winner is {self.current_player().name}")
        # else:
        #     print(self.board)
        #     print("The game is a draw")
    
    def get_moves(self, player_id):
        moves = [] # places that a player can move from -> to [x1, y1, x2, y2]
        placements = [] # places that a player can add a new piece to the game board [size, x, y]
        
        pieces_to_place = self.players[player_id].get_pieces()
        
        for p in pieces_to_place:
            for i, row in enumerate(self.board.board):
                for j, stack in enumerate(row):
                    if p > stack.top_piece().size:
                        placements.append([p,i,j])
                        
        for i, row in enumerate(self.board.board):
            for j, stack in enumerate(row):
                if stack.top_piece().owner == player_id:
                    for k, row2 in enumerate(self.board.board):
                        for l, stack2 in enumerate(row2):
                            if stack.top_piece().size > stack2.top_piece().size:                 
                                moves.append([i,j,k,l])
                                
        return placements, moves
    
    
    def get_best_move(self, player_id):
        best_eval = float('-inf')
        placements, moves = self.get_moves(player_id)
        
        if placements: #Pick a random move as best if no best move is found.
            best_move = random.choice(placements)
        else:
            best_move = random.choice(moves)
    
        for place in placements:
            piece = Piece(place[0], player_id)
            self.board.add_piece(place[1], place[2], piece)
            self.turn_count += 1
            move_eval = minimax(self.board, 15, float('-inf'), float('inf'), False, player_id)
            self.board.board[place[1]][place[2]].remove_piece()
            self.turn_count -= 1
            if move_eval > best_eval:
                best_eval = move_eval
                best_move = place
        
        for move in moves:
            piece = Piece(move[0], player_id)
            self.board.move_piece(move[0], move[1], move[2], move[3])
            self.turn_count += 1
            move_eval = minimax(self.board, 15, float('-inf'), float('inf'), False, player_id)
            self.turn_count -= 1
            self.board.move_piece(move[2], move[3], move[0], move[1])
            if move_eval > best_eval:
                best_eval = move_eval
                best_move = move
        
        print(f"Best Eval: {best_eval}")
        return best_move
    
    
    def play_turn(self):
        
        player = self.current_player()
        print(f"{player.name}'s turn:")
        print(self.board)
        
        #Turn for AI Players
        if player.AI == True:
            move = self.get_best_move(player.identifier)
            piece_size = None
            
            if len(move) == 3:  
                piece_size, x, y = move
            elif len(move) == 4:
                x1, y1, x2, y2 = move
            else:
                print(f"Something went wrong with determining the best move. Array: {move}")
                
            if piece_size is not None:
                piece = player.use_piece(piece_size)
                self.board.add_piece(x, y, piece)
                print(f"AI placed {piece} at ({x}, {y}). \n")
            else:
                self.board.move_piece(x1, y1, x2, y2)
                print(f"{self.current_player().name} moved from {(x1, y1)} to {(x2, y2)}. \n")
                
        # Turn for Human Players        
        else:
            while True:
                action = input("Enter 'place' to place a piece or 'move' to move a piece: ").strip().lower()
    
                if action == 'place':
                    piece_size = int(input("Enter piece size (1, 2, 3): ").strip().upper())
                    x, y = map(int, input("Enter coordinates to place piece (row col): ").split())
    
                    piece = player.use_piece(piece_size)
                    print(piece)

                    if piece and self.board.add_piece(x, y, piece):
                        print(f"Placed {piece} at ({x}, {y}).")
                        break
                    else:
                        print("Invalid move. Try again.")
                        if piece:
                            player.pieces[str(piece_size)] += 1  # Return the piece back to player
    
                elif action == 'move':
                    x1, y1 = map(int, input("Enter coordinates to move from (row col): ").split())
                    x2, y2 = map(int, input("Enter coordinates to move to (row col): ").split())
    
                    if self.board.move_piece(x1, y1, x2, y2):
                        print(f"Moved piece from ({x1}, {y1}) to ({x2}, {y2}).")
                        break
                    else:
                        print("Invalid move. Try again.")


def evaluate(board, player_id):
    winner = board.check_winner()[1]
    if winner == player_id:
        return 100 - game.turn_count
    elif winner is not None:
        return -100 + game.turn_count
    else:
        return 0

def minimax(board, depth, alpha, beta, is_maximizing, player_id):
    board_hash = board.Hash()
    if board_hash in global_memo:
        return global_memo[board_hash]

    winner = board.check_winner()[1]
    if winner is not None or depth == 0:
        score = evaluate(board, player_id)
        global_memo[board_hash] = score
        return score

    if is_maximizing:
        max_eval = float('-inf')
        placements, moves = game.get_moves(player_id)
        for place in placements:
            piece = Piece(place[0], player_id)
            board.add_piece(place[1], place[2], piece)
            game.turn_count += 1
            eval = minimax(board, depth - 1, alpha, beta, False, player_id)
            game.turn_count -= 1
            board.board[place[1]][place[2]].remove_piece()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        for move in moves:
            board.move_piece(move[0], move[1], move[2], move[3])
            game.turn_count += 1
            eval = minimax(board, depth - 1, alpha, beta, False, player_id)
            board.move_piece(move[2], move[3], move[0], move[1])
            game.turn_count -= 1
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        global_memo[board_hash] = max_eval
        return max_eval
    
    else:
        min_eval = float('inf')
        opponent_id = 1 - player_id
        placements, moves = game.get_moves(opponent_id)
        for place in placements:
            piece = Piece(place[0], opponent_id)
            board.add_piece(place[1], place[2], piece)
            game.turn_count += 1
            eval = minimax(board, depth - 1, alpha, beta, True, player_id)
            board.board[place[1]][place[2]].remove_piece()
            game.turn_count -= 1
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        for move in moves:
            board.move_piece(move[0], move[1], move[2], move[3])
            game.turn_count += 1
            eval = minimax(board, depth - 1, alpha, beta, True, player_id)
            board.move_piece(move[2], move[3], move[0], move[1])
            game.turn_count -= 1
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        global_memo[board_hash] = min_eval
        return min_eval

game = Game()
game.run()
