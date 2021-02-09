"""
Created on Fri May 25 17:12:20 2018
@author: Francois, Jillian
"""
# j'ai fixe lives a -10 et mouvement initial du Big fish a 0 pour faciliter le developpement.

import pygame
import time
import random

pygame.init()

display_width = 900
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('A fishy situation')
clock = pygame.time.Clock()

# colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (19, 187, 255)
food_color = (255, 187, 19)

# variables
fish_width = 60
fish_height = 35

BigFish_width = 250
BigFish_height = 120


# import images
Fish_l_raw = pygame.image.load('resources/Fish_l.png')
Fish_r_raw = pygame.transform.flip(Fish_l_raw, 1, 0)

BigFish = pygame.image.load('resources/Bigfish.png')
BigFish_l = pygame.transform.scale(BigFish, (BigFish_width, BigFish_height))
BigFish_r = pygame.transform.flip(BigFish_l, 1,  0)

Life = pygame.image.load('resources/life.png')
Life = pygame.transform.scale(Life, (20, 20))

Banana = pygame.image.load('resources/banana.png')
Banana = pygame.transform.scale(Banana, (30, 30))

angry_Fish_l_raw = pygame.image.load('resources/angry_fish.png')
angry_Fish_r_raw = pygame.transform.flip(angry_Fish_l_raw, 1, 0)


# Definitions
def Myfish(x, y, orientation, score, Fish_l_raw, Fish_r_raw, fish_width, fish_height, can_eat_Bigfish):

    Fish_l = pygame.transform.scale(Fish_l_raw, (fish_width, fish_height))
    Fish_r = pygame.transform.scale(Fish_r_raw,  (fish_width, fish_height))

    angry_Fish_l = pygame.transform.scale(angry_Fish_l_raw, (fish_width, fish_height))
    angry_Fish_r = pygame.transform.scale(angry_Fish_r_raw, (fish_width, fish_height))
    if can_eat_Bigfish == 0:
        if fish_width < 115:
            if orientation == 'l':
                gameDisplay.blit(Fish_l, (x, y))
                # pygame.draw.rect(gameDisplay, red, (x, y, fish_width, fish_height), 2)
            if orientation == 'r':
                gameDisplay.blit(Fish_r, (x, y))

        if fish_width > 115:
            if orientation == 'l':
                gameDisplay.blit(Fish_l, (x, y))
            if orientation == 'r':
                gameDisplay.blit(Fish_r, (x, y))
            can_eat_Bigfish = 1

    if can_eat_Bigfish == 1:
        if fish_width < 160:
            if orientation == 'l':
                gameDisplay.blit(angry_Fish_l, (x, y))
            if orientation == 'r':
                gameDisplay.blit(angry_Fish_r, (x, y))

        if fish_width > 160:
            if orientation == 'l':
                gameDisplay.blit(angry_Fish_l, (x, y))
            if orientation == 'r':
                gameDisplay.blit(angry_Fish_r, (x, y))
            can_eat_Bigfish = 1

    return can_eat_Bigfish


def fish_evolution(score, fish_width, fish_height, run_once):

    if score >= 2 and run_once == 0:
        fish_width += round(fish_width*0.3)
        fish_height += round(fish_height*0.3)
        run_once = 1
    if score >= 5 and run_once == 1:
        fish_width += round(fish_width*0.3)
        fish_height += round(fish_height*0.3)
        run_once = 2
    if score >= 10 and run_once == 2:
        fish_width += round(fish_width*0.3)
        fish_height += round(fish_height*0.3)
        run_once = 3
    if score >= 15 and run_once == 3:
        fish_width += round(fish_width*0.3)
        fish_height += round(fish_height*0.3)
        run_once = 4
    if score >= 20 and run_once == 4:
        fish_width += round(fish_width*0.5)
        fish_height += round(fish_height*0.5)
        run_once = 5

    return fish_width, fish_height, run_once


def food(foodx, foody, foodw, color):
    pygame.draw.circle(gameDisplay, color, (foodx, foody), foodw)


def extra_food(extra_food_x, extra_food_y, foodw, color):
    for i in range(len(extra_food_y)):
        pygame.draw.circle(gameDisplay, color, (extra_food_x[i], extra_food_y[i]), foodw)


def Display_Score(highscore, score, lives):
    font = pygame.font.SysFont(None, 25)
    text1 = font.render("Highscore: " + str(highscore), True, black)
    gameDisplay.blit(text1, (3, 3))
    text2 = font.render("Score: " + str(score), True, black)
    gameDisplay.blit(text2, (3, 23))
    for i in range(lives):
        gameDisplay.blit(Life, (3+i*30, 43))


