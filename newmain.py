import pygame
import random
import sys


pygame.init()


WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("StarWars Game")


clock = pygame.time.Clock()


x1, y1 = 0, 600
moving = False
running = True


shoot_timer = 0
shoot_interval = 10
shooting_lines = []


enemies = []
enemy_spawn_timer = 0
enemy_spawn_interval = 30  


enemy = pygame.image.load('enemy.png')
enemy = pygame.transform.scale(enemy, (enemy.get_width() // 4, enemy.get_height() // 4))
enemy = pygame.transform.rotate(enemy, 180)


ally = pygame.image.load('ally.png')
ally = pygame.transform.scale(ally, (ally.get_width() // 6, ally.get_height() // 6))
w, h = ally.get_size()



allowed_area_y = (2 * HEIGHT // 3, HEIGHT)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        if event.type == pygame.KEYDOWN:
            if ( event.key == pygame.K_RIGHT or event.key == pygame.K_d) and x1<WIDTH-w:
                    x1 += 50  
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and x1>0:
                    x1 -= 50 
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and y1>600:
                    y1 -= 50  
            if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and y1<HEIGHT-h:
                    y1 += 50


    screen.fill((0, 0, 0))
    sur = pygame.Surface((400, 400), pygame.SRCALPHA)
    sur2 = pygame.Surface((400, 400), pygame.SRCALPHA)
    

    for i in range(100):
        x3 = 20
        y3 = 20
        x4 = 28
        y4 = 28
        x5 = random.randint(0, WIDTH)
        y5 = random.randint(0, HEIGHT)
        x6 = random.randint(0, WIDTH)
        y6 = random.randint(0, HEIGHT)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        color2 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        pygame.draw.line(sur, color, (x3, y3), (x4, y4), 2)
        pygame.draw.line(sur2, color2, (x3, y3), (x4, y4), 2)
        screen.blit(sur, (x5, y5))
        screen.blit(sur2, (x6, y6))
        

    if moving and shoot_timer == 0:
        shooting_lines.append((x1 + w // 2, y1))
    shoot_timer = (shoot_timer + 1) % shoot_interval  

    
    for line in shooting_lines[:]:
        start_x, start_y = line
        pygame.draw.line(screen, (255, 0, 0), (start_x, start_y), (start_x, start_y - 20), 4)
        if start_y - 20 > 0:
            shooting_lines[shooting_lines.index(line)] = (start_x, start_y - 10)
        else:
            shooting_lines.remove(line)


    if enemy_spawn_timer == 0:
        enemy_x = random.randint(0, WIDTH - enemy.get_width())
        enemies.append([enemy_x, 0])  
    enemy_spawn_timer = (enemy_spawn_timer + 1) % enemy_spawn_interval


    for i in enemies[:]:
        i[1] += 4  
        screen.blit(enemy, (int(i[0]), int(i[1])))
        if i[1] > 2*HEIGHT/3:  
            enemies.remove(i)

    font = pygame.font.Font(None, 50) 
    text_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) 
    text = font.render("StarWars", True, text_color)
    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = HEIGHT // 2 - text.get_height() //2
    text_w = text.get_width()
    text_h = text.get_height()

    screen.blit(text, (WIDTH/2-text_w/2, HEIGHT/4)) 
    screen.blit(ally, (x1, y1))
    pygame.display.flip()


    clock.tick(60)


pygame.quit()
sys.exit()