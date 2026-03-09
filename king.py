from piece import Piece

class King(Piece):
    def __str__(self):
        return "♔" if self.color == "white" else "♚"
    
    def get_possible_moves(self, board):
        moves = []
        # Все соседние клетки
        king_moves = [
            (0, 1), (0, -1), (1, 0), (-1, 0),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        
        for dx, dy in king_moves:
            new_x = self.x + dx
            new_y = self.y + dy
            
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                target = board.grid[new_y][new_x]
                if target is None or target.color != self.color:
                    moves.append((new_x, new_y))    
        return moves
