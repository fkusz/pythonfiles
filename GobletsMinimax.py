import math
from functools import lru_cache

class TicTacToe:
    def __init__(self):
        self.board = [None] * 9
        self.current_player = '1'
        self.pieces = {'1': 1, '2': 2, '3': 3, 'A': 1, 'B': 2, 'C': 3}
        self.player_pieces_count = {'1': [0, 0, 0], 'A': [0, 0, 0]}
        self.previous_states = []
    
    def is_valid_move(self, position, piece):
        if self.board[position] is None:
            player = '1' if piece in ['1', '2', '3'] else 'A'
            size = self.pieces[str(piece)] - 1
            if self.player_pieces_count[player][size] < 2:
                return True
        elif str(piece) in self.pieces and str(self.board[position]) in self.pieces:
            return self.pieces[str(piece)] > self.pieces[str(self.board[position])]
        return False
    
    def make_move(self, move):
        if move is None:
            return
        if isinstance(move[1], str):
            self.board[move[0]] = move[1]
            player = '1' if move[1] in ['1', '2', '3'] else 'A'
            size = self.pieces[str(move[1])] - 1
            self.player_pieces_count[player][size] += 1
        else:
            self.board[move[1]] = self.board[move[0]]
            self.board[move[0]] = None
    
    def check_game_over(self):
        winning_positions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]               # Diagonals
        ]
    
        for positions in winning_positions:
            if (self.board[positions[0]] in ['1', '2', '3'] and
                self.board[positions[1]] in ['1', '2', '3'] and
                self.board[positions[2]] in ['1', '2', '3']):
                return '1'
            elif (self.board[positions[0]] in ['A', 'B', 'C'] and
                  self.board[positions[1]] in ['A', 'B', 'C'] and
                  self.board[positions[2]] in ['A', 'B', 'C']):
                return 'A'
    
        if None not in self.board:
            return 'Draw'
    
        return None
    
    @lru_cache(maxsize=None)
    def heuristic_eval(self):
        score = 0
        winning_positions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]               # Diagonals
        ]
    
        for positions in winning_positions:
            player_pieces = sum(1 for pos in positions if self.board[pos] in ['1', '2', '3'])
            opponent_pieces = sum(1 for pos in positions if self.board[pos] in ['A', 'B', 'C'])
    
            if player_pieces == 3:
                return 1000
            elif opponent_pieces == 3:
                return -1000
            else:
                score += player_pieces ** 2 - opponent_pieces ** 2
    
            # Encourage blocking the opponent's winning moves
            if opponent_pieces == 2 and player_pieces == 0:
                score -= 50
            elif player_pieces == 2 and opponent_pieces == 0:
                score += 50
    
        # Encourage placing pieces in the center and corners
        center_piece = self.board[4]
        if center_piece in ['1', '2', '3']:
            score += 10
        elif center_piece in ['A', 'B', 'C']:
            score -= 10
    
        corner_positions = [0, 2, 6, 8]
        player_corner_pieces = sum(1 for pos in corner_positions if self.board[pos] in ['1', '2', '3'])
        opponent_corner_pieces = sum(1 for pos in corner_positions if self.board[pos] in ['A', 'B', 'C'])
        score += player_corner_pieces * 5 - opponent_corner_pieces * 5
    
        # Encourage playing more pieces
        player_pieces_count = sum(self.player_pieces_count['1'])
        opponent_pieces_count = sum(self.player_pieces_count['A'])
        score += (6 - player_pieces_count) * 3 - (6 - opponent_pieces_count) * 3
    
        # Encourage covering moves
        for i in range(9):
            if self.board[i] in ['1', '2', '3'] and self.board[i] != '3':
                for j in range(9):
                    if self.board[j] in ['A', 'B', 'C'] and self.pieces[str(self.board[i])] < self.pieces[str(self.board[j])]:
                        score += 20
            elif self.board[i] in ['A', 'B', 'C'] and self.board[i] != 'C':
                for j in range(9):
                    if self.board[j] in ['1', '2', '3'] and self.pieces[str(self.board[i])] < self.pieces[str(self.board[j])]:
                        score -= 20
    
        return score
    
    def minimax(self, depth, is_maximizing, alpha, beta, max_depth=6):
        if depth == max_depth:
            return self.heuristic_eval()
    
        result = self.check_game_over()
        if result is not None:
            if result == 'Draw':
                return 0
            return 1000 if result in ('1', '2', '3') else -1000
    
        if is_maximizing:
            max_eval = -math.inf
            for move in self.get_possible_moves():
                # Create a copy of the board and player_pieces_count for simulation
                board_copy = self.board.copy()
                player_pieces_count_copy = {player: count.copy() for player, count in self.player_pieces_count.items()}
    
                # Make the move on the copied board
                self.make_move(move)
    
                eval = self.minimax(depth + 1, False, alpha, beta, max_depth)
    
                # Undo the move and restore the original board and player_pieces_count
                self.board = board_copy
                self.player_pieces_count = player_pieces_count_copy
    
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for move in self.get_possible_moves():
                # Create a copy of the board and player_pieces_count for simulation
                board_copy = self.board.copy()
                player_pieces_count_copy = {player: count.copy() for player, count in self.player_pieces_count.items()}
    
                # Make the move on the copied board
                self.make_move(move)
    
                eval = self.minimax(depth + 1, True, alpha, beta, max_depth)
    
                # Undo the move and restore the original board and player_pieces_count
                self.board = board_copy
                self.player_pieces_count = player_pieces_count_copy
    
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
    
    def get_possible_moves(self):
        moves = []
        for i in range(9):
            if self.board[i] is None:
                for piece in ['1', '2', '3'] if self.current_player == '1' else ['A', 'B', 'C']:
                    if self.is_valid_move(i, piece):
                        moves.append((i, piece))
            elif str(self.board[i]) in (['1', '2', '3'] if self.current_player == '1' else ['A', 'B', 'C']):
                for j in range(9):
                    if self.board[j] is None and self.is_valid_move(j, self.board[i]):
                        moves.append((i, j))
        return moves
    
    def get_best_move(self, max_depth=6):
         best_eval = -math.inf if self.current_player == '1' else math.inf
         best_move = None
         alpha = -math.inf
         beta = math.inf
         for move in self.get_possible_moves():
             self.make_move(move)
             eval = self.minimax(0, self.current_player != '1', alpha, beta, max_depth)
             if isinstance(move[1], str):
                 self.board[move[0]] = None
                 player = '1' if move[1] in ['1', '2', '3'] else 'A'
                 size = self.pieces[str(move[1])] - 1
                 self.player_pieces_count[player][size] -= 1
             else:
                 self.board[move[0]] = self.board[move[1]]
                 self.board[move[1]] = None
             if self.current_player == '1' and eval > best_eval:
                 best_eval = eval
                 best_move = move
             elif self.current_player != '1' and eval < best_eval:
                 best_eval = eval
                 best_move = move
         return best_move
    
    def visualize_board(self):
        print("Current Game Board:")
        for i in range(3):
            row = ""
            for j in range(3):
                piece = self.board[i * 3 + j]
                if piece is None:
                    row += "- "
                else:
                    row += str(piece) + " "
            print(row)
        print()
    
    def is_repetitive_state(self):
        current_state = tuple(self.board)
        self.previous_states.append(current_state)
    
        if len(self.previous_states) > 9 and self.previous_states[-1] == self.previous_states[-5]:
            return True
    
        return False

# Example usage
game = TicTacToe()
game.visualize_board()

while game.check_game_over() is None:
   best_move = game.get_best_move(max_depth=6)  # Specify the desired max_depth
   game.make_move(best_move)
   game.visualize_board()

   if game.is_repetitive_state():
       print("The game reached a repetitive state. It's a draw!")
       break

   game.current_player = 'A' if game.current_player == '1' else '1'

result = game.check_game_over()
if result == 'Draw':
   print("The game ended in a draw.")
elif result is None:
   print("The game ended in a draw due to repetitive states.")
else:
   print(f"Player {result} wins!")