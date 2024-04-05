import pygame

clock = pygame.time.Clock() #fps

pygame.init()
screen = pygame.display.set_mode((1200,675)) #screen

#изображения
pygame.display.set_caption("Forest defence")
start_bg = pygame.image.load("forest_icon.jpg")
pygame.display.set_icon(start_bg)
gname_bg = pygame.image.load("forest.jpg").convert()
player_right = pygame.image.load("right.png").convert_alpha()
player_left = pygame.image.load("left.png").convert_alpha()
enemy_right = pygame.image.load("enemy_right.png").convert_alpha()
enemy_left = pygame.image.load("enemy_left.png").convert_alpha()
pasxalka = pygame.image.load("meme.png").convert_alpha()
ammo = pygame.image.load("ammo.png").convert_alpha()

#переменные экрана,героя,врагов
enemyXRight = 1250
enemyYRight = 510
enemyXLeft = -50
enemyYLeft = 420
playerX = 600
playerY = 500
ammoX = playerX
ammoY = playerY
bg_x = 0
score = 0
player_speed = 10
jump_count = 12

count_left = 2500
count_right = 2000

last_player_direction = player_right
enemy_in_game_right = []
enemy_in_game_left = []
ammo_in_game_right = []
ammo_in_game_left = []
enemy_timer_right = pygame.USEREVENT + 1
enemy_timer_left = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer_right, count_right)
pygame.time.set_timer(enemy_timer_left, count_left)


scores = 1
best_score = 0

#Кнопки
label = pygame.font.Font("BungeeSpice-Regular.ttf",35)
lose_label = label.render("YOU LOSE",False,(255,255,255))
best_score_label = label.render("Best Score:",False,(255,255,255))
win_label = label.render("YOU WON",False,(255,255,255))
restart_lable = label.render("RESTART",False,(255,255,200))
restart_lable_rect = restart_lable.get_rect(topleft=(510,300))
znak_lable = label.render("BETA 1.0",False,(255,255,255))
start_lable = label.render("START",False,(255,255,200))
start_lable_rect = restart_lable.get_rect(topleft=(500,200))

close = label.render("EXIT",False,(255,255,200))
close_lable_rect = close.get_rect(topleft=(510,350))
isWon = False
start = 0
ammo_speed = 5

isJumping = False
isGameplay = False
isStart = True



while isStart:


    last_score = scores
    screen.blit(gname_bg, (bg_x, 0))
    screen.blit(gname_bg, (bg_x + 1200, 0))

    player_rect = last_player_direction.get_rect(topleft=(playerX,playerY))
    if isGameplay:
        # сложность и конец игры
        if scores >= 30000:
            isGameplay = False
            isWon = True
        if scores == 2000:
            count_right -= 500
            count_left -= 500
        scores += 1
        score_count = label.render("Score: " + str(scores), False, (117, 168, 240))
        screen.blit(score_count, (500,50))
        #enemies
        if enemy_in_game_right:
            for (i,el) in enumerate(enemy_in_game_right):
                screen.blit(enemy_left, (el))
                el.x -= 5 + (scores / 500)
                if el.x <= - 100:
                    enemy_in_game_right.pop(i)
                if player_rect.colliderect(el):
                    start += 1
                    isGameplay = False
        if enemy_in_game_left:
            for (i,el) in enumerate(enemy_in_game_left):
                screen.blit(enemy_left, (el))
                el.x += 5 + (scores / 300)
                if el.x >= 1250:
                    enemy_in_game_left.pop(i)
                if player_rect.colliderect(el):
                    start += 1
                    isGameplay = False
        if ammo_in_game_right:
            for (i,el) in enumerate(ammo_in_game_right):
                screen.blit(ammo,(el))
                el.x += 10
                if el.x >= 1250:
                   ammo_in_game_right.pop(i)
        if ammo_in_game_left:
            for (i,el) in enumerate(ammo_in_game_left):
                screen.blit(ammo,(el))
                el.x -= 10
                if el.x < -100:
                   ammo_in_game_left.pop(i)

        #нажатие клавиш
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(last_player_direction, (playerX, playerY))
            last_player_direction = player_left
        elif keys[pygame.K_RIGHT]:
            screen.blit(last_player_direction, (playerX, playerY))
            last_player_direction = player_right
        else:
            screen.blit(last_player_direction, (playerX, playerY))
        if playerX <= 0 or playerX >= 1100:
            isGameplay = False
            start += 1
        if keys[pygame.K_LEFT]:
            playerX -= player_speed + 2
        if keys[pygame.K_c] and last_player_direction == player_right:
            ammo_in_game_right.append(ammo.get_rect(topleft=(playerX, playerY)))
        if keys[pygame.K_c] and last_player_direction == player_left:
            ammo_in_game_left.append(ammo.get_rect(topleft=(playerX, playerY)))
        elif keys[pygame.K_RIGHT]:
            playerX += player_speed

        #прыжок
        if not isJumping:
            if keys[pygame.K_SPACE]:
                isJumping = True
        else:
            if jump_count >= -12:
                if jump_count > 0:
                    playerY -= (jump_count ** 2) / 6
                else:
                    playerY += (jump_count ** 2) / 6
                jump_count -= 0.5
            else:
                isJumping = False
                jump_count = 12
                player_speed = 10

        #движение игрока и фона
        ammoX += 5
        bg_x -= 2
        playerX -= 2
        if bg_x == -1200:
            bg_x = 0
    #меню
    else:
        score_label = label.render("Score: " + str(last_score), False, (255, 255, 255))
        screen.blit(znak_lable, (0, 0))
        screen.blit(start_bg, (0, 0))
        if start >= 1 and not isWon:
            screen.blit(pasxalka, (0, 0))
            screen.blit(lose_label, (500,200))
            screen.blit(restart_lable, restart_lable_rect)
            screen.blit(score_label, (500, 250))
        if start == 0 and not isWon:
            screen.blit(start_lable,start_lable_rect)
        screen.blit(close, close_lable_rect)
        mouse_pos = pygame.mouse.get_pos()
        if restart_lable_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            isGameplay = True
            scores = 0
            playerX = 600
            playerY = 500
            isJumping = False
            jump_count = 12
            enemy_in_game_right.clear()
            enemy_in_game_left.clear()
        if isWon:
            screen.blit(pasxalka, (0, 0))
            screen.blit(pasxalka, (700, 0))
            screen.blit(win_label, (500, 200))
            screen.blit(restart_lable, restart_lable_rect)
            screen.blit(score_label, (500, 250))

        if start_lable_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            isGameplay = True
        if close_lable_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            isStart = False

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isStart = False
            pygame.quit()
        if event.type == enemy_timer_right:
            enemy_in_game_right.append(enemy_left.get_rect(topleft=(enemyXRight, enemyYRight)))
        if event.type == enemy_timer_left:
            enemy_in_game_left.append(enemy_right.get_rect(topleft=(enemyXLeft, enemyYLeft)))
    clock.tick(60)
