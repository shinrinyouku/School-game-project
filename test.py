import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("StarWars Game")
clock = pygame.time.Clock()

x1, y1 = 0, 600
running = True
shoot_timer = 0
shooting = False
score = 0
hitpoints = 3
hit_line_y = 600
bullets = []
enemies = []
enemy_spawn_interval = 30
enemy_speed = 2

enemy_image = pygame.image.load('enemy.png')
enemy_image = pygame.transform.scale(enemy_image, (enemy_image.get_width() // 4, enemy_image.get_height() // 4))
enemy_image = pygame.transform.rotate(enemy_image, 180)

ally = pygame.image.load('ally.png')
ally = pygame.transform.scale(ally, (ally.get_width() // 6, ally.get_height() // 6))
w, h = ally.get_size()

def show_start_menu():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render("Press ENTER to Start", True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

def show_game_over():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render(f"Game Over! Final Score: {score}", True, (255, 255, 255))
    restart_text = font.render("Press Enter to Restart", True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return True
    return False

def draw_stars():
    for _ in range(100):
        x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 2)

show_start_menu()

move_right = move_left = move_up = move_down = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                move_right = True
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                move_left = True
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                move_up = True
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                move_down = True
            if event.key == pygame.K_SPACE:
                shooting = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                move_right = False
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                move_left = False
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                move_up = False
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                move_down = False
            if event.key == pygame.K_SPACE:
                shooting = False

    if move_right and x1 < WIDTH - w:
        x1 += 10
    if move_left and x1 > 0:
        x1 -= 10
    if move_up and y1 > 600:
        y1 -= 10
    if move_down and y1 < HEIGHT - h:
        y1 += 10

    screen.fill((0, 0, 0))
    draw_stars()
    pygame.draw.line(screen, (255, 255, 255), (0, hit_line_y), (WIDTH, hit_line_y), 2)

    if shooting and shoot_timer % 5 == 0:
        bullets.append([x1 + w // 2, y1])
    shoot_timer += 1
    
    for bullet in bullets[:]:
        bullet[1] -= 10
        pygame.draw.line(screen, (255, 0, 0), (bullet[0], bullet[1]), (bullet[0], bullet[1] - 20), 4)
        if bullet[1] < 0:
            bullets.remove(bullet)

    if shoot_timer % enemy_spawn_interval == 0:
        enemies.append([random.randint(0, WIDTH - enemy_image.get_width()), 0])
    
    for enemy in enemies[:]:
        enemy[1] += enemy_speed
        screen.blit(enemy_image, (enemy[0], enemy[1]))
        if enemy[1] >= hit_line_y-enemy_image.get_height():
            enemies.remove(enemy)
            hitpoints -= 1

    for enemy in enemies[:]:
        enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_image.get_width(), enemy_image.get_height())
        for bullet in bullets[:]:
            bullet_rect = pygame.Rect(bullet[0] - 2, bullet[1] - 20, 4, 20)
            if enemy_rect.colliderect(bullet_rect):
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 10
                break

    screen.blit(ally, (x1, y1))
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    
    for i in range(hitpoints):
        pygame.draw.circle(screen, (255, 0, 0), (WIDTH - 30 - i * 40, 30), 15)
    
    pygame.display.flip()
    clock.tick(60)
    
    if hitpoints <= 0:
        if show_game_over():
            x1, y1 = 0, 600
            running = True
            shoot_timer = 0
            shooting = False
            score = 0
            hitpoints = 3
            bullets.clear()
            enemies.clear()

pygame.quit()
sys.exit()