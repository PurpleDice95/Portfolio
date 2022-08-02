import pandas as pd
import pygame
from Classes import *
import math

pygame.init()
pygame.font.init()

font1 = pygame.font.SysFont("Arial", 34)
font2 = pygame.font.Font("Antipasto-Pro-Regular-trial.ttf", 34)
win = pygame.display.set_mode((800, 800), pygame.RESIZABLE)
pygame.display.set_caption("Chess")
place_sound_effect = pygame.mixer.Sound("Sprites/click_x.wav")
pygame.display.set_icon(pygame.image.load("Sprites/Icon.png"))
invalid_move_sound_effect = pygame.mixer.Sound("Sprites/button-10.wav")
running = True
promote_to = None
annotate = False
annotations = []
move_history = []
scroll_y = 150

Board = pd.DataFrame(index=[x for x in range(8)])
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
ResetBoard(letters, Board, move_history)






while running:
    # Rendering
    win.fill((199, 199, 199))
    cursor_pos = cursor_pos_x, cursor_pos_y = pygame.mouse.get_pos()
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                # win.blit(pygame.image.load("Sprites/SquareW.png"), (i*100, j*100))
                pygame.draw.rect(win, (240, 195, 128), (i*100, j*100, 100, 100))
            else:
                # win.blit(pygame.image.load("Sprites/SquareB.png"), (i * 100, j * 100))
                pygame.draw.rect(win, (109, 62, 23), (i * 100, j * 100, 100, 100))
    for index, row in Board.iterrows():
        for square in row:
            square.draw(win)

    pygame.draw.rect(win, (24, 24, 24), (800, 0, 40, 840))
    pygame.draw.rect(win, (24, 24, 24), (0, 800, 840, 40))
    for col in Board.columns:
        win.blit(font1.render(col, True, (199, 199, 199)), (Piece.to_int_dict[col]*100+40, 800))
    for row in Board.index:
        win.blit(font1.render(str(8-row), True, (199, 199, 199)), (815, row*100+40))

    for move in move_history:
        if move[0].side == -1:
            dis_col = 900
        else:
            dis_col = 1000

        win.blit(font1.render(f"{str(move[0])} {move[1][0]}{8-move[1][1]}", True, (24, 24, 24)), (dis_col, scroll_y + (move_history.index(move)//2)*36))
        pygame.draw.line(win, (24, 24, 24), (890, 34 + scroll_y + (move_history.index(move)//2)*36), (1130, 34 + scroll_y + (move_history.index(move)//2)*36), 2)
    pygame.draw.rect(win, (35, 110, 97), (840, 0, 50, 840))
    pygame.draw.rect(win, (35, 110, 97), (840, 0, 440, 150))
    pygame.draw.rect(win, (35, 110, 97), (1130, 0, 150, 840))
    pygame.draw.rect(win, (35, 110, 97), (840, 690, 440, 150))





    # Annotation
    if annotate:
        for start, end in annotations:
            if start == end:
                pygame.draw.circle(win, (0, 200, 0), (start[0]*100+50, start[1]*100+50), 50, 5)
            else:
                startpoint = pygame.math.Vector2(start[0] * 100 + 50, start[1] * 100 + 50)
                endpoint = pygame.math.Vector2(end[0] * 100 + 50, end[1] * 100 + 50)
                pygame.draw.line(win, (0, 200, 0), startpoint, endpoint, 10)
                current_endpoint = endpoint + ((startpoint - endpoint).rotate(45).normalize().elementwise() * pygame.math.Vector2(40, 40).elementwise())
                pygame.draw.line(win, (0, 200, 0), endpoint, current_endpoint, 10)
                current_endpoint = endpoint + ((startpoint - endpoint).rotate(-45).normalize().elementwise() * pygame.math.Vector2(40, 40).elementwise())
                pygame.draw.line(win, (0, 200, 0), endpoint, current_endpoint, 10)

    # Render Pieces
    for index, row in Board.iterrows():
        for square in row:
            if not isinstance(square, EmptySquare):
                if square.picked:
                    win.blit(square.sprite, (cursor_pos_x-50, cursor_pos_y-50))

    if Piece.interacting_w_promote_UI:
        DrawPromoteUI(win, font2, cursor_pos)

    if cursor_pos_x > 800 or cursor_pos_y > 800:
        Piece.interacting_w_UI = True

    if promote_to is not None:
        Piece.promoting_piece.promote(promote_to, Board)
        Piece.interacting_w_promote_UI = False
        promote_to = None


    # Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.VIDEORESIZE:
            size = width, height = 1280, 840
            win = pygame.display.set_mode(size, pygame.RESIZABLE)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if Piece.interacting_w_promote_UI:
                    if 300 <= cursor_pos_x <= 500:
                        if 225 <= cursor_pos_y <= 275:
                            promote_to = "Queen"
                        if 300 <= cursor_pos_y <= 350:
                            promote_to = "Rook"
                        if 375 <= cursor_pos_y <= 425:
                            promote_to = "Bishop"
                        if 450 <= cursor_pos_y <= 500:
                            promote_to = "Knight"

                if not Piece.interacting_w_UI and not Piece.interacting_w_promote_UI:
                    pieceX = letters[int(cursor_pos[0]/100)]
                    pieceY = int(cursor_pos[1]/100)
                    if not isinstance(Board.loc[pieceY, pieceX], EmptySquare):
                        Board.loc[pieceY, pieceX].picked = True

            elif event.button == 3:
                if not Piece.interacting_w_UI and not Piece.interacting_w_promote_UI:
                    start_pos = int(cursor_pos[0]/100), int(cursor_pos[1]/100)

            elif event.button == 5:
                scroll_y -= 18

            elif event.button == 4:
                if scroll_y < 150:
                    scroll_y += 18

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if event.button == 1:
                if not Piece.interacting_w_UI and not Piece.interacting_w_promote_UI:
                    moveX = letters[int(cursor_pos[0]/100)]
                    moveY = int(cursor_pos[1] / 100)
                    move = moveX, moveY

                    if not isinstance(Board.loc[pieceY, pieceX], EmptySquare):
                        Board.loc[pieceY, pieceX].picked = False
                        if len(move_history) > 0:
                            turn_condition = (Board.loc[pieceY, pieceX].side != move_history[-1][0].side)
                        else:
                            turn_condition = True

                        if Board.loc[pieceY, pieceX].is_valid_move(move, Board) and turn_condition:
                            move_history.append((Board.loc[pieceY, pieceX], move))
                            Board.loc[pieceY, pieceX].move(move, Board)
                            annotate = False
                            annotations = []
                            place_sound_effect.play()
                        else:
                            invalid_move_sound_effect.play()
                Piece.interacting_w_UI = False

            elif event.button == 3:
                if not Piece.interacting_w_UI and not Piece.interacting_w_promote_UI:
                    end_pos = int(cursor_pos[0] / 100), int(cursor_pos[1] / 100)
                    annotations.append((start_pos, end_pos))
                    annotate = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                annotations = []
                annotate = False
            if event.key == pygame.K_r:
                ResetBoard(letters, Board, move_history)

    pygame.display.update()
