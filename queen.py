from piece import Piece

class Queen(Piece):
    def __str__(self):
        return "♕" if self.color == "white" else "♛"
    
    def get_possible_moves(self, board):
        moves = []
        # Все направления: горизонтали, вертикали и диагонали
        directions = [
            (0, 1), (0, -1), (1, 0), (-1, 0),  # как ладья
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # как слон
        ]
        
        for dx, dy in directions:
            for step in range(1, 8):
                new_x = self.x + dx * step
                new_y = self.y + dy * step
                
                if not (0 <= new_x < 8 and 0 <= new_y < 8):
                    break
                
                target = board.grid[new_y][new_x]
                if target is None:
                    moves.append((new_x, new_y))
                elif target.color != self.color:
                    moves.append((new_x, new_y))
                    break
                else:
                    break
                    
        return moves
