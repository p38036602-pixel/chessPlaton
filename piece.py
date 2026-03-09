class Piece:
    def __init__(self, color, x, y):
        if color not in ('white', 'black'):
            raise ValueError("Цвет должен быть 'white' или 'black'")
        if not (0 <= x < 8 and 0 <= y < 8):
            raise ValueError("Координаты должны быть в диапазоне от 0 до 7")
        self.color = color
        self.x = x
        self.y = y
        self.has_moved = False

    def move(self, new_x, new_y):
        if not (0 <= new_x < 8 and 0 <= new_y < 8):
            raise ValueError("Координаты должны быть в диапазоне от 0 до 7")
        self.x = new_x
        self.y = new_y
        self.has_moved = True

    def __str__(self):
        return "?"