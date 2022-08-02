import math
import pygame


class Wall:
    def __init__(self, pos):
        self.pos = self.pos_x, self.pos_y = pos
        self.color = (0, 0, 255)


class Space:
    def __init__(self, pos):
        self.pos = self.pos_x, self.pos_y = pos
        self.color = (0, 255, 0)


class Start:
    Start = []

    def __init__(self, pos, grid):
        self.pos = self.pos_x, self.pos_y = pos
        self.color = (255, 0, 0)
        self.distance = 0
        self.euclid_dis = None
        self.prev_node = None
        if len(self.Start) > 0:
            grid[self.Start[0].pos_x, self.Start[0].pos_y] = Space((self.Start[0].pos_x, self.Start[0].pos_y))
            self.Start.pop(0)
        self.Start.append(self)


class End:
    End = []

    def __init__(self, pos, grid):
        self.pos = self.pos_x, self.pos_y = pos
        self.color = (255, 0, 255)
        if len(self.End) > 0:
            grid[self.End[0].pos_x, self.End[0].pos_y] = Space((self.End[0].pos_x, self.End[0].pos_y))
            self.End.pop(0)
        self.End.append(self)


class Node:
    def __init__(self, pos, path_len_expanding_node, prev_node):
        self.pos = self.pos_x, self.pos_y = pos
        self.color = (255, 255, 255)
        self.distance = path_len_expanding_node + 1
        self.euclid_dis = EuclidDisBtwn(self, End.End[0])
        self.prev_node = prev_node


class Path:
    def __init__(self, pos):
        self.pos = self.pos_x, self.pos_y = pos
        self.color = (0, 0, 0)


def ColorPath(node, grid):
    shortest_path = [node]
    while True:
        if node.prev_node is not None:
            shortest_path.append(node.prev_node)
            node = node.prev_node
        else:
            break
    print(len(shortest_path))
    for path_node in shortest_path:
        grid[path_node.pos_x, path_node.pos_y] = Path((path_node.pos_x, path_node.pos_y))



def EuclidDisBtwn(node, end):
    return math.sqrt(((node.pos_x - end.pos_x) ** 2) + ((node.pos_y - end.pos_y) ** 2))
