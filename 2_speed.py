import random
from datetime import datetime, timedelta

import pygame

pygame.init()
 
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
 
WIDTH = 800
HEIGHT = 200
BLOCK_SIZE = 20
 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("UG Snake Game")
 
clock = pygame.time.Clock()
last_moved_time = datetime.now()

class Snake:
    def __init__(self):
        self.positions = [(0,2),(0,1),(0,0)]  # 뱀의 위치
        self.direction = 'E'  # 초기방향 동쪽
 
    def draw(self):
        for position in self.positions: 
            draw_block(screen, GREEN, position)
 
    def move(self):
        head_position = self.positions[0]
        y, x = head_position
        if self.direction == 'N':
            next_position = (y - 1, x)
        elif self.direction == 'S':
            next_position = (y + 1, x)
        elif self.direction == 'W':
            next_position = (y, x - 1)
        elif self.direction == 'E':
            next_position = (y, x + 1)

        if next_position[0] < 0 or next_position[0] >= HEIGHT/BLOCK_SIZE or next_position[1] < 0 or next_position[1] >= WIDTH/BLOCK_SIZE:
            pygame.quit()
            quit()

        self.positions = [next_position] + self.positions[:-1]
 
    def grow(self):
        tail_position = self.positions[-1]
        y, x = tail_position
        if self.direction == 'N':
            self.positions.append((y - 1, x))
        elif self.direction == 'S':
            self.positions.append((y + 1, x))
        elif self.direction == 'W':
            self.positions.append((y, x - 1))
        elif self.direction == 'C':
            self.positions.append((y, x + 1))
 
class Apple:
    def __init__(self):
        self.position = (5,5)
  
    def draw(self):
        draw_block(screen, RED, self.position)
  
    def generate_position(self):
        new_x = random.randint(0, WIDTH//BLOCK_SIZE - 1)
        new_y = random.randint(0, HEIGHT//BLOCK_SIZE - 1)
        return (new_y, new_x)

 
def draw_block(screen, color, position):
    block = pygame.Rect((position[1] * BLOCK_SIZE, position[0] * BLOCK_SIZE),
                        (BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, color, block)
 
def run_game():
    global last_moved_time
 
    snake = Snake()
    apple = Apple()
    done = False
    speed = 10 # 속도 변수 추가
 
    while not done:
        clock.tick(speed) #현재 속도에 맞게 tick 설정
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN and event.key in KEY_DIRECTION:
                snake.direction = KEY_DIRECTION[event.key]
 
        if datetime.now() - last_moved_time > timedelta(seconds=0.1):
            snake.move()
            last_moved_time = datetime.now()
 
            if snake.positions[0] == apple.position:
                snake.grow()
                apple.position = apple.generate_position()
                speed += 3 # 속도를 3씩 증가
                 
            if snake.positions[0] in snake.positions[1:]:
                done = True
 
        screen.fill(WHITE)
        snake.draw()
        apple.draw()
        pygame.display.update()
 
    pygame.quit()
 
KEY_DIRECTION = {
    pygame.K_UP: 'N',
    pygame.K_DOWN: 'S',
    pygame.K_LEFT: 'W',
    pygame.K_RIGHT: 'E',
}
 
run_game()
