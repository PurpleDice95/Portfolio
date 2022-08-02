import pygame
import numpy as np
import copy


class Empty:
    def __str__(self):
        return " "

    def __init__(self, pos):
        self.pos = self.pos_x, self.pos_y = pos
        self.symbol = None

    def draw(self):
        pass


class X:
    def __str__(self):
        return "X"

    def __init__(self, pos):
        self.pos = self.pos_x, self.pos_y = pos
        self.symbol = -1
        self.color = (0, 0, 0)

    def draw(self):
        global screen
        pygame.draw.line(screen, self.color, (self.pos_y*200 + 170, self.pos_x*200 + 170),
                         (self.pos_y*200 + 30, self.pos_x*200 + 30), 20)
        pygame.draw.line(screen, self.color, (self.pos_y * 200 + 30, self.pos_x * 200 + 170),
                         (self.pos_y * 200 + 170, self.pos_x * 200 + 30), 20)


class O:
    def __str__(self):
        return "O"

    def __init__(self, pos):
        self.pos = self.pos_x, self.pos_y = pos
        self.symbol = 1
        self.color = (0, 0, 0)

    def draw(self):
        global screen
        pygame.draw.circle(screen, self.color, (self.pos_y*200+100, self.pos_x*200+100), 80, 12)


def CheckWin(temp_grid):
    for i in range(3):
        if temp_grid[i, 0].symbol == temp_grid[i, 1].symbol and temp_grid[i, 1].symbol == temp_grid[i, 2].symbol and temp_grid[i, 0].symbol is not None:
            return temp_grid[i, 0].symbol
        elif temp_grid[0, i].symbol == temp_grid[1, i].symbol and temp_grid[1, i].symbol == temp_grid[2, i].symbol and temp_grid[0, i].symbol is not None:
            return temp_grid[0, i].symbol
    if temp_grid[0, 0].symbol == temp_grid[1, 1].symbol and temp_grid[1, 1].symbol == temp_grid[2, 2].symbol and temp_grid[0, 0].symbol is not None:
        return temp_grid[0, 0].symbol
    elif temp_grid[2, 0].symbol == temp_grid[1, 1].symbol and temp_grid[1, 1].symbol == temp_grid[0, 2].symbol and temp_grid[2, 0].symbol is not None:
        return temp_grid[2, 0].symbol
    for i in range(temp_grid.shape[0]):
        for j in range(temp_grid.shape[1]):
            if temp_grid[i, j].symbol is None:
                return None
    return 0


def ColorWinningLine(temp_grid):
    print("Hi")
    for i in range(3):
        if temp_grid[i, 0].symbol == temp_grid[i, 1].symbol and temp_grid[i, 1].symbol == temp_grid[i, 2].symbol and temp_grid[i, 0].symbol is not None:
            temp_grid[i, 0].color = (255, 0, 0)
            temp_grid[i, 1].color = (255, 0, 0)
            temp_grid[i, 2].color = (255, 0, 0)
        elif temp_grid[0, i].symbol == temp_grid[1, i].symbol and temp_grid[1, i].symbol == temp_grid[2, i].symbol and temp_grid[0, i].symbol is not None:
            temp_grid[0, i].color = (255, 0, 0)
            temp_grid[1, i].color = (255, 0, 0)
            temp_grid[2, i].color = (255, 0, 0)
    if temp_grid[0, 0].symbol == temp_grid[1, 1].symbol and temp_grid[1, 1].symbol == temp_grid[2, 2].symbol and temp_grid[0, 0].symbol is not None:
        temp_grid[0, 0].color = (255, 0, 0)
        temp_grid[1, 1].color = (255, 0, 0)
        temp_grid[2, 2].color = (255, 0, 0)
    elif temp_grid[2, 0].symbol == temp_grid[1, 1].symbol and temp_grid[1, 1].symbol == temp_grid[0, 2].symbol and temp_grid[2, 0].symbol is not None:
        temp_grid[0, 2].color = (255, 0, 0)
        temp_grid[1, 1].color = (255, 0, 0)
        temp_grid[2, 0].color = (255, 0, 0)
    for i in range(temp_grid.shape[0]):
        for j in range(temp_grid.shape[1]):
            if temp_grid[i, j].symbol is None:
                return None
    for i in range(temp_grid.shape[0]):
        for j in range(temp_grid.shape[1]):
            temp_grid[i, j].color = (255, 255, 0)

def isGridEmpty(temp_grid):
    for i in range(3):
        for j in range(3):
            if temp_grid[i, j].symbol is None:
                return False
    return True

# Minmax algo
def MAX(curr_state):
    if CheckWin(curr_state) is not None:
        return CheckWin(curr_state)

    possible_moves = []
    for i in range(curr_state.shape[0]):
        for j in range(curr_state.shape[1]):
            if isinstance(curr_state[i, j], Empty):
                possible_moves.append(curr_state[i, j])

    value = -2
    for move in possible_moves:
        next_state = copy.deepcopy(curr_state)
        next_state[move.pos_x, move.pos_y] = O((move.pos_x, move.pos_y))
        new_value = MIN(next_state)

        if new_value > value:
            value = new_value
    return value



def MIN(curr_state):
    if CheckWin(curr_state) is not None:
        return CheckWin(curr_state)

    possible_moves = []
    for i in range(curr_state.shape[0]):
        for j in range(curr_state.shape[1]):
            if isinstance(curr_state[i, j], Empty):
                possible_moves.append(curr_state[i, j])

    value = 2
    for move in possible_moves:
        next_state = copy.deepcopy(curr_state)
        next_state[move.pos_x, move.pos_y] = X((move.pos_x, move.pos_y))
        new_value = MAX(next_state)

        if new_value < value:
            value = new_value
    return value

# Rendering
def DrawWindow():
    global screen
    screen.fill((255, 255, 255))
    for i in range(2, 6, 2):
        pygame.draw.line(screen, (0, 0, 0), (i*100, 0), (i*100, 600), 5)
        pygame.draw.line(screen, (0, 0, 0), (0, i * 100), (600, i * 100), 5)
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            grid[i, j].draw()


pygame.init()
running = True
Clock = pygame.time.Clock()
screen = pygame.display.set_mode((600, 600))


grid = np.empty((3, 3), dtype=object)
for i in range(grid.shape[0]):
    for j in range(grid.shape[1]):
        grid[i, j] = Empty((i, j))

# Main loop
while running:
    DrawWindow()
    cursor_pos = cursor_pos_x, cursor_pos_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and isinstance(grid[cursor_pos_y//200, cursor_pos_x//200], Empty):
            grid[cursor_pos_y//200, cursor_pos_x//200] = X((cursor_pos_y//200, cursor_pos_x//200))
            moves = []
            for i in range(grid.shape[0]):
                for j in range(grid.shape[1]):
                    if isinstance(grid[i, j], Empty):
                        moves.append(grid[i, j])
            valued_state = None
            max_value = -2
            for move in moves:
                next_state = copy.deepcopy(grid)
                next_state[move.pos_x, move.pos_y] = O((move.pos_x, move.pos_y))
                new_value = MIN(next_state)
                if new_value > max_value:
                    max_value = new_value
                    valued_state = copy.deepcopy(next_state)

            if CheckWin(grid) is None:
                grid = copy.deepcopy(valued_state)
                DrawWindow()
            if CheckWin(grid) is not None:
                ColorWinningLine(grid)
                DrawWindow()


    Clock.tick(60)
    pygame.display.update()