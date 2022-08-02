import pandas as pd
import numpy as np
import pygame


class EmptySquare:
    def __init__(self):
        self.side = None

    def __str__(self):
        return "|_|"

    def draw(self, win):
        pass
    def place(self, board):
        pass


class Piece:
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    to_int_dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    side = None
    sprite = None
    picked = None
    enpassant_pawns = []
    interacting_w_UI = False
    interacting_w_promote_UI = False
    promoting_side = None
    promoting_piece = None

    def place(self, board):
        board.loc[self.posY, self.posX] = self

    def draw(self, win):
        if not self.picked:
            win.blit(self.sprite, ((self.to_int_dict[self.posX]*100)+12, (self.posY*100)+12))

    def in_diagonal(self, new_pos, board, diags):
        for diag in diags:
            if board.loc[new_pos[1], new_pos[0]] in diag and self in diag:
                return True, diag
        return False, None

    def piece_in_way(self, new_pos, board):
        numpy_board = board.to_numpy()
        diags = [numpy_board[::-1, :].diagonal(i) for i in range(-numpy_board.shape[0] + 1, numpy_board.shape[1])]
        diags.extend(numpy_board.diagonal(i) for i in range(numpy_board.shape[1] - 1, -numpy_board.shape[0], -1))
        diags = [n.tolist() for n in diags]

        in_diag = self.in_diagonal(new_pos, board, diags)
        if new_pos[0] == self.posX:
            for i in range(min(self.posY, new_pos[1]) + 1, max(self.posY, new_pos[1])):
                if not isinstance(board.loc[i, self.posX], EmptySquare):
                    return True

        elif new_pos[1] == self.posY:
            for i in range(min(self.to_int_dict[self.posX], self.to_int_dict[new_pos[0]]) + 1, max(self.to_int_dict[self.posX], self.to_int_dict[new_pos[0]])):
                if not isinstance(board.iloc[self.posY, i], EmptySquare):
                    return True

        elif in_diag[0]:
            squares = in_diag[1][min(in_diag[1].index(board.loc[new_pos[1], new_pos[0]]), in_diag[1].index(self))+1:max(in_diag[1].index(board.loc[new_pos[1], new_pos[0]]), in_diag[1].index(self))]
            for square in squares:
                if not isinstance(square, EmptySquare):
                    return True
        return False

    def is_not_blocked(self, new_pos, board):
        if ((board.loc[new_pos[1], new_pos[0]].side != self.side) and
                not self.piece_in_way(new_pos, board)):
            return True
        return False

    def move(self, new_pos, board):
        board.loc[self.posY, self.posX] = EmptySquare()
        self.posX, self.posY = new_pos
        board.loc[new_pos[1], new_pos[0]] = self

        for pawn in Piece.enpassant_pawns:
            if self.side != pawn.side:
                pawn.enpassant = False


