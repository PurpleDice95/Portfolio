import numpy as np
import pygame


pygame.init()
mapSize = (800, 800)
screen = pygame.display.set_mode(mapSize)

pygame.mouse.set_pos(mapSize[0]/2, mapSize[1]/2)
pygame.mouse.set_visible(False)
running = True

# 700 by 700 space
grid = np.array([[1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 0, 1, 0, 0, 0, 0, 1],
                 [1, 0, 1, 0, 0, 0, 0, 1],
                 [1, 0, 1, 0, 0, 0, 0, 1],
                 [1, 0, 0, 0, 1, 0, 0, 1],
                 [1, 0, 0, 0, 0, 0, 0, 1],
                 [1, 0, 0, 0, 0, 0, 0, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1]])

fov = 60


class Camera:
    def __init__(self, pos):
        self.pos_x, self.pos_y = pos
        self.box_x, self.box_y = self.pos_x//100, self.pos_y//100
        self.facing = 90

    def move(self, bearing):
        self.pos_x = self.pos_x + 0.1*np.cos(np.deg2rad(bearing))
        self.pos_y = self.pos_y + 0.1*np.sin(np.deg2rad(bearing))

    def moveForward(self):
        self.move(self.facing)

    def moveBackward(self):
        self.move((self.facing+180) % 360)

    def moveLeft(self):
        self.move((self.facing-90) % 360)

    def moveRight(self):
        self.move((self.facing+90) % 360)


def euc_dis(x1, y1, x2, y2):
    return np.sqrt((x1-x2)**2 + (y1-y2)**2)

def CastRay():
    global grid
    global player
    ray_bearing = player.facing

    for ray_bearing in np.linspace(ray_bearing - fov/2, ray_bearing + fov/2, num=fov):
        ray_bearing %= 360
        # horizontal check
        depth = 0
        aTan = -1/np.tan(np.deg2rad(ray_bearing))

        if ray_bearing > 180:
            ray_y = (player.pos_y // 100) * 100 - 0.001
            ray_x = (player.pos_y - ray_y)*aTan + player.pos_x
            y_offset = -100
            x_offset = -y_offset*aTan
        if ray_bearing < 180:
            ray_y = (player.pos_y // 100) * 100 + 100
            ray_x = (player.pos_y - ray_y) * aTan + player.pos_x
            y_offset = 100
            x_offset = -y_offset * aTan
        if ray_bearing == 0 or ray_bearing == 180:
            ray_y = player.pos_y
            ray_x = player.pos_x
            depth = 8
        while depth < 8:
            if 0 <= ray_x//100 < grid.shape[1] and 0 <= ray_y//100 < grid.shape[0] and grid[int(ray_y//100), int(ray_x//100)] == 1:
                depth = 8
            else:
                ray_x += x_offset
                ray_y += y_offset
                depth += 1

        hray_x, hray_y = ray_x, ray_y

        # vertical check
        depth = 0
        nTan = -np.tan(np.deg2rad(ray_bearing))
        if 90 < ray_bearing < 270:
            ray_x = (player.pos_x // 100) * 100 - 0.001
            ray_y = (player.pos_x - ray_x) * nTan + player.pos_y
            x_offset = -100
            y_offset = -x_offset * nTan
        if ray_bearing > 270 or ray_bearing < 90:
            ray_x = (player.pos_x // 100) * 100 + 100
            ray_y = (player.pos_x - ray_x) * nTan + player.pos_y
            x_offset = 100
            y_offset = -x_offset * nTan
        if ray_bearing == 90 or ray_bearing == 270:
            ray_y = player.pos_y
            ray_x = player.pos_x
            depth = 9
        while depth < 9:
            if 0 <= ray_x // 100 < grid.shape[1] and 0 <= ray_y // 100 < grid.shape[0] and grid[int(ray_y // 100), int(ray_x // 100)] == 1:
                depth = 9
            else:
                ray_x += x_offset
                ray_y += y_offset
                depth += 1

        vray_x, vray_y = ray_x, ray_y

        ray_x, ray_y = (vray_x, vray_y) if euc_dis(vray_x, vray_y, player.pos_x, player.pos_y) <= euc_dis(hray_x, hray_y, player.pos_x, player.pos_y) else (hray_x, hray_y)


        pygame.draw.line(screen, (0, 255, 0), (player.pos_x, player.pos_y), (ray_x, ray_y))
        pygame.draw.line(screen, (0, 255, 0), (player.pos_x, player.pos_y), (player.pos_x + 10*np.cos(np.deg2rad(player.facing)), player.pos_y + 10*np.sin(np.deg2rad(player.facing))))



def DrawMapTemp():
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[j, i] == 1:
                pygame.draw.rect(screen, (255, 255, 255), (i*100, j*100, 99, 99))




player = Camera((150, 150))

while running:
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 0), (player.pos_x, player.pos_y, 5, 5))
    mouse_pos = pygame.mouse.get_pos()
    keyboard_state = pygame.key.get_pressed()
    DrawMapTemp()
    if not pygame.mouse.get_pressed(3)[0]:
        CastRay()



    if mouse_pos[0] > mapSize[0]/2:
        player.facing = (player.facing + 0.3) % 360
        pygame.mouse.set_pos(mapSize[0]/2, mapSize[1]/2)
    elif mouse_pos[0] < mapSize[0]/2:
        player.facing = (player.facing - 0.3) % 360
        pygame.mouse.set_pos(mapSize[0]/2, mapSize[1]/2)

    if keyboard_state[pygame.K_w]:
        player.moveForward()
    if keyboard_state[pygame.K_s]:
        player.moveBackward()
    if keyboard_state[pygame.K_a]:
        player.moveLeft()
    if keyboard_state[pygame.K_d]:
        player.moveRight()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
