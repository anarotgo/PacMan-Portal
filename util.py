class Util:
    def draw_misc(font, score, screen, powerup, pygame, lives, player_images, game_over, game_won):
        score_text = font.render(f'Score: {score}', True, 'white')
        screen.blit(score_text, (10, 920))
        if powerup:
            pygame.draw.circle(screen, 'blue', (140, 930), 15)
        for i in range(lives):
            screen.blit(pygame.transform.scale(player_images[0], (30, 30)), (650 + i * 40, 915))
        if game_over:
            pygame.draw.rect(screen, 'white', [50, 200, 800, 300],0, 10)
            pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
            gameover_text = font.render('Game over! Space bar to restart!', True, 'red')
            screen.blit(gameover_text, (100, 300))
        if game_won:
            pygame.draw.rect(screen, 'white', [50, 200, 800, 300],0, 10)
            pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
            gameover_text = font.render('Victory! Space bar to restart!', True, 'green')
            screen.blit(gameover_text, (100, 300))

    def check_collisions(scor, power, power_count, eaten_ghost, HEIGHT, WIDTH, player_x, level,center_x, center_y):
        num1 = (HEIGHT - 50) // 32
        num2 = WIDTH // 30
        if 0 < player_x < 870:
            if level[center_y // num1][center_x // num2] == 1:
                level[center_y // num1][center_x // num2] = 0
                scor += 10
            if level[center_y // num1][center_x // num2] == 2:
                level[center_y // num1][center_x // num2] = 0
                scor += 50
                power = True
                power_count = 0
                eaten_ghost = [False, False, False, False]
        return scor, power, power_count, eaten_ghost

    def draw_board(HEIGHT, WIDTH, level, pygame, screen, flicker, color, PI): #(HEIGHT, WIDTH, level, pygame, screen, flicker, color, PI
        num1 = ((HEIGHT - 50) // 32)
        num2 = (WIDTH // 30)
        for i in range(len(level)):
            for j in range(len(level[i])):
                if level[i][j] == 1:
                    pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
                if level[i][j] == 2 and not flicker:
                    pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
                if level[i][j] == 3:
                    pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1),
                                    (j * num2 + (0.5 * num2), i * num1 + num1), 3)
                if level[i][j] == 4:
                    pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)),
                                    (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
                if level[i][j] == 5:
                    pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1],
                                    0, PI / 2, 3)
                if level[i][j] == 6:
                    pygame.draw.arc(screen, color,
                                    [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 3)
                if level[i][j] == 7:
                    pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI,
                                    3 * PI / 2, 3)
                if level[i][j] == 8:
                    pygame.draw.arc(screen, color,
                                    [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2,
                                    2 * PI, 3)
                if level[i][j] == 9:
                    pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                    (j * num2 + num2, i * num1 + (0.5 * num1)), 3)

    def draw_player(direction, screen, player_images, counter, player_x, player_y, pygame):
        # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
        if direction == 0:
            screen.blit(player_images[counter // 5], (player_x, player_y))
        elif direction == 1:
            screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
        elif direction == 2:
            screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
        elif direction == 3:
            screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))

    def check_position(centerx, centery, HEIGHT, WIDTH, direction, level):
        turns = [False, False, False, False]
        num1 = (HEIGHT - 50) // 32
        num2 = (WIDTH // 30)
        num3 = 15
        # check collisions based on center x and center y of player +/- fudge number
        if centerx // 30 < 29:
            if direction == 0:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
            if direction == 1:
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
            if direction == 2:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
            if direction == 3:
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True

            if direction == 2 or direction == 3:
                if 12 <= centerx % num2 <= 18:
                    if level[(centery + num3) // num1][centerx // num2] < 3:
                        turns[3] = True
                    if level[(centery - num3) // num1][centerx // num2] < 3:
                        turns[2] = True
                if 12 <= centery % num1 <= 18:
                    if level[centery // num1][(centerx - num2) // num2] < 3:
                        turns[1] = True
                    if level[centery // num1][(centerx + num2) // num2] < 3:
                        turns[0] = True
            if direction == 0 or direction == 1:
                if 12 <= centerx % num2 <= 18:
                    if level[(centery + num1) // num1][centerx // num2] < 3:
                        turns[3] = True
                    if level[(centery - num1) // num1][centerx // num2] < 3:
                        turns[2] = True
                if 12 <= centery % num1 <= 18:
                    if level[centery // num1][(centerx - num3) // num2] < 3:
                        turns[1] = True
                    if level[centery // num1][(centerx + num3) // num2] < 3:
                        turns[0] = True
        else:
            turns[0] = True
            turns[1] = True

        return turns


    def move_player(play_x, play_y, direction, turns_allowed, player_speed):
        # r, l, u, d
        if direction == 0 and turns_allowed[0]:
            play_x += player_speed
        elif direction == 1 and turns_allowed[1]:
            play_x -= player_speed
        if direction == 2 and turns_allowed[2]:
            play_y -= player_speed
        elif direction == 3 and turns_allowed[3]:
            play_y += player_speed
        return play_x, play_y


    def get_targets(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y,
                    player_x, player_y, powerup, blinky, eaten_ghost, inky, pinky, clyde):
        if player_x < 450:
            runaway_x = 900
        else:
            runaway_x = 0
        if player_y < 450:
            runaway_y = 900
        else:
            runaway_y = 0
        return_target = (380, 400)
        if powerup:
            if not blinky.dead and not eaten_ghost[0]:
                blink_target = (runaway_x, runaway_y)
            elif not blinky.dead and eaten_ghost[0]:
                if 340 < blink_x < 560 and 340 < blink_y < 500:
                    blink_target = (400, 100)
                else:
                    blink_target = (player_x, player_y)
            else:
                blink_target = return_target
            if not inky.dead and not eaten_ghost[1]:
                ink_target = (runaway_x, player_y)
            elif not inky.dead and eaten_ghost[1]:
                if 340 < ink_x < 560 and 340 < ink_y < 500:
                    ink_target = (400, 100)
                else:
                    ink_target = (player_x, player_y)
            else:
                ink_target = return_target
            if not pinky.dead:
                pink_target = (player_x, runaway_y)
            elif not pinky.dead and eaten_ghost[2]:
                if 340 < pink_x < 560 and 340 < pink_y < 500:
                    pink_target = (400, 100)
                else:
                    pink_target = (player_x, player_y)
            else:
                pink_target = return_target
            if not clyde.dead and not eaten_ghost[3]:
                clyd_target = (450, 450)
            elif not clyde.dead and eaten_ghost[3]:
                if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                    clyd_target = (400, 100)
                else:
                    clyd_target = (player_x, player_y)
            else:
                clyd_target = return_target
        else:
            if not blinky.dead:
                if 340 < blink_x < 560 and 340 < blink_y < 500:
                    blink_target = (400, 100)
                else:
                    blink_target = (player_x, player_y)
            else:
                blink_target = return_target
            if not inky.dead:
                if 340 < ink_x < 560 and 340 < ink_y < 500:
                    ink_target = (400, 100)
                else:
                    ink_target = (player_x, player_y)
            else:
                ink_target = return_target
            if not pinky.dead:
                if 340 < pink_x < 560 and 340 < pink_y < 500:
                    pink_target = (400, 100)
                else:
                    pink_target = (player_x, player_y)
            else:
                pink_target = return_target
            if not clyde.dead:
                if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                    clyd_target = (400, 100)
                else:
                    clyd_target = (player_x, player_y)
            else:
                clyd_target = return_target
        return [blink_target, ink_target, pink_target, clyd_target]
    
    def load_images(player_images, pygame):
        for i in range(1, 5):
            player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (45, 45)))
        
        blinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/red.png'), (45, 45))
        pinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/pink.png'), (45, 45))
        inky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/blue.png'), (45, 45))
        clyde_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/orange.png'), (45, 45))
        spooked_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/powerup.png'), (45, 45))
        dead_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/dead.png'), (45, 45))
        return blinky_img, pinky_img, inky_img, clyde_img, spooked_img, dead_img