class Pawn(Piece):

    def __str__(self):
        return ""

    def __init__(self, pos, side):
        self.posX, self.posY = pos
        self.side = side
        self.moved_once = False
        self.picked = False
        self.enpassant = False
        self.can_enpassant = False
        self.self_destruct = False
        if self.side > 0:
            sprite = pygame.image.load("Sprites/pawn1.png")
            self.sprite = pygame.transform.scale(sprite, (75, 75))
        else:
            sprite = pygame.image.load("Sprites/pawn.png")
            self.sprite = pygame.transform.scale(sprite, (75, 75))

    def is_not_blocked(self, new_pos, board):
        if ((not board.loc[new_pos[1], new_pos[0]].side) and
                not self.piece_in_way(new_pos, board)):
            return True
        return False

    def is_valid_move(self, new_pos, board):
        if new_pos[0] == self.posX:
            if self.is_not_blocked(new_pos, board):
                if new_pos[1] == self.posY + self.side:
                    return True

                elif (new_pos[1] == self.posY + (self.side*2)) and not self.moved_once:
                    self.enpassant = True
                    Piece.enpassant_pawns.append(self)
                    if self.to_int_dict[new_pos[0]]+1 <= 7:
                        if isinstance(board.loc[new_pos[1], self.letters[self.to_int_dict[new_pos[0]]+1]], Pawn):
                            board.loc[new_pos[1], self.letters[self.to_int_dict[new_pos[0]]+1]].can_enpassant = True
                    if self.to_int_dict[new_pos[0]]-1 >= 0:
                        if isinstance(board.loc[new_pos[1], self.letters[self.to_int_dict[new_pos[0]]-1]], Pawn):
                            board.loc[new_pos[1], self.letters[self.to_int_dict[new_pos[0]]-1]].can_enpassant = True
                    return True
        elif ((((self.to_int_dict[new_pos[0]] == self.to_int_dict[self.posX] + 1) or
                (self.to_int_dict[new_pos[0]] == self.to_int_dict[self.posX] - 1))
              and (new_pos[1] == self.posY + self.side))
              and board.loc[new_pos[1], new_pos[0]].side == (self.side * -1)):
            return True
        elif ((((self.to_int_dict[new_pos[0]] == self.to_int_dict[self.posX] + 1) or
                (self.to_int_dict[new_pos[0]] == self.to_int_dict[self.posX] - 1))
               and (new_pos[1] == self.posY + self.side))
               and (isinstance(board.loc[self.posY, new_pos[0]], Pawn)
                and  board.loc[self.posY, new_pos[0]].enpassant
                and self.can_enpassant)):
            board.loc[self.posY, new_pos[0]] = EmptySquare()
            return True
        return False

    def can_promote(self):
        if (self.posY == 7 and self.side == 1) or (self.posY == 0 and self.side == -1):
            return True
        return False

    def move(self, new_pos, board):
        board.loc[self.posY, self.posX] = EmptySquare()
        self.posX, self.posY = new_pos
        board.loc[new_pos[1], new_pos[0]] = self
        self.moved_once = True
        for pawn in Piece.enpassant_pawns:
            if self.side != pawn.side:
                pawn.enpassant = False
        if self.can_promote():
            Piece.interacting_w_promote_UI = True
            Piece.promoting_side = self.side
            Piece.promoting_piece = self



    def promote(self, piece, board):
        if piece == "Queen":
            Queen((self.posX, self.posY), self.side).place(board)
        elif piece == "Rook":
            Rook((self.posX, self.posY), self.side).place(board)
        elif piece == "Bishop":
            Bishop((self.posX, self.posY), self.side).place(board)
        elif piece == "Knight":
            Knight((self.posX, self.posY), self.side).place(board)


class Bishop(Piece):
    def __str__(self):
        return "B"

    def __init__(self, pos, side):
        self.posX, self.posY = pos
        self.side = side
        self.picked = False
        if self.side > 0:
            sprite = pygame.image.load("Sprites/bishop1.png")
            self.sprite = pygame.transform.scale(sprite, (75, 75))
        else:
            sprite = pygame.image.load("Sprites/bishop.png")
            self.sprite = pygame.transform.scale(sprite, (75, 75))

    def is_valid_move(self, new_pos, board):
        numpy_board = board.to_numpy()
        diags = [numpy_board[::-1, :].diagonal(i) for i in range(-numpy_board.shape[0] + 1, numpy_board.shape[1])]
        diags.extend(numpy_board.diagonal(i) for i in range(numpy_board.shape[1] - 1, -numpy_board.shape[0], -1))
        diags = [n.tolist() for n in diags]

        if self.is_not_blocked(new_pos, board) and self.in_diagonal(new_pos, board, diags)[0]:
            return True
        return False


