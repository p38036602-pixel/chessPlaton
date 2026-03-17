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
        
        # Обычные ходы короля
        for dx, dy in king_moves:
            new_x = self.x + dx
            new_y = self.y + dy
            
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                target = board.grid[new_y][new_x]
                if target is None or target.color != self.color:
                    moves.append((new_x, new_y))
        
        # Рокировка
        if not self.has_moved and not board.is_in_check(self.color):
            # Короткая рокировка (королевская сторона)
            if self._can_castle_kingside(board):
                moves.append((6, self.y))  # Король на g1/g8
            
            # Длинная рокировка (ферзевая сторона)
            if self._can_castle_queenside(board):
                moves.append((2, self.y))  # Король на c1/c8
                
        return moves
    
    def _can_castle_kingside(self, board):
        #Проверка возможности короткой рокировки
        # Проверяем, что ладья на месте и не двигалась
        rook = board.grid[self.y][7]
        if rook is None or rook.__class__.__name__ != "Rook" or rook.has_moved:
            return False
        
        # Проверяем, что клетки между королем и ладьей пустые
        for x in range(self.x + 1, 7):
            if board.grid[self.y][x] is not None:
                return False
        
        # Проверяем, что король не проходит через битое поле и не находится под шахом
        # Проверяем клетку f1/f8
        if board.is_square_attacked((5, self.y), self.color):
            return False
        # Проверяем клетку g1/g8
        if board.is_square_attacked((6, self.y), self.color):
            return False
            
        return True
    
    def _can_castle_queenside(self, board):
        #Проверка возможности длинной рокировки
        # Проверяем, что ладья на месте и не двигалась
        rook = board.grid[self.y][0]
        if rook is None or rook.__class__.__name__ != "Rook" or rook.has_moved:
            return False
        
        # Проверяем, что клетки между королем и ладьей пустые
        for x in range(1, self.x):
            if board.grid[self.y][x] is not None:
                return False
        
        # Проверяем, что король не проходит через битое поле и не находится под шахом
        # Проверяем клетку d1/d8
        if board.is_square_attacked((3, self.y), self.color):
            return False
        # Проверяем клетку c1/c8
        if board.is_square_attacked((2, self.y), self.color):
            return False
            
        return True