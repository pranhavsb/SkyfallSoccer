import pygame
import random


pygame.init()
pygame.display.set_caption("Clickball 2.0")
screen = pygame.display.set_mode((900, 600))


post = pygame.transform.scale(pygame.image.load('post.png'), (150, 100))
stad = pygame.transform.scale(pygame.image.load('stad.png'), (900, 600))
ball = pygame.transform.scale(pygame.image.load('ball.png'), (50, 50))
rugby = pygame.transform.scale(pygame.image.load('rugby.png'), (50, 50))


player_x = 375
player_y = 500


ball_x = []
ball_y = []
ball_speed = []

#rugby styff
rugby_x = random.randint(0, 850)
rugby_y = random.randint(-600, -100)
rugby_speed = 1.5

#ball stuff
current_balls = 1
max_balls = 5
score = 0
missed_balls = 0
max_missed_balls = 5
game_over = False
level = 1
columns = [False] * 9


for david in range(max_balls):
    ball_x.append(random.randint(0, 850))
    ball_y.append(random.randint(-300, -50))
    ball_speed.append(random.uniform(0.7, 1.2))


font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 60)


running = True

while running:
    screen.blit(stad, (0, 0))
    screen.blit(post, (player_x, player_y))

    if not game_over:
        #new ball coordinates
        for i in range(current_balls):
            ball_y[i] += ball_speed[i]
            screen.blit(ball, (ball_x[i], ball_y[i]))

            # check if ball is caught by postr
            if (
                player_y < ball_y[i] + 50 and
                player_x < ball_x[i] + 50 and
                player_x + 150 > ball_x[i]
            ):
                ball_y[i] = random.randint(-300, -50)
                column_index = ball_x[i] // 100
                ball_x[i] = random.choice([j * 100 for j in range(9) if not columns[j]])
                columns[column_index] = False
                ball_speed[i] += 0.01
                score += 1


                if score % 15 == 0 and current_balls < max_balls:
                    current_balls += 1


                if score % 15 == 0:
                    level += 1
                    max_missed_balls += 5

        #  chck if ball touch botom
        for i in range(current_balls):
            if ball_y[i] > 600:
                ball_y[i] = random.randint(-300, -50)
                column_index = ball_x[i] // 100
                ball_x[i] = random.choice([j * 100 for j in range(9) if not columns[j]])
                columns[column_index] = False
                missed_balls += 1


        if level > 1:
            rugby_y += rugby_speed
            screen.blit(rugby, (rugby_x, rugby_y))

            # if rugby caught, die
            if (
                player_y < rugby_y + 50 and
                player_x < rugby_x + 50 and
                player_x + 150 > rugby_x
            ):
                game_over = True

            # new rugby
            if rugby_y > 600:
                rugby_y = random.randint(-600, -100)
                rugby_x = random.randint(0, 850)

        # Display score, missed balls, and level
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        missed_text = font.render(f"Missed: {missed_balls}/{max_missed_balls}", True, (255, 0, 0))
        level_text = font.render(f"Level: {level}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(missed_text, (10, 50))
        screen.blit(level_text, (10, 90))


        if missed_balls >= max_missed_balls:
            game_over = True

    else:

        game_over_text = large_font.render("GAME OVER BRO!", True, (255, 0, 0))
        restart_text = font.render("Press R to Restart", True, (255, 255, 255))
        final_score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
        screen.blit(game_over_text, (300, 200))
        screen.blit(final_score_text, (350, 280))
        screen.blit(restart_text, (330, 350))


    pygame.display.update()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Restart stats
        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            score = 0
            missed_balls = 0
            max_missed_balls = 5
            current_balls = 1
            level = 1
            rugby_y = random.randint(-600, -100)
            rugby_x = random.randint(0, 850)
            for i in range(max_balls):
                ball_y[i] = random.randint(-300, -50)
                ball_x[i] = random.randint(0, 850)
                ball_speed[i] = random.uniform(0.7, 1.2)
            game_over = False

    #player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= 5
    if keys[pygame.K_RIGHT] and player_x < 750:  # 900 - post width
        player_x += 5


pygame.quit()
