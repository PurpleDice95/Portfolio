import numpy as np
import pygame
import math
from PIL import Image

# Inspiration https://youtu.be/gYRrGTC7GtA


# Params
fov = 60
sensitivity = 1.0
movement_speed = 3.0

Map = Image.open("Map.png")
grid = np.array(Map)

pygame.init()
screenSize = (1920, 1080)
screen = pygame.display.set_mode(screenSize)

pygame.mouse.set_pos(screenSize[0]/2, screenSize[1]/2)
pygame.mouse.set_visible(False)
running = True






class Camera:
    def __init__(self, pos):
        self.pos_x, self.pos_y = pos
        self.box_x, self.box_y = self.pos_x//100, self.pos_y//100
        self.facing = 90

    def move(self, bearing, move_facing):
        if tuple(grid[int(self.pos_y//100), int((self.pos_x + movement_speed * np.cos(np.deg2rad((self.facing + move_facing)%360)))//100)]) == (255, 255, 255, 255):
            self.pos_x = self.pos_x + movement_speed*np.cos(np.deg2rad(bearing))
        if tuple(grid[int((self.pos_y + movement_speed * np.sin(np.deg2rad((self.facing + move_facing)%360)))//100), int(self.pos_x//100)]) == (255, 255, 255, 255):
            self.pos_y = self.pos_y + movement_speed*np.sin(np.deg2rad(bearing))

    def moveForward(self):
        self.move(self.facing, 0)

    def moveBackward(self):
        self.move((self.facing+180) % 360, 180)

    def moveLeft(self):
        self.move((self.facing-90) % 360, -90)

    def moveRight(self):
        self.move((self.facing+90) % 360, 90)


def euc_dis(x1, y1, x2, y2):
    return np.sqrt((x1-x2)**2 + (y1-y2)**2)


def shaded_color(color):
    return max(0, color[0] - 10), max(0, color[1] - 10), max(0, color[2] - 10)

# Ray
def CastRay():
    global grid
    global player
    global screen
    ray_bearing = player.facing
    count = 0

    for ray_bearing in np.linspace(ray_bearing - fov/2, ray_bearing + fov/2, num=fov):
        ray_bearing %= 360
        # horizontal check
        depth = 0
        aTan = -1/np.tan(np.deg2rad(ray_bearing))
        Hwall_color = (255, 255, 255)
        Vwall_color = (255, 255, 255)

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
            depth = grid.shape[1]+1
        while depth < grid.shape[1]+1:
            if 0 <= ray_x//100 < grid.shape[1] and 0 <= ray_y//100 < grid.shape[0] and tuple(grid[int(ray_y//100), int(ray_x//100)]) != (255, 255, 255, 255):
                depth = grid.shape[1]+1
                Hwall_color = tuple(grid[int(ray_y//100), int(ray_x//100)])
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
            depth = grid.shape[0]+1
        while depth < grid.shape[0]+1:
            if 0 <= ray_x // 100 < grid.shape[1] and 0 <= ray_y // 100 < grid.shape[0] and tuple(grid[int(ray_y//100), int(ray_x//100)]) != (255, 255, 255, 255):
                depth = grid.shape[0]+1
                Vwall_color = shaded_color(tuple(grid[int(ray_y//100), int(ray_x//100)]))
            else:
                ray_x += x_offset
                ray_y += y_offset
                depth += 1

        vray_x, vray_y = ray_x, ray_y

        VEucDis = euc_dis(vray_x, vray_y, player.pos_x, player.pos_y)
        HEucDis = euc_dis(hray_x, hray_y, player.pos_x, player.pos_y)
        if VEucDis <= HEucDis:
            ray_x, ray_y = vray_x, vray_y
            TrueEucDis = VEucDis
            wall_color = Vwall_color
        else:
            ray_x, ray_y = hray_x, hray_y
            TrueEucDis = HEucDis
            wall_color = Hwall_color

        TrueEucDis *= np.cos(np.deg2rad((player.facing-ray_bearing)%360))

        lineDistance = (100 * screenSize[1])/0.01 if TrueEucDis == 0 else (100 * screenSize[1])/TrueEucDis

        lineDistance = screenSize[1] if lineDistance >= screenSize[1] else lineDistance

        pygame.draw.rect(screen, wall_color, (count*math.ceil(screenSize[0]/fov), (screenSize[1]-lineDistance)/2, math.ceil(screenSize[0]/fov), lineDistance))
        count += 1


player = Camera((150, 150))

# Main loop
while running:
    screen.fill((255, 255, 255))
    mouse_pos = pygame.mouse.get_pos()
    keyboard_state = pygame.key.get_pressed()
    pygame.draw.rect(screen, (0, 0, 0), (0, int(screenSize[1]/2), screenSize[0], int(screenSize[1]/2)))
    CastRay()



    if mouse_pos[0] > screenSize[0]/2:
        player.facing = (player.facing + sensitivity) % 360
        pygame.mouse.set_pos(screenSize[0]/2, screenSize[1]/2)
    elif mouse_pos[0] < screenSize[0]/2:
        player.facing = (player.facing - sensitivity) % 360
        pygame.mouse.set_pos(screenSize[0]/2, screenSize[1]/2)


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