class Rook(Piece):
    def __str__(self):
        return "R"

    def __init__(self, pos, side):
        self.posX, self.posY = pos
        self.side = side
        self.moved_once = False
        self.picked = False
        if self.side > 0:
            sprite = pygame.image.load("Sprites/rook1.png")
            self.sprite = pygame.transform.scale(sprite, (75, 75))
        else:
            sprite = pygame.image.load("Sprites/rook.png")
            self.sprite = pygame.transform.scale(sprite, (75, 75))

    def is_valid_move(self, new_pos, board):
        if self.is_not_blocked(new_pos, board) and (self.posX == new_pos[0] or self.posY == new_pos[1]):
            return True
        return False

    def move(self, new_pos, board):
        board.loc[self.posY, self.posX] = EmptySquare()
        self.posX, self.posY = new_pos
        board.loc[new_pos[1], new_pos[0]] = self
        self.moved_once = True

        for pawn in Piece.enpassant_pawns:
            if self.side != pawn.side:
                pawn.enpassant = False


class Queen(Piece):
    def __str__(self):
        return "Q"

    def __init__(self, pos, side):
        self.posX, self.posY = pos
        self.side = side
        self.picked = False
        if self.side > 0:
            sprite = pygame.image.load("Sprites/queen1.png")
            self.sprite = pygame.transform.scale(sprite, (75, 75))
        else:
            sprite = pygame.image.load("Sprites/queen.png")
            self.sprite = pygame.transform.scale(sprite, (75, 75))

    def is_valid_move(self, new_pos, board):
        numpy_board = board.to_numpy()
        diags = [numpy_board[::-1, :].diagonal(i) for i in range(-numpy_board.shape[0] + 1, numpy_board.shape[1])]
        diags.extend(numpy_board.diagonal(i) for i in range(numpy_board.shape[1] - 1, -numpy_board.shape[0], -1))
        diags = [n.tolist() for n in diags]

        if self.is_not_blocked(new_pos, board) and ((self.posX == new_pos[0] or self.posY == new_pos[1]) or
                                                    self.in_diagonal(new_pos, board, diags)[0]):
            return True
        return False


class Knight(Piece):
    def __str__(self):
        return "N"

    def __init__(self, pos, side):
        self.posX, self.posY = pos
        self.side = side
        self.picked = False
        if self.side > 0:
            sprite = pygame.image.load("Sprites/knight1.png")
            self.sprite = pygame.transform.scale(sprite, (75, 75))
        else:
            sprite = pygame.image.load("Sprites/knight.png")
            self.sprite = pygame.transform.scale(sprite, (75, 75))

    def is_valid_move(self, new_pos, board):
        all_moves = [
            (self.to_int_dict[self.posX]+1, self.posY-2),
            (self.to_int_dict[self.posX]-1, self.posY-2),
            (self.to_int_dict[self.posX]+1, self.posY+2),
            (self.to_int_dict[self.posX]-1, self.posY+2),
            (self.to_int_dict[self.posX]+2, self.posY+1),
            (self.to_int_dict[self.posX]+2, self.posY-1),
            (self.to_int_dict[self.posX]-2, self.posY+1),
            (self.to_int_dict[self.posX]-2, self.posY-1)
        ]
        legal_moves = []
        for move in all_moves:
            if (0 <= move[0] <= 7) and (0 <= move[1] <= 7):
                legal_moves.append((self.letters[move[0]], move[1]))

        if new_pos in legal_moves and board.loc[new_pos[1], new_pos[0]].side != self.side:
            return True
        return False


