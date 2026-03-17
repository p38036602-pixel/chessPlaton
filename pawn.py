from piece import Piece

class Pawn(Piece):
    def __str__(self):
        return "♙" if self.color == "white" else "♟"

    def get_possible_moves(self, board):
        moves = []
        # Определяем направление движения пешки
        direction = 1 if self.color == "white" else -1
        # Начальный ряд для пешки
        start_row = 1 if self.color == "white" else 6
        # Ряд, где возможно взятие на проходе
        en_passant_row = 4 if self.color == "white" else 3
        
        # Ход на одну клетку вперед
        x, y = self.x, self.y
        new_y = y + direction
        if 0 <= new_y < 8 and board.grid[new_y][x] is None:
            moves.append((x, new_y))
            
            # Ход на две клетки вперед с начальной позиции
            if y == start_row:
                new_y_2 = y + 2 * direction
                if 0 <= new_y_2 < 8 and board.grid[new_y_2][x] is None:
                    moves.append((x, new_y_2))

        # Взятие вражеских фигур по диагонали
        for dx in [-1, 1]:
            new_x = x + dx
            new_y = y + direction
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                target = board.grid[new_y][new_x]
                if target and target.color != self.color:
                    moves.append((new_x, new_y))
        
        # Взятие на проходе
        if y == en_passant_row:  # Пешка находится в нужном ряду
            for dx in [-1, 1]:
                new_x = x + dx
                if 0 <= new_x < 8:
                    # Проверяем соседнюю клетку
                    adjacent_piece = board.grid[y][new_x]
                    if (adjacent_piece and 
                        adjacent_piece.__class__.__name__ == "Pawn" and 
                        adjacent_piece.color != self.color and
                        hasattr(board, 'last_move') and board.last_move):
                        
                        # Проверяем, была ли это пешка, которая только что сделала ход на 2 клетки
                        last_from, last_to = board.last_move
                        last_piece = board.grid[last_to[1]][last_to[0]]
                        
                        if (last_piece == adjacent_piece and  # Та же пешка
                            abs(last_from[1] - last_to[1]) == 2 and  # Ход на 2 клетки
                            last_to[0] == new_x and  # Та же вертикаль
                            last_to[1] == y):  # Тот же ряд
                            
                            # Добавляем взятие на проходе
                            moves.append((new_x, y + direction))

        return moves