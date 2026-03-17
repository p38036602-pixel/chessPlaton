class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]

    def place_piece(self, piece):
        if not (0 <= piece.x < 8 and 0 <= piece.y < 8):
            raise ValueError("Фигура вне доски")
        self.grid[piece.y][piece.x] = piece

    def new_game(self, piece_classes):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        
        if piece_classes.get('Pawn'):
            for i in range(8):
                self.place_piece(piece_classes['Pawn']("white", i, 1))
                self.place_piece(piece_classes['Pawn']("black", i, 6))
        
        non_pawn_pieces = [
            ('Rook', [0, 7]),
            ('Knight', [1, 6]),
            ('Bishop', [2, 5]),
            ('Queen', [3]),
            ('King', [4])
        ]

        for p_name, files in non_pawn_pieces:
            cls = piece_classes.get(p_name)
            if cls:
                for f in files:
                    self.place_piece(cls("white", f, 0))
                    self.place_piece(cls("black", f, 7))

    def move_piece(self, from_x, from_y, to_x, to_y):
        #Перемещает фигуру с проверкой на рокировку
        piece = self.grid[from_y][from_x]
        if piece is None:
            return False
        
        # Проверяем, является ли ход рокировкой
        if piece.__class__.__name__ == "King" and abs(to_x - from_x) == 2:
            # Рокировка
            return self._handle_castling(piece, to_x, to_y)
        
        # Обычный ход
        self.grid[from_y][from_x] = None
        self.grid[to_y][to_x] = piece
        piece.x, piece.y = to_x, to_y
        piece.has_moved = True
        return True

    def _handle_castling(self, king, to_x, to_y):
        #Обрабатывает рокировку#
        # Определяем направление рокировки
        if to_x == 6:  # Короткая рокировка
            rook = self.grid[to_y][7]
            if rook and rook.__class__.__name__ == "Rook" and not rook.has_moved:
                # Перемещаем короля
                self.grid[king.y][king.x] = None
                self.grid[to_y][to_x] = king
                king.x, king.y = to_x, to_y
                king.has_moved = True
                
                # Перемещаем ладью
                self.grid[to_y][7] = None
                self.grid[to_y][5] = rook  # Ладья на f1/f8
                rook.x, rook.y = 5, to_y
                rook.has_moved = True
                return True
                
        elif to_x == 2:  # Длинная рокировка
            rook = self.grid[to_y][0]
            if rook and rook.__class__.__name__ == "Rook" and not rook.has_moved:
                # Перемещаем короля
                self.grid[king.y][king.x] = None
                self.grid[to_y][to_x] = king
                king.x, king.y = to_x, to_y
                king.has_moved = True
                
                # Перемещаем ладью
                self.grid[to_y][0] = None
                self.grid[to_y][3] = rook  # Ладья на d1/d8
                rook.x, rook.y = 3, to_y
                rook.has_moved = True
                return True
        
        return False

    def is_in_check(self, color):
        #Проверяет, находится ли король указанного цвета под шахом
        # Находим короля
        king_pos = None
        for y in range(8):
            for x in range(8):
                piece = self.grid[y][x]
                if piece and piece.__class__.__name__ == "King" and piece.color == color:
                    king_pos = (x, y)
                    break
            if king_pos:
                break
        
        if not king_pos:
            return False
        
        # Проверяем, атакована ли клетка короля
        return self.is_square_attacked(king_pos, color)

    def is_square_attacked(self, square, defending_color):
        #Проверяет, атакована ли клетка фигурами противника"""
        target_x, target_y = square
        attacking_color = "black" if defending_color == "white" else "white"
        
        for y in range(8):
            for x in range(8):
                piece = self.grid[y][x]
                if piece and piece.color == attacking_color:
                    # Получаем все возможные ходы фигуры (без проверки на шах)
                    if piece.__class__.__name__ == "Pawn":
                        # Особый случай для пешки (бьет по диагонали)
                        if self._is_pawn_attacking(piece, target_x, target_y):
                            return True
                    else:
                        moves = piece.get_possible_moves(self)
                        if (target_x, target_y) in moves:
                            return True
        return False

    def _is_pawn_attacking(self, pawn, target_x, target_y):
        #Проверяет, атакует ли пешка указанную клетку"""
        direction = 1 if pawn.color == "white" else -1
        # Пешка атакует по диагонали вперед
        return (target_y == pawn.y + direction and 
                abs(target_x - pawn.x) == 1)

    def __str__(self):
        rows = []
        for row_idx in range(7, -1, -1):
            row = self.grid[row_idx]
            line = ""
            for cell in row:
                if cell is None:
                    line += ". "
                else:
                    line += str(cell) + " "
            rows.append(line.strip())
        return "\n".join(rows)