def mort():
    GameOver_Display('No more lives left :(')


def GameOver_Display(texte):
    textefont = pygame.font.SysFont('comicsansms', 72)
    textSurface = textefont.render(texte, True, black)
    TextSurf,  TextRect = textSurface, textSurface.get_rect()
    TextRect.center = ((display_width/2), (display_height/2))
    gameDisplay.fill(blue)
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.flip()


def Bigfish(Bigfish_x, Bigfish_y, orientation_bigfish, BigFish_dead):
    if BigFish_dead == 0:
        if orientation_bigfish == 'l':
            gameDisplay.blit(BigFish_l, (Bigfish_x, Bigfish_y))
        if orientation_bigfish == 'r':
            gameDisplay.blit(BigFish_r, (Bigfish_x, Bigfish_y))
    if BigFish_dead == 1:
        BigFishDead = pygame.transform.flip(BigFish_l, 0, 1)
        gameDisplay.blit(BigFishDead, (Bigfish_x, Bigfish_y))


def game_loop():

    # LOCAL VARIABLES #
    # frames per second
    fps = 60
    # My fish starting point:
    x = (display_width * 0.45)
    y = (display_height * 0.8)
    orientation = 'l'
    fish_width = 40
    fish_height = 25
    can_eat_Bigfish = 0
    # fish position change
    x_change = 0
    y_change = 0
    # food position
    food_x = random.randrange(1, display_width)
    food_y = 0
    food_radius = 5
    food_speed = 2
    # Score
    score = 0
    highscore = 0
    lives = 3
    # Big fish starting point
    Bigfish_x = (display_width * 0.40)
    Bigfish_y = (display_width * 0.45)
    Bigfish_x_change = 2
    Bigfish_y_change = -2
    tracking_x = 0
    tracking_y = 0
    orientation_bigfish = 'l'
    BigFish_dead = 0
    # extra food special
    extrafood = 0
    once_extrafood = 0
    start_bonus_food = 0
    extra_food_x = []
    extra_food_y = []
    # extra life special
    extra_life = 0
    once_life = 0
    # proba = random.randrange(0, 100)/100
    life_x = random.randrange(0, display_width)
    life_y = 0
    # other
    framecount = 0
    run_once = 0
    gameExit = False

    while not gameExit:
        # === KEYS ===
        # Quit key
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

                # Movement keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                    orientation = 'l'
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                    orientation = 'r'
                if event.key == pygame.K_UP:
                    y_change = -5
                if event.key == pygame.K_DOWN:
                    y_change = 5

                # for multiplayer
                if event.key == pygame.K_a:
                    x_change = -5
                    orientation = 'l'
                if event.key == pygame.K_d:
                    x_change = 5
                    orientation = 'r'
                if event.key == pygame.K_w:
                    y_change = -5
                if event.key == pygame.K_s:
                    y_change = 5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    x_change = 0
                if event.key == pygame.K_RIGHT:
                    x_change = 0
                if event.key == pygame.K_UP:
                    y_change = 0
                if event.key == pygame.K_DOWN:
                    y_change = 0
                # for multiplayer
                if event.key == pygame.K_a:
                    x_change = 0
                if event.key == pygame.K_d:
                    x_change = 0
                if event.key == pygame.K_w:
                    y_change = 0
                if event.key == pygame.K_s:
                    y_change = 0
        x += x_change
        y += y_change

        # === BOUNDARIES ===

        # define boundaries for fish movement on on display
        if x > display_width - fish_width:
            x = display_width - fish_width
        if x < 0:
            x = 0
        if y > display_height - fish_height:
            y = display_height - fish_height
        if y < 0:
            y = 0

        # ===  DISPLAY ===

        gameDisplay.fill(blue)
        # if extrafood != 1:
        food(food_x, food_y, food_radius, food_color)
        Bigfish(Bigfish_x, Bigfish_y, orientation_bigfish, BigFish_dead)
        can_eat_Bigfish = Myfish(x, y, orientation, score, Fish_l_raw, Fish_r_raw, fish_width, fish_height, can_eat_Bigfish)
        Display_Score(highscore, score, lives)

        # === EVENTS ===

        # falling food
        if food_y > display_height:
            # food_y = -random.randrange(0, display_width) - food_radius
            food_y = 0 - food_radius
            food_x = random.randrange(0, display_width)
        food_y += food_speed

        # Condition for Specials
        if random.randrange(1, 100*60) < 5:
            extrafood = 1

        if random.randrange(1, 100*60) < 3:  # 5 chances sur 100 par secondes
            extra_life = 1

        # Extra food special
        if extrafood == 1:
            draw = True

            if once_extrafood == 0:
                extra_food_special_x = random.randrange(1, display_width-30)
                extra_food_special_y = 0
                once_extrafood = 1

            if draw:
                # pygame.draw.circle(gameDisplay, red, (extra_food_special_x, extra_food_special_y), food_radius+1)
                gameDisplay.blit(Banana, (extra_food_special_x, extra_food_special_y))
                extra_food_special_y += 1

            if extra_food_special_x + 30 > x and extra_food_special_x < x + fish_width and extra_food_special_y + 30 > y and extra_food_special_y < y + fish_height:
                extra_food_special_y = display_height
                draw = False
                # start_bonus_food = 1
                start_time = time.process_time()
                start_bonus_food = 1

            if extra_food_special_y > display_height:
                extrafood = 0
                once_extrafood = 0

        if start_bonus_food == 1:
            elapsed_time = time.process_time() - start_time

            if elapsed_time < 3 and framecount == 1 or elapsed_time < 3 and framecount == 15 or elapsed_time < 3 and framecount == 30 or elapsed_time < 3 and framecount == 45:
                extra_food_x.append(random.randrange(1, display_width))
                extra_food_y.append(0)
            extra_food_y = [a+food_speed for a in extra_food_y]
            extra_food(extra_food_x, extra_food_y, food_radius, food_color)

            if elapsed_time > 3 and min(extra_food_y) > display_height:
                start_bonus_food = 0

        # extra life special:
        if extra_life == 1:
            if once_life == 0:
                life_x = random.randrange(0, display_width - 20)
                life_y = -20
                once_life = 1
            gameDisplay.blit(Life, (life_x, life_y))
            life_y += 1

        if life_x > x and life_x < x + fish_width and life_y > y and life_y < y + fish_height:
            life_y = display_height
            lives += 1

        if life_y > display_height:
            extra_life = 0
            once_life = 0

        # fish catches food
        # if extrafood==1:
        for i in range(len(extra_food_x)):
            if extra_food_x[i] > x and extra_food_x[i] < x + fish_width and extra_food_y[i] > y and extra_food_y[i] < y + fish_height:
                extra_food_y[i] = display_height
                score += 1
        else:
            if food_x > x and food_x < x + fish_width and food_y > y and food_y < y + fish_height:
                food_y = display_height
                score += 1

        fish_width, fish_height, run_once = fish_evolution(score, fish_width, fish_height, run_once)

        # Big fish
        if Bigfish_x_change > 0:
            orientation_bigfish = 'r'
        else:
            orientation_bigfish = 'l'
        if BigFish_dead == 0:
            if Bigfish_x > display_width - BigFish_width or tracking_x > random.randrange(0, display_width):
                Bigfish_x_change = -3
                tracking_x = 0
            if Bigfish_x < 0 or tracking_x > random.randrange(0, display_width):
                Bigfish_x_change = 3
                tracking_x = 0
            if Bigfish_y > display_height - BigFish_height or tracking_y > random.randrange(0, display_height):
                Bigfish_y_change = -3
                tracking_y = 0
            if Bigfish_y < 0 or tracking_y > random.randrange(0, display_height):
                Bigfish_y_change = 3
                tracking_y = 0
        if BigFish_dead == 1:
            Bigfish_x_change = 0
            Bigfish_y_change = -2

        Bigfish_x += Bigfish_x_change
        Bigfish_y += Bigfish_y_change
        tracking_x += abs(Bigfish_x_change)/fps
        tracking_y += abs(Bigfish_y_change)/fps

        # Bigfish catches myfish
        if can_eat_Bigfish == 0:
            if x+fish_width > Bigfish_x and x < Bigfish_x + BigFish_width and y + fish_height > Bigfish_y + 30 and y < Bigfish_y + BigFish_height-20:
                y = 0
                x = 0
                lives -= 1

        # Myfish eats bigfish
        if can_eat_Bigfish == 1:
            if x+fish_width > Bigfish_x and x < Bigfish_x + BigFish_width and y + fish_height > Bigfish_y + 30 and y < Bigfish_y + BigFish_height-20:
                BigFish_dead = 1

        # Highscore calculation
        if score > highscore:
            highscore = score

        # out of lives
        if lives < 1:
            mort()
            time.sleep(2)
            pygame.quit()
            quit()

        # frame counter
        if framecount > 59:
            framecount = 0
        else:
            framecount += 1

        pygame.display.update()
        clock.tick(fps)


game_loop()
pygame.quit()
quit()
