import pygame
import sys
import os
from random import randrange as rnd

WIDTH, HEIGHT = 1200, 800
fps = 60

paddle_w = 330
paddle_h = 35
paddle_speed = 15
paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, HEIGHT - paddle_h - 10, paddle_w, paddle_h)

ball_radius = 20
ball_speed = 6
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
dx, dy = 1, -1

block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
color_list = [(0, 100, 0) for i in range(10) for j in range(4)]

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

img = pygame.image.load('data/1.jpg').convert()

size = width, height = 1200, 800
screen = pygame.display.set_mode(size)

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    pygame.init()
    intro_text = ["                                                      Арканоид","",
                  "                        Нажмите любую кнопку чтобы продолжить","",]
    fon = pygame.transform.scale(load_image('1.jpg'), size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 350
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('blue'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(30)

def end_screen():
    pygame.init()
    intro_text = ["       GAME","",
                  "                                      OVER"]
    fon = pygame.transform.scale(load_image('1.jpg'), size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 350
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                exit()
        pygame.display.flip()
        clock.tick(30)

def end_screen1():
    pygame.init()
    intro_text = ["       YOU", "",
                  "                                      WIN!"]
    fon = pygame.transform.scale(load_image('1.jpg'), size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 350
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('green'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                exit()
        pygame.display.flip()
        clock.tick(30)




def detect_collision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy

start_screen()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end_screen()

    sc.blit(img, (0, 0))

    [pygame.draw.rect(sc, color_list[color], block) for color, block in enumerate(block_list)]
    pygame.draw.rect(sc, pygame.Color('darkblue'), paddle)
    pygame.draw.circle(sc, pygame.Color('darkred'), ball.center, ball_radius)

    ball.x += ball_speed * dx
    ball.y += ball_speed * dy

    if ball.centerx < ball_radius or ball.centerx > WIDTH - ball_radius:
        dx = -dx

    if ball.centery < ball_radius:
        dy = -dy

    if ball.colliderect(paddle) and dy > 0:
        dx, dy = detect_collision(dx, dy, ball, paddle)

    hit_index = ball.collidelist(block_list)
    if hit_index != -1:
        hit_rect = block_list.pop(hit_index)
        hit_color = color_list.pop(hit_index)
        dx, dy = detect_collision(dx, dy, ball, hit_rect)

        hit_rect.inflate_ip(ball.width * 3, ball.height * 3)
        pygame.draw.rect(sc, hit_color, hit_rect)
        fps += 2

    if ball.bottom > HEIGHT:
        end_screen()
        print('GAME OVER!')
        exit()
    elif not len(block_list):
        end_screen1()
        print('YOU WIN')
        exit()

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= paddle_speed
    if key[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.right += paddle_speed

    pygame.display.flip()
    clock.tick(fps)