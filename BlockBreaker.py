import pygame
import random
import sys

# Pygame 초기화
pygame.init()

# 화면 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("블록 깨기 게임")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
LIME = (50, 205, 50)
PURPLE = (128, 0, 128)

# 게임 클래스
class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vx = random.choice([-5, 5])
        self.vy = -5

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

        # 벽과의 충돌
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.vx *= -1
        if self.rect.top <= 0:
            self.vy *= -1
        if self.rect.bottom >= SCREEN_HEIGHT:
            return False  # 게임 오버
        return True

class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((300, 15))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)
        self.speed = 7
        self.keys = None

    def update(self):
        if self.keys and self.keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if self.keys and self.keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((60, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(MAGENTA)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vy = 3

    def update(self):
        self.rect.y += self.vy
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 15))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.vy = -10

    def update(self):
        self.rect.y += self.vy
        if self.rect.bottom < 0:
            self.kill()

# 게임 실행
def main():
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    large_font = pygame.font.Font(None, 72)
    
    # 스프라이트 그룹
    all_sprites = pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    items = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    
    # 패들 생성
    paddle = Paddle(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 30)
    all_sprites.add(paddle)
    
    # 공 생성
    ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    all_sprites.add(ball)
    
    # 블록 생성 (화려한 색상)
    colors = [CYAN, MAGENTA, ORANGE, LIME, PURPLE, RED, YELLOW, GREEN]
    for row in range(4):
        for col in range(12):
            x = col * 65 + 5
            y = row * 25 + 10
            color = colors[row % len(colors)]
            block = Block(x, y, color)
            all_sprites.add(block)
            blocks.add(block)
    
    score = 0
    running = True
    game_started = False
    has_weapon = False
    
    while running:
        clock.tick(60)
        keys = pygame.key.get_pressed()
        paddle.keys = keys
        
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_started:
                    game_started = True
                # 총알 발사
                if event.key == pygame.K_LCTRL and has_weapon and game_started:
                    bullet = Bullet(paddle.rect.centerx, paddle.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
        
        # 게임 시작 전
        if not game_started:
            screen.fill(BLACK)
            start_text = large_font.render("SPACE to Start", True, WHITE)
            start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(start_text, start_rect)
            pygame.display.flip()
            continue
        
        # 스프라이트 업데이트
        all_sprites.update()
        
        # 공이 화면 아래로 떨어졌는지 확인
        if not ball.update():
            print(f"게임 오버! 최종 점수: {score}")
            running = False
        
        # 패들과 공의 충돌
        if pygame.sprite.spritecollide(ball, pygame.sprite.Group(paddle), False):
            ball.vy *= -1
            ball.rect.bottom = paddle.rect.top
        
        # 블록과 공의 충돌
        hit_blocks = pygame.sprite.spritecollide(ball, blocks, True)
        for block in hit_blocks:
            ball.vy *= -1
            score += 10
            # 아이템 생성 (30% 확률)
            if random.random() < 0.3:
                item = Item(block.rect.centerx, block.rect.centery)
                all_sprites.add(item)
                items.add(item)
        
        # 패들과 아이템 충돌
        hit_items = pygame.sprite.spritecollide(paddle, items, True)
        for item in hit_items:
            has_weapon = True
            score += 50
        
        # 블록과 총알 충돌
        hit_blocks_by_bullet = pygame.sprite.groupcollide(blocks, bullets, True, True)
        for block in hit_blocks_by_bullet:
            score += 10
            # 아이템 생성 (30% 확률)
            if random.random() < 0.3:
                item = Item(block.rect.centerx, block.rect.centery)
                all_sprites.add(item)
                items.add(item)
        
        # 모든 블록 제거되면 승리
        if len(blocks) == 0:
            print(f"승리! 최종 점수: {score}")
            running = False
        
        # 화면 그리기
        screen.fill(BLACK)
        all_sprites.draw(screen)
        
        # 점수 표시
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # 무기 상태 표시
        if has_weapon:
            weapon_text = font.render("Weapon: ON (CTRL)", True, LIME)
        else:
            weapon_text = font.render("Weapon: OFF", True, RED)
        screen.blit(weapon_text, (SCREEN_WIDTH - 280, 10))
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()