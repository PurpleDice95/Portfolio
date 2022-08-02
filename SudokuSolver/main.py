import numpy as np
import copy
import pygame

# Class for position
class Pos:
    def __init__(self, pos_x, pos_y):
        self.pos = self.pos_x, self.pos_y = pos_x, pos_y

        # coords of all positions in the same cage
        self.cage = (self.pos_x//3, self.pos_y//3)
        self.cage_coords = []
        for i in range(self.cage[0]*3, self.cage[0]*3+3):
            for j in range(self.cage[1]*3, self.cage[1]*3+3):
                self.cage_coords.append((i, j))

        # coods of all positions in the same row/col
        self.row_coords = [(x, self.pos_y) for x in range(9)]
        self.col_coords = [(self.pos_x, y) for y in range(9)]

    # elements in above positions for any grid (temp_grid)
    def set_elements(self, temp_grid):
        self.cage_elements = [temp_grid[y, x] for x, y in self.cage_coords]
        self.row_elements = [temp_grid[y, x] for x, y in self.row_coords]
        self.col_elements = [temp_grid[y, x] for x, y in self.col_coords]

    # is num a valid entry in temp_grid
    def valid_number(self, num, temp_grid):
        self.set_elements(temp_grid)
        if num in self.cage_elements or num in self.row_elements or num in self.col_elements or not 1 <= num <= 9:
            return False
        else:
            return True

    # is the position on temp_grid empty
    def is_empty(self, temp_grid):
        return True if temp_grid[self.pos_y, self.pos_x] == 0 else False

# recursive brute force
def solve(temp_grid):
    global index, empty_squares
    # base case - solved
    if index > len(empty_squares)-1:
        return temp_grid
    else:
        curr_grid = copy.deepcopy(temp_grid)

        # draw
        screen.fill((255, 255, 255))
        draw_grid(curr_grid)
        pygame.display.update()
        # time.sleep(0.01)

        # check each num
        for num in range(1, 10):
            if empty_squares[index].valid_number(num, curr_grid):
                curr_grid[empty_squares[index].pos_y, empty_squares[index].pos_x] = num
                index += 1
                new_grid = solve(curr_grid)
                index -= 1
                if new_grid is not None:
                    return new_grid
        # no valid solution
        return None


def draw_grid(Grid):
    for i in range(1, 9):
        pygame.draw.line(screen, (0, 0, 0), (0, i*64), (577, i*64), 2)
        pygame.draw.line(screen, (0, 0, 0), (i * 64, 0), (i * 64, 577), 2)
    for i in range(3):
        pygame.draw.line(screen, (0, 0, 0), (0, i * 64*3), (577, i * 64*3), 5)
        pygame.draw.line(screen, (0, 0, 0), (i * 64*3, 0), (i * 64*3, 577), 5)

    # draw numbers
    for i in range(9):
        for j in range(9):
            screen.blit(font1.render(str(Grid[j, i] if Grid[j, i] != 0 else ""), True, (0, 0, 0)), (i*64+20, j*64+7))


def writeGrid(y, x, n):
    global grid
    grid[y, x] = n


# pygame init
pygame.init()
pygame.font.init()
font1 = pygame.font.SysFont("Arial", 48)
Clock = pygame.time.Clock()
screen = pygame.display.set_mode((576, 576))
running = True

# default grid
grid = np.array([[0, 0, 9, 0, 0, 1, 0, 0, 0],
                 [0, 0, 0, 4, 0, 0, 0, 0, 1],
                 [8, 7, 0, 0, 0, 0, 3, 0, 0],
                 [0, 2, 0, 0, 0, 8, 0, 0, 0],
                 [0, 0, 5, 0, 0, 0, 6, 0, 7],
                 [0, 8, 3, 0, 9, 0, 0, 5, 0],
                 [7, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 3, 0, 0, 0, 2],
                 [0, 0, 2, 6, 0, 5, 0, 0, 9]])


while running:
    screen.fill((255, 255, 255))
    cursor_pos = pygame.mouse.get_pos()
    cursor_grid_pos = Pos(cursor_pos[0]//64, cursor_pos[1]//64)

    # highlight
    highlighted = set(cursor_grid_pos.cage_coords + cursor_grid_pos.row_coords + cursor_grid_pos.col_coords)
    if pygame.mouse.get_focused():
        for elem_x, elem_y in highlighted:
            highlight = pygame.Surface((64, 64))
            highlight.set_alpha(64)
            highlight.fill((0, 0, 0))
            screen.blit(highlight, (elem_x*64, elem_y*64))
        screen.blit(highlight, (cursor_grid_pos.pos_x*64, cursor_grid_pos.pos_y*64))

    draw_grid(grid)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Queue
                empty_squares = []
                for i in range(9):
                    for j in range(9):
                        temp_pos = Pos(j, i)
                        if temp_pos.is_empty(grid):
                            empty_squares.append(temp_pos)
                index = 0
                grid = solve(grid)

            elif event.key == pygame.K_TAB:
                grid = np.zeros((9, 9), dtype=int)

            elif event.unicode.isnumeric() and 1 <= int(event.unicode) <= 9 and pygame.mouse.get_focused():
                grid[cursor_grid_pos.pos_y, cursor_grid_pos.pos_x] = int(event.unicode)

        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()


