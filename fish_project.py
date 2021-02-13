"""
Created on Fri May 25 17:12:20 2018
@author: Francois, Jillian
"""

import pygame
import time
import random
import settings
import entities

pygame.init()

gameDisplay = pygame.display.set_mode((settings.DISPLAY_WIDTH, settings.DISPLAY_HEIGHT))
pygame.display.set_caption('A fishy situation')
clock = pygame.time.Clock()


# import images
Life_img = pygame.transform.scale(pygame.image.load('resources/life.png'), (20, 20))
Banana_img = pygame.transform.scale(pygame.image.load('resources/banana.png'), (30, 30))


# Definitions
def food(foodx, foody, foodw, color):
    pygame.draw.circle(gameDisplay, color, (foodx, foody), foodw)


def extra_food(extra_food_x, extra_food_y, foodw, color):
    for i in range(len(extra_food_y)):
        pygame.draw.circle(gameDisplay, color, (extra_food_x[i], extra_food_y[i]), foodw)


def Display_Score(highscore, score, lives):
    font = pygame.font.SysFont(None, 25)
    text1 = font.render("Highscore: " + str(highscore), True, settings.BLACK)
    gameDisplay.blit(text1, (3, 3))
    text2 = font.render("Score: " + str(score), True, settings.BLACK)
    gameDisplay.blit(text2, (3, 23))
    for i in range(lives):
        gameDisplay.blit(Life_img, (3+i*30, 43))


def mort():
    GameOver_Display('No more lives left :(')


