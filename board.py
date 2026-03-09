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