from piece import Piece

class Pawn(Piece):
    def __str__(self):
        return "♙" if self.color == "white" else "♟"

    def get_possible_moves(self, board):
        moves = []
        # Определяем, в какую сторону двигается фигура
        direction = 1 if self.color == "white" else -1
        start_row = 1 if self.color == "white" else 6
        
        # Продвижение на ОДНУ клетку вперёд
        x, y = self.x, self.y
        new_y = y + direction
        if 0 <= new_y < 8 and board.grid[new_y][x] is None:
            moves.append((x, new_y))
            
            # Продвижение на ДВЕ клетки вперёд
            if y == start_row:
                new_y_2 = y + 2 * direction
                if 0 <= new_y_2 < 8 and board.grid[new_y_2][x] is None:
                    moves.append((x, new_y_2))

        # Взятие вражеских фигур
        for dx in [-1, 1]:
            new_x = x + dx
            new_y = y + direction
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                target = board.grid[new_y][new_x]
                if target and target.color != self.color:
                    moves.append((new_x, new_y))

        return moves