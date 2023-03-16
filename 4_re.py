import pygame
import random
import time

# 게임 화면 설정
WIDTH = 640
HEIGHT = 480
FPS = 10

# 색상 설정
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# 초기화
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# 이미지 로드
snake_img = pygame.image.load('snake.png').convert()
apple_img = pygame.image.load('apple.png').convert()
background_img = pygame.image.load('background.png').convert()

# 뱀 클래스
class Snake:
    def __init__(self):
        self.positions = [(3, 0), (2, 0), (1, 0), (0, 0)]  # 초기 위치
        self.length = 4  # 초기 길이
        self.direction = 'E'  # 초기 방향
    
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
        self.positions.insert(0, next_position)
        if len(self.positions) > self.length:
            self.positions.pop()

# 충돌 검사 함수
def collide(head, body):
    if head in body[1:]:
        return True
    if head[0] < 0 or head[0] >= HEIGHT or head[1] < 0 or head[1] >= WIDTH:
        return True
    return False

# 사과 생성 함수
def create_apple():
    x = random.randrange(0, WIDTH - 20, 20)
    y = random.randrange(0, HEIGHT - 20, 20)
    return (y, x)

# 글씨 보이기 함수
def show_text(text, x, y, color, size):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# 게임 실행 함수
def run_game():
    snake = Snake()
    apple_position = create_apple()
    score = 0
    game_over = False

    while not game_over:
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != 'S':
                    snake.direction = 'N'
                elif event.key == pygame.K_DOWN and snake.direction != 'N':
                    snake.direction = 'S'
                elif event.key == pygame.K_LEFT and snake.direction != 'E':
                    snake.direction = 'W'
                elif event.key == pygame.K_RIGHT and snake.direction != 'W':
                    snake.direction = 'E'

        # 뱀 이동
        snake.move()

        # 충돌 검사
        if collide(snake.positions[0], snake.positions):
            message_display("Game Over")
            pygame.time.wait(2000)
            pygame.quit()
            quit()

        # 사과 먹기
        if snake.positions[0] == apple_position:
            snake.length += 1
            score += 1
            speed += 1
            apple_position = create_apple()

        # 화면 그리기
        screen.blit(background_img, (0, 0))
        screen.blit(apple_img, apple_position)
        for position in snake.positions:
            screen.blit(snake_img, (position[1]*20, position[0]*20))
        draw_score(score)
        pygame.display.update()

        # 게임 속도 설정
        clock.tick(speed)

run_game()