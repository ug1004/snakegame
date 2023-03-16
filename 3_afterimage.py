import random
from datetime import datetime, timedelta

import pygame

pygame.init()
background_image = pygame.image.load("background.png")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
 
WIDTH = 500
HEIGHT = 800
BLOCK_SIZE = 20
 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("UG Snake GAME")
 
clock = pygame.time.Clock()
last_moved_time = datetime.now()

# 배경 이미지 로드
background = pygame.image.load('background.png')

class Snake:
    def __init__(self):
        self.positions = [(0,2),(0,1),(0,0)]  # 뱀의 위치
        self.direction = 'E'  # 초기방향 동쪽
        self.trail = [] # 자취 남길 장소 저장할 리스트
        self.background = background_image # 배경이미지 저장할 surface
 
    def draw(self):
        # 이전 위치 지우기
        for position in self.trail:
            draw_block(screen, background_image, position)

        # 이전 위치 자취로 남길 리스트 추가
        for position in self.positions:
            if position not in self.trail:
                self.trail.append(position)

        # 자취를 그리기
        for position in self.trail:
            draw_block(screen, background_image, position)

        # 뱀을 그리기
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
        elif self.direction == 'E':
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

 
def draw_block(screen, color, position, background=None):
    block = pygame.Rect((position[1] * BLOCK_SIZE, position[0] * BLOCK_SIZE), (BLOCK_SIZE, BLOCK_SIZE))
    if background is not None:
        screen.blit(background, block)
    else:
        pygame.draw.rect(screen, color, block)

def run_game(speed):
    global last_moved_time
    
    snake = Snake()
    apple = Apple()
    done = False
    
    while not done:
        clock.tick(speed)
        
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
                if speed > 3:
                    speed -= 3
            
            if snake.positions[0] in snake.positions[1:]:
                done = True
            
            screen.blit(snake.background, (0,0)) # 배경 이미지 그리기
            snake.draw() # 뱀 그리기
            apple.draw()
            pygame.display.update()
    
    pygame.quit()

    # 1초 대기
pygame.time.wait(1000)

KEY_DIRECTION = {
    pygame.K_UP: 'N',
    pygame.K_DOWN: 'S',
    pygame.K_LEFT: 'W',
    pygame.K_RIGHT: 'E',
}

speed = 10
run_game(speed)