def GameOver_Display(texte):
    textefont = pygame.font.SysFont('comicsansms', 72)
    textSurface = textefont.render(texte, True, settings.BLACK)
    TextSurf,  TextRect = textSurface, textSurface.get_rect()
    TextRect.center = ((settings.DISPLAY_WIDTH/2), (settings.DISPLAY_HEIGHT/2))
    gameDisplay.fill(settings.BLUE)
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
    x_change = 0
    y_change = 0
    # food position
    food_x = random.randrange(1, settings.DISPLAY_WIDTH)
    food_y = 0
    food_radius = 5
    food_speed = 2
    # Score
    score = 0
    highscore = 0
    lives = 3
    # Big fish starting point
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
    life_x = random.randrange(0, settings.DISPLAY_WIDTH)
    life_y = 0
    # other
    framecount = 0
    gameExit = False

    my_fish_entity = entities.MyFish()
    big_fish_entity = entities.BigFish()

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
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_UP:
                    y_change = -5
                if event.key == pygame.K_DOWN:
                    y_change = 5

                # for multiplayer
                if event.key == pygame.K_a:
                    x_change = -5
                if event.key == pygame.K_d:
                    x_change = 5
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

        my_fish_entity.move(x_change, y_change)

        # ===  DISPLAY ===

        gameDisplay.fill(settings.BLUE)
        food(food_x, food_y, food_radius, settings.ORANGE)
        gameDisplay.blit(my_fish_entity.get_img(), my_fish_entity.pos)
        gameDisplay.blit(big_fish_entity.get_img(), big_fish_entity.pos)
        Display_Score(highscore, score, lives)

        # === EVENTS ===

        # falling food
        if food_y > settings.DISPLAY_HEIGHT:
            # food_y = -random.randrange(0, settings.DISPLAY_WIDTH) - food_radius
            food_y = 0 - food_radius
            food_x = random.randrange(0, settings.DISPLAY_WIDTH)
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
                extra_food_special_x = random.randrange(1, settings.DISPLAY_WIDTH-30)
                extra_food_special_y = 0
                once_extrafood = 1

            if draw:
                # pygame.draw.circle(gameDisplay, settings.RED, (extra_food_special_x, extra_food_special_y), food_radius+1)
                gameDisplay.blit(Banana_img, (extra_food_special_x, extra_food_special_y))
                extra_food_special_y += 1

            # for my_fish_entity
            # ======================
            if extra_food_special_x + 30 > my_fish_entity.pos.x and extra_food_special_x < my_fish_entity.pos.x + my_fish_entity.width and extra_food_special_y + 30 > my_fish_entity.pos.y and extra_food_special_y < my_fish_entity.pos.y + my_fish_entity.height:
                extra_food_special_y = settings.DISPLAY_HEIGHT
                draw = False
                # start_bonus_food = 1
                start_time = time.process_time()
                start_bonus_food = 1
            # ======================

            if extra_food_special_y > settings.DISPLAY_HEIGHT:
                extrafood = 0
                once_extrafood = 0

        if start_bonus_food == 1:
            elapsed_time = time.process_time() - start_time

            if elapsed_time < 3 and framecount == 1 or elapsed_time < 3 and framecount == 15 or elapsed_time < 3 and framecount == 30 or elapsed_time < 3 and framecount == 45:
                extra_food_x.append(random.randrange(1, settings.DISPLAY_WIDTH))
                extra_food_y.append(0)
            extra_food_y = [a+food_speed for a in extra_food_y]
            extra_food(extra_food_x, extra_food_y, food_radius, settings.ORANGE)

            if elapsed_time > 3 and min(extra_food_y) > settings.DISPLAY_HEIGHT:
                start_bonus_food = 0

        # extra life special:
        if extra_life == 1:
            if once_life == 0:
                life_x = random.randrange(0, settings.DISPLAY_WIDTH - 20)
                life_y = -20
                once_life = 1
            gameDisplay.blit(Life_img, (life_x, life_y))
            life_y += 1

        if life_x > my_fish_entity.pos.x and life_x < my_fish_entity.pos.x + my_fish_entity.width and life_y > my_fish_entity.pos.y and life_y < my_fish_entity.pos.y + my_fish_entity.height:
            life_y = settings.DISPLAY_HEIGHT
            lives += 1

        if life_y > settings.DISPLAY_HEIGHT:
            extra_life = 0
            once_life = 0

        # fish catches food
        for i in range(len(extra_food_x)):
            if extra_food_x[i] > my_fish_entity.pos.x and extra_food_x[i] < my_fish_entity.pos.x + my_fish_entity.width and extra_food_y[i] > my_fish_entity.pos.y and extra_food_y[i] < my_fish_entity.pos.y + my_fish_entity.height:
                extra_food_y[i] = settings.DISPLAY_HEIGHT
                score += 1
                my_fish_entity.grow()
        if food_x > my_fish_entity.pos.x and food_x < my_fish_entity.pos.x + my_fish_entity.width and food_y > my_fish_entity.pos.y and food_y < my_fish_entity.pos.y + my_fish_entity.height:
            food_y = settings.DISPLAY_HEIGHT
            score += 1
            my_fish_entity.grow()

        big_fish_entity.wander()

        scale = 25
        # vel
        pygame.draw.line(gameDisplay, settings.GREEN, big_fish_entity.pos, (big_fish_entity.pos + big_fish_entity.vel * scale), 5)
        # desired
        pygame.draw.line(gameDisplay, settings.RED, big_fish_entity.pos, (big_fish_entity.pos + big_fish_entity.desired * scale), 5)
        # target
        center = big_fish_entity.pos + big_fish_entity.vel.normalize() * entities.WANDER_RING_DISTANCE
        pygame.draw.circle(gameDisplay, settings.WHITE, (int(center.x), int(center.y)), entities.WANDER_RING_RADIUS, 1)
        pygame.draw.line(gameDisplay, settings.CYAN, center, big_fish_entity.displacement, 5)

        # Collision Bigfish/myfish
        if my_fish_entity.pos.x+my_fish_entity.width > big_fish_entity.pos.x and my_fish_entity.pos.x < big_fish_entity.pos.x + big_fish_entity.width and my_fish_entity.pos.y + my_fish_entity.height > big_fish_entity.pos.y + 30 and my_fish_entity.pos.y < big_fish_entity.pos.y + big_fish_entity.height-20:
            if my_fish_entity.can_take_revenge:
                BigFish_dead = 1
                my_fish_entity.eat(big_fish_entity)
            else:
                big_fish_entity.eat(my_fish_entity)

        # Highscore calculation
        if score > highscore:
            highscore = score

        if my_fish_entity.lives == 0:
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
