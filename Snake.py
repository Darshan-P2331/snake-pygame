import pygame
import sys
import random
from pygame.math import Vector2

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

CELL_SIZE = 30
CELL_NUMBER = 20
FPS = 60


GRASS_COLOR = (167, 209, 61)

SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, 150)

WIN = pygame.display.set_mode(
    (CELL_SIZE * CELL_NUMBER, CELL_SIZE * CELL_NUMBER))
pygame.display.set_caption("Snake Game")

FONT_FACE = pygame.font.Font('Assets/Font/PoetsenOne-Regular.ttf', 25)
CRUNCH_SOUND = pygame.mixer.Sound('Assets/Sound/crunch.wav')

# Images
APPLE = pygame.image.load('Assets/Graphics/apple.png').convert_alpha()

HEAD_UP = pygame.image.load('Assets/Graphics/head_up.png').convert_alpha()
HEAD_DOWN = pygame.image.load('Assets/Graphics/head_down.png').convert_alpha()
HEAD_LEFT = pygame.image.load('Assets/Graphics/head_left.png').convert_alpha()
HEAD_RIGHT = pygame.image.load(
    'Assets/Graphics/head_right.png').convert_alpha()

TAIL_UP = pygame.image.load('Assets/Graphics/tail_up.png').convert_alpha()
TAIL_DOWN = pygame.image.load('Assets/Graphics/tail_down.png').convert_alpha()
TAIL_LEFT = pygame.image.load('Assets/Graphics/tail_left.png').convert_alpha()
TAIL_RIGHT = pygame.image.load(
    'Assets/Graphics/tail_right.png').convert_alpha()

BODY_VERTICAL = pygame.image.load(
    'Assets/Graphics/body_vertical.png').convert_alpha()
BODY_HORIZONTAL = pygame.image.load(
    'Assets/Graphics/body_horizontal.png').convert_alpha()

BODY_TR = pygame.image.load('Assets/Graphics/body_tr.png').convert_alpha()
BODY_TL = pygame.image.load('Assets/Graphics/body_tl.png').convert_alpha()
BODY_BR = pygame.image.load('Assets/Graphics/body_br.png').convert_alpha()
BODY_BL = pygame.image.load('Assets/Graphics/body_bl.png').convert_alpha()

clock = pygame.time.Clock()


class Fruit:
    def __init__(self):
        self.randomize()

    def draw(self):
        fruit_rect = pygame.Rect(self.pos.x*CELL_SIZE,
                                 self.pos.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        WIN.blit(APPLE, fruit_rect)
        # pygame.draw.rect(WIN, (126, 166, 140), fruit_rect)

    def randomize(self):
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)


class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False

    def draw(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        for i, block in enumerate(self.body):
            x_pos = block.x * CELL_SIZE
            y_pos = block.y * CELL_SIZE
            block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)

            if i == 0:
                WIN.blit(self.head, block_rect)
            elif i == len(self.body) - 1:
                WIN.blit(self.tail, block_rect)
            else:
                prev_block = self.body[i+1]-block
                next_block = self.body[i-1]-block
                if prev_block.x == next_block.x:
                    WIN.blit(BODY_VERTICAL, block_rect)
                elif prev_block.y == next_block.y:
                    WIN.blit(BODY_HORIZONTAL, block_rect)
                else:
                    if prev_block.x == -1 and next_block.y == -1 or prev_block.y == -1 and next_block.x == -1:
                        WIN.blit(BODY_TL, block_rect)
                    elif prev_block.x == -1 and next_block.y == 1 or prev_block.y == 1 and next_block.x == -1:
                        WIN.blit(BODY_BL, block_rect)
                    elif prev_block.x == 1 and next_block.y == -1 or prev_block.y == -1 and next_block.x == 1:
                        WIN.blit(BODY_TR, block_rect)
                    elif prev_block.x == 1 and next_block.y == 1 or prev_block.y == 1 and next_block.x == 1:
                        WIN.blit(BODY_BR, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1]-self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = HEAD_LEFT
        elif head_relation == Vector2(-1, 0):
            self.head = HEAD_RIGHT
        elif head_relation == Vector2(0, 1):
            self.head = HEAD_UP
        elif head_relation == Vector2(0, -1):
            self.head = HEAD_DOWN

    def update_tail_graphics(self):
        tail_relation = self.body[-2]-self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = TAIL_LEFT
        elif tail_relation == Vector2(-1, 0):
            self.tail = TAIL_RIGHT
        elif tail_relation == Vector2(0, 1):
            self.tail = TAIL_UP
        elif tail_relation == Vector2(0, -1):
            self.tail = TAIL_DOWN

    def move(self):
        if self.new_block:
            body_copy = self.body[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0]+self.direction)
        self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        CRUNCH_SOUND.play()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)


class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def update(self):
        self.snake.move()
        self.collision()
        self.check_fail()

    def draw(self):
        self.draw_grass()
        self.fruit.draw()
        self.snake.draw()
        self.draw_score()

    def draw_grass(self):
        for row in range(CELL_NUMBER):
            if row % 2 == 0:
                for col in range(0, CELL_NUMBER, 2):
                    grass_rect = pygame.Rect(
                        col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(WIN, GRASS_COLOR, grass_rect)
            else:
                for col in range(1, CELL_NUMBER, 2):
                    grass_rect = pygame.Rect(
                        col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(WIN, GRASS_COLOR, grass_rect)

    def draw_score(self):
        score = len(self.snake.body) - 3
        score_label = FONT_FACE.render(f"{score}", 1, (56, 74, 12))
        score_x = CELL_SIZE * CELL_NUMBER - 60
        score_y = CELL_SIZE * CELL_NUMBER - 40
        score_rect = score_label.get_rect(center=(score_x, score_y))
        apple_rect = APPLE.get_rect(
            midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top,
                              apple_rect.width + score_rect.width + 6, apple_rect.height)

        pygame.draw.rect(WIN, (167, 209, 61), bg_rect)
        WIN.blit(score_label, score_rect)
        WIN.blit(APPLE, apple_rect)
        pygame.draw.rect(WIN, (56, 74, 12), bg_rect, 2)

    def collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < CELL_NUMBER or not 0 <= self.snake.body[0].y < CELL_NUMBER:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()


main_game = Main()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SNAKE_UPDATE:
            main_game.update()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and main_game.snake.direction.y != 1:
                main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and main_game.snake.direction.y != -1:
                main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT and main_game.snake.direction.x != 1:
                main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT and main_game.snake.direction.x != -1:
                main_game.snake.direction = Vector2(1, 0)

    WIN.fill((175, 215, 70))
    main_game.draw()
    pygame.display.update()
    clock.tick(FPS)
