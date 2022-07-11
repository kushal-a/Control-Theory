import pygame
import numpy as np
import Control as c

pygame.init()
screen = pygame.display.set_mode((800, 600), 0, 40)
centerX = 400
centerY = 400
plateT = 60
time = 0
plate = pygame.image.load("plate.png")
plate = pygame.transform.rotate(plate, -45)
ball = pygame.image.load("ball.png")
ball = pygame.transform.scale(ball, (40, 40))
pivot = pygame.image.load("plain-triangle.png")
run = True


def blit_rot_center(surf, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)

    surf.blit(rotated_image, new_rect)


dx = 0.0
x = 0
x_new = x
theta = 0
dtheta = 0.0
PID_status = ""

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                X, Y = event.pos
                x_new = (X - (centerX - 20 - plateT * np.sin(np.radians(theta)))) / np.cos(np.radians(theta))
                PID_status = "RESET"
        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0] == 1:
                X, Y = event.pos
                x_new = (X - (centerX - 20 - plateT * np.sin(np.radians(theta)))) / np.cos(np.radians(theta))
                PID_status = "RESET"

    dx, dtheta = c.solve(x, theta, dx, x_new, PID_status)
    if x > 300 or x < -300:
        dx = 0
    x += dx
    if theta > 15 or theta < -15:
        dtheta = 0
    theta += dtheta

    screen.fill((235, 62, 74))
    blit_rot_center(screen, plate, (centerX - 364, centerY - 364), theta)
    screen.blit(ball, (centerX - 20 + x * np.cos(np.radians(theta)) - plateT * np.sin(np.radians(theta)),
                       centerY - 20 - plateT * np.cos(np.radians(theta)) - x * np.sin(np.radians(theta))))
    time += 1
    screen.blit(pivot, (centerX - 32, centerY - 32 + plateT))
    pygame.display.update()
