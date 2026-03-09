import pygame
import sys
import importlib
from board import Board
from piece import Piece

WIDTH, HEIGHT = 600, 600
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Эти константы отвечают за цвета,
# можете их менять
WHITE = (238, 238, 210) # Цвет белых клеток
BLACK = (118, 150, 86) # Цвет черных клеток
SELECTED_COLOR = (255, 255, 0) # Цвет выбранной клетки
FONT_COLOR = (0, 0, 0) # Цвет фигур


COL_MAP_INV = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
def parse_move(move):
    if isinstance(move, tuple) or isinstance(move, list):
        if len(move) == 2:
            return move[0], move[1]
    
    if isinstance(move, str) and len(move) >= 2:
        col_char = move[0]
        row_char = move[1]
        
        x = COL_MAP_INV.get(col_char)
        try:
            y = int(row_char) - 1
        except ValueError:
            return None

        if x is not None and 0 <= y < 8:
            return x, y
            
    return None

def safe_import(module_name, class_name):
    try:
        module = importlib.import_module(module_name)
        return getattr(module, class_name)
    except (ImportError, AttributeError):
        return None

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Шахматы")
    
    try:
        font = pygame.font.SysFont("segoeuisymbol", 50) 
    except:
        font = pygame.font.SysFont("arial", 50)

    board = Board()
    
    piece_classes = {
        'Pawn': safe_import('pawn', 'Pawn'),
        'Rook': safe_import('rook', 'Rook'),
        'Knight': safe_import('knight', 'Knight'),
        'Bishop': safe_import('bishop', 'Bishop'),
        'Queen': safe_import('queen', 'Queen'),
        'King': safe_import('king', 'King'),
    }

    board.new_game(piece_classes)

    selected_piece = None
    possible_moves = []

    running = True
    while running:
        screen.fill(WHITE)
        
        for row in range(ROWS):
            for col in range(COLS):
                color = WHITE if (row + col) % 2 == 0 else BLACK
                rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(screen, color, rect)

        if selected_piece:
            py_row_sel = 7 - selected_piece.y
            py_col_sel = selected_piece.x
            
            sel_rect = pygame.Rect(py_col_sel * SQUARE_SIZE, py_row_sel * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, SELECTED_COLOR, sel_rect, 4) 

            for move in possible_moves:
                coords = parse_move(move)
                if coords:
                    mx, my = coords
                    py_row_move = 7 - my
                    py_col_move = mx
                    
                    center_x = py_col_move * SQUARE_SIZE + SQUARE_SIZE // 2
                    center_y = py_row_move * SQUARE_SIZE + SQUARE_SIZE // 2
                    pygame.draw.circle(screen, (100, 100, 100), (center_x, center_y), SQUARE_SIZE // 6)

        for logic_y in range(8):
            for logic_x in range(8):
                piece = board.grid[logic_y][logic_x]
                if piece:
                    screen_x = logic_x * SQUARE_SIZE
                    screen_y = (7 - logic_y) * SQUARE_SIZE
                    
                    piece_text = str(piece)
                    text_surface = font.render(piece_text, True, FONT_COLOR)
                    
                    text_rect = text_surface.get_rect(center=(screen_x + SQUARE_SIZE // 2, screen_y + SQUARE_SIZE // 2))
                    screen.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    try:
                        board.new_game(piece_classes)
                        selected_piece = None
                        possible_moves = []
                        print("Новая игра начата")
                    except Exception as e:
                        print(f"Ошибка при создании новой игры: {e}")

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click
                    pos = pygame.mouse.get_pos()
                    col_idx = pos[0] // SQUARE_SIZE
                    row_idx = pos[1] // SQUARE_SIZE
                    
                    logic_x = col_idx
                    logic_y = 7 - row_idx
                    
                    clicked_move = None
                    for move in possible_moves:
                        coords = parse_move(move)
                        if coords and coords == (logic_x, logic_y):
                            clicked_move = coords
                            break
                    
                    if selected_piece and clicked_move:
                        board.grid[selected_piece.y][selected_piece.x] = None
                        
                        target_x, target_y = clicked_move
                        
                        selected_piece.move(target_x, target_y)
                        
                        board.grid[target_y][target_x] = selected_piece
                        
                        selected_piece = None
                        possible_moves = []
                        
                    else:
                        if 0 <= logic_x < 8 and 0 <= logic_y < 8:
                            clicked_piece = board.grid[logic_y][logic_x]
                            if clicked_piece:
                                selected_piece = clicked_piece
                                try:
                                    possible_moves = selected_piece.get_possible_moves(board)
                                except TypeError:
                                    possible_moves = selected_piece.get_possible_moves()
                                    
                                print(f"Выбрана фигура: {selected_piece} на позиции ({logic_x}, {logic_y}). Возможные ходы: {possible_moves}")
                                pass
                            else:
                                selected_piece = None
                                possible_moves = []

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