class King(Piece):
    def __str__(self):
        return "K"

    def __init__(self, pos, side):
        self.posX, self.posY = pos
        self.side = side
        self.picked = False
        self.legal_moves = []
        self.moved_once = False
        if self.side > 0:
            sprite = pygame.image.load("Sprites/king1.png")
            self.sprite = pygame.transform.scale(sprite, (75, 75))
        else:
            sprite = pygame.image.load("Sprites/king.png")
            self.sprite = pygame.transform.scale(sprite, (75, 75))

    def is_valid_move(self, new_pos, board):
        all_moves = []
        # in_check_moves = []
        self.legal_moves = []

        for row in range(-1, 2):
            for col in range(-1, 2):
                all_moves.append((self.to_int_dict[self.posX]+col, self.posY+row))

        for move in all_moves:
            if (0 <= move[0] <= 7) and (0 <= move[1] <= 7):
                self.legal_moves.append((self.letters[move[0]], move[1]))

        if self.side == -1:
            temp_y_pos = 7
        elif self.side == 1:
            temp_y_pos = 0
        if new_pos == ("g", temp_y_pos):
            if isinstance(board.loc[temp_y_pos, "h"], Rook) and not board.loc[temp_y_pos, "h"].moved_once and not self.moved_once and board.loc[temp_y_pos, "h"].side == self.side:
                if not self.in_check(("f", temp_y_pos), board) and not self.in_check(new_pos, board) and not self.in_check((self.posX, self.posY), board):
                    if isinstance(board.loc[new_pos[1], new_pos[0]], EmptySquare) and isinstance(board.loc[temp_y_pos, "f"], EmptySquare):
                        board.loc[temp_y_pos, "h"].move(("f", temp_y_pos), board)
                        return True
        if new_pos == ("c", temp_y_pos):
            if isinstance(board.loc[temp_y_pos, "a"], Rook) and not board.loc[temp_y_pos, "a"].moved_once and not self.moved_once and board.loc[temp_y_pos, "h"].side == self.side:
                if not self.in_check(("d", temp_y_pos), board) and not self.in_check(new_pos, board) and not self.in_check((self.posX, self.posY), board):
                    if isinstance(board.loc[new_pos[1], new_pos[0]], EmptySquare) and isinstance(board.loc[temp_y_pos, "d"], EmptySquare):
                        board.loc[temp_y_pos, "a"].move(("d", temp_y_pos), board)
                        return True

        if new_pos in self.legal_moves and board.loc[new_pos[1], new_pos[0]].side != self.side and not self.in_check(new_pos, board):
            self.moved_once = True
            return True
        return False

    def in_check(self, new_pos, board):
        temp_pos = self.posX, self.posY
        temp_piece = board.loc[new_pos[1], new_pos[0]]
        self.move(new_pos, board)

        for index, row in board.iterrows():
            for square in row:

                if (
                        not isinstance(square, EmptySquare) and
                        # not isinstance(square, King) and
                        not isinstance(square, Pawn) and
                        square.side != self.side and
                        square.is_valid_move(new_pos, board)
                ):
                    self.move(temp_pos, board)
                    temp_piece.place(board)
                    return True

                if isinstance(square, Pawn) and square.side != self.side:
                    if (
                            (((self.to_int_dict[new_pos[0]] == self.to_int_dict[square.posX] + 1) or
                              (self.to_int_dict[new_pos[0]] == self.to_int_dict[square.posX] - 1))
                             and (new_pos[1] == square.posY + square.side))
                    ):
                        self.move(temp_pos, board)
                        temp_piece.place(board)
                        return True
                if isinstance(square, King) and square.side != self.side:
                    if new_pos in square.legal_moves:
                        self.move(temp_pos, board)
                        temp_piece.place(board)
                        return True

        self.move(temp_pos, board)
        temp_piece.place(board)
        return False


