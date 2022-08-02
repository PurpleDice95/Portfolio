import numpy as np
import pygame
from Classes import *

# params
grid_size = (90, 80)
speed = 10
dis_weight = 0.5

pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Arial", 30)
Clock = pygame.time.Clock()
running = True
set_all_wall = True
start_set = False
Solvable = [False, False]
Queue = []
FinishedQueue = []
screen = pygame.display.set_mode((grid_size[0]*10, grid_size[1]*10))
pygame.display.set_caption("PathFinder")
grid = np.empty(grid_size, dtype=object)
for i in range(grid.shape[0]):
    for j in range(grid.shape[1]):
        grid[i, j] = Space((i, j))

for i in range(0, grid_size[0]):
    for j in range(0, grid_size[1]):
        grid[i, j] = Wall((i, j))
for i in range(1, grid_size[0]-1):
    for j in range(1, grid_size[1]-1):
        grid[i, j] = Space((i, j))

while running:
    screen.fill((0, 0, 0))
    cursor_pos = cursor_x, cursor_y = pygame.mouse.get_pos()
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            pygame.draw.rect(screen, grid[row, col].color, (row * 10, col * 10, 10, 10))
    if Start.Start:
        pygame.draw.rect(screen, (255, 0, 0), (Start.Start[0].pos_x * 10, Start.Start[0].pos_y * 10, 10, 10))
    for row in range(grid.shape[0]):
        pygame.draw.line(screen, (0, 0, 0), (row * 10, 0), (row * 10, grid_size[1] * 10), 1)
    for col in range(grid.shape[1]):
        pygame.draw.line(screen, (0, 0, 0), (0, col*10), (grid_size[0]*10, col*10), 1)

    if Solvable[0] and Solvable[1]:
        for row in range(grid.shape[0]):
            for col in range(grid.shape[1]):
                if isinstance(grid[row, col], Node) or isinstance(grid[row, col], Path):
                    grid[row, col] = Space((row, col))

        Queue = []
        FinishedQueue = []
        Start.Start[0].euclid_dis = EuclidDisBtwn(Start.Start[0], End.End[0])
        Queue.append(Start.Start[0])
        i = 0
        while Queue:

            node = Queue[0]
            right_node = grid[node.pos_x + 1, node.pos_y]
            left_node = grid[node.pos_x - 1, node.pos_y]
            down_node = grid[node.pos_x, node.pos_y + 1]
            up_node = grid[node.pos_x, node.pos_y - 1]

            # print(node.distance, node.prev_node)
            # Place new nodes
            if isinstance(right_node, Space):
                grid[node.pos_x + 1, node.pos_y] = Node((node.pos_x + 1, node.pos_y), node.distance, node)
                Queue.append(grid[node.pos_x + 1, node.pos_y])

            if isinstance(left_node, Space):
                grid[node.pos_x - 1, node.pos_y] = Node((node.pos_x - 1, node.pos_y), node.distance, node)
                Queue.append(grid[node.pos_x - 1, node.pos_y])

            if isinstance(down_node, Space):
                grid[node.pos_x, node.pos_y + 1] = Node((node.pos_x, node.pos_y + 1), node.distance, node)
                Queue.append(grid[node.pos_x, node.pos_y + 1])

            if isinstance(up_node, Space):
                grid[node.pos_x, node.pos_y - 1] = Node((node.pos_x, node.pos_y - 1), node.distance, node)
                Queue.append(grid[node.pos_x, node.pos_y - 1])

            # Modify adjacent existing nodes
            if isinstance(right_node, Node) and right_node not in FinishedQueue and right_node.distance > node.distance + 1:
                Queue.remove(grid[node.pos_x + 1, node.pos_y])
                grid[node.pos_x + 1, node.pos_y].distance = node.distance + 1
                grid[node.pos_x + 1, node.pos_y].prev_node = node
                Queue.append(grid[node.pos_x + 1, node.pos_y])

            if isinstance(left_node, Node) and left_node not in FinishedQueue and left_node.distance > node.distance + 1:
                Queue.remove(grid[node.pos_x - 1, node.pos_y])
                grid[node.pos_x - 1, node.pos_y].distance = node.distance + 1
                grid[node.pos_x - 1, node.pos_y].prev_node = node
                Queue.append(grid[node.pos_x - 1, node.pos_y])

            if isinstance(down_node, Node) and down_node not in FinishedQueue and down_node.distance > node.distance + 1:
                Queue.remove(grid[node.pos_x, node.pos_y + 1])
                grid[node.pos_x, node.pos_y + 1].distance = node.distance + 1
                grid[node.pos_x, node.pos_y + 1].prev_node = node
                Queue.append(grid[node.pos_x, node.pos_y + 1])

            if isinstance(up_node, Node) and up_node not in FinishedQueue and up_node.distance > node.distance + 1:
                Queue.remove(grid[node.pos_x, node.pos_y - 1])
                grid[node.pos_x, node.pos_y - 1].distance = node.distance + 1
                grid[node.pos_x, node.pos_y - 1].prev_node = node
                Queue.append(grid[node.pos_x, node.pos_y - 1])

            # Check for end node
            if isinstance(right_node, End):
                ColorPath(node, grid)
                break

            if isinstance(left_node, End):
                ColorPath(node, grid)
                break

            if isinstance(down_node, End):
                ColorPath(node, grid)
                break

            if isinstance(up_node, End):
                ColorPath(node, grid)
                break

            Queue.remove(node)
            Queue.sort(key=lambda x: x.distance*(1-dis_weight)*2 + x.euclid_dis*dis_weight*2)
            FinishedQueue.append(node)

            if i % speed == 0:
                for row in range(grid.shape[0]):
                    for col in range(grid.shape[1]):
                        pygame.draw.rect(screen, grid[row, col].color, (row * 10, col * 10, 10, 10))
                for row in range(grid.shape[0]):
                    pygame.draw.line(screen, (0, 0, 0), (row * 10, 0), (row * 10, grid_size[1] * 10), 1)
                for col in range(grid.shape[1]):
                    pygame.draw.line(screen, (0, 0, 0), (0, col * 10), (grid_size[0] * 10, col * 10), 1)

                pygame.event.pump()
                pygame.display.update()
            i += 1

        Solvable = [False, False]

    if pygame.mouse.get_pressed(3)[0]:
        grid[cursor_x//10, cursor_y//10] = Wall((cursor_x//10, cursor_y//10))
    if pygame.mouse.get_pressed(3)[2]:
        grid[cursor_x // 10, cursor_y // 10] = Space((cursor_x // 10, cursor_y // 10))

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 2 and not start_set:
                grid[cursor_x // 10, cursor_y // 10] = Start((cursor_x // 10, cursor_y // 10), grid)
                start_set = True
                Solvable[0] = True
            elif event.button == 2 and start_set:
                grid[cursor_x // 10, cursor_y // 10] = End((cursor_x // 10, cursor_y // 10), grid)
                start_set = False
                Solvable[1] = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                Start.Start = []
                End.End = []
                if set_all_wall:
                    for i in range(grid.shape[0]):
                        for j in range(grid.shape[1]):
                            grid[i, j] = Wall((i, j))
                    set_all_wall = False

                elif not set_all_wall:
                    for i in range(grid.shape[0]):
                        for j in range(grid.shape[1]):
                            grid[i, j] = Space((i, j))
                    for i in range(0, grid_size[0]):
                        for j in range(0, grid_size[1]):
                            grid[i, j] = Wall((i, j))
                    for i in range(1, grid_size[0] - 1):
                        for j in range(1, grid_size[1] - 1):
                            grid[i, j] = Space((i, j))
                    set_all_wall = True

            elif event.unicode.isnumeric():
                dis_weight = int(event.unicode)*0.1
                screen.blit(font.render(f"{dis_weight}", True, (0, 0, 0)), (20, 20))

        if event.type == pygame.QUIT:
            running = False

    Clock.tick(1000)
    pygame.display.update()