def DrawPromoteUI(win, font1, cursor_pos):
    displacement = 9
    pygame.draw.rect(win, (24, 24, 24), (300, 225, 200, 50))
    pygame.draw.rect(win, (199, 199, 199), (305, 230, 190, 40))
    win.blit(pygame.transform.scale(Queen(("a", 0), Piece.promoting_side).sprite, (36, 36)), (307, 232))
    win.blit(font1.render("Queen", True, (24, 24, 24)), (367, 230+displacement))

    pygame.draw.rect(win, (24, 24, 24), (300, 300, 200, 50))
    pygame.draw.rect(win, (199, 199, 199), (305, 305, 190, 40))
    win.blit(pygame.transform.scale(Rook(("a", 0), Piece.promoting_side).sprite, (36, 36)), (307, 307))
    win.blit(font1.render("Rook", True, (24, 24, 24)), (375, 305+displacement))

    pygame.draw.rect(win, (24, 24, 24), (300, 375, 200, 50))
    pygame.draw.rect(win, (199, 199, 199), (305, 380, 190, 40))
    win.blit(pygame.transform.scale(Bishop(("a", 0), Piece.promoting_side).sprite, (36, 36)), (307, 382))
    win.blit(font1.render("Bishop", True, (24, 24, 24)), (367, 380+displacement))

    pygame.draw.rect(win, (24, 24, 24), (300, 450, 200, 50))
    pygame.draw.rect(win, (199, 199, 199), (305, 455, 190, 40))
    win.blit(pygame.transform.scale(Knight(("a", 0), Piece.promoting_side).sprite, (36, 36)), (307, 457))
    win.blit(font1.render("Knight", True, (24, 24, 24)), (367, 455+displacement))

    if 300 <= cursor_pos[0] <= 500:
        if 225 <= cursor_pos[1] <= 275:
            pygame.draw.rect(win, (0, 200, 0), (300, 225, 200, 50))
            pygame.draw.rect(win, (199, 199, 199), (305, 230, 190, 40))
            win.blit(pygame.transform.scale(Queen(("a", 0), Piece.promoting_side).sprite, (36, 36)), (307, 232))
            win.blit(font1.render("Queen", True, (24, 24, 24)), (367, 230+displacement))

        if 300 <= cursor_pos[1] <= 350:
            pygame.draw.rect(win, (0, 200, 0), (300, 300, 200, 50))
            pygame.draw.rect(win, (199, 199, 199), (305, 305, 190, 40))
            win.blit(pygame.transform.scale(Rook(("a", 0), Piece.promoting_side).sprite, (36, 36)), (307, 307))
            win.blit(font1.render("Rook", True, (24, 24, 24)), (375, 305+displacement))

        if 375 <= cursor_pos[1] <= 425:
            pygame.draw.rect(win, (0, 200, 0), (300, 375, 200, 50))
            pygame.draw.rect(win, (199, 199, 199), (305, 380, 190, 40))
            win.blit(pygame.transform.scale(Bishop(("a", 0), Piece.promoting_side).sprite, (36, 36)), (307, 382))
            win.blit(font1.render("Bishop", True, (24, 24, 24)), (367, 380+displacement))

        if 450 <= cursor_pos[1] <= 500:
            pygame.draw.rect(win, (0, 200, 0), (300, 450, 200, 50))
            pygame.draw.rect(win, (199, 199, 199), (305, 455, 190, 40))
            win.blit(pygame.transform.scale(Knight(("a", 0), Piece.promoting_side).sprite, (36, 36)), (307, 457))
            win.blit(font1.render("Knight", True, (24, 24, 24)), (367, 455+displacement))

def ResetBoard(letters, Board, move_history):
    move_history = []
    Piece.side = None
    Piece.sprite = None
    Piece.picked = None
    Piece.enpassant_pawns = []
    Piece.interacting_w_UI = False
    Piece.interacting_w_promote_UI = False
    Piece.promoting_side = None
    Piece.promoting_piece = None

    for letter in letters:
        Board[letter] = pd.Series([EmptySquare() for i in range(8)])

    for i in range(8):
        Pawn((letters[i], 1), 1).place(Board)
        Pawn((letters[i], 6), -1).place(Board)

    Bishop(("c", 0), 1).place(Board)
    Bishop(("f", 0), 1).place(Board)
    Bishop(("c", 7), -1).place(Board)
    Bishop(("f", 7), -1).place(Board)

    Rook(("a", 0), 1).place(Board)
    Rook(("h", 0), 1).place(Board)
    Rook(("a", 7), -1).place(Board)
    Rook(("h", 7), -1).place(Board)

    Queen(("d", 0), 1).place(Board)
    Queen(("d", 7), -1).place(Board)

    Knight(("b", 0), 1).place(Board)
    Knight(("g", 0), 1).place(Board)
    Knight(("b", 7), -1).place(Board)
    Knight(("g", 7), -1).place(Board)

    King(("e", 0), 1).place(Board)
    King(("e", 7), -1).place(Board)

