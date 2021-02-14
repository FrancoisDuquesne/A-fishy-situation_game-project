"""
Created on Fri May 25 17:12:20 2018
@author: Francois, Jillian
"""

import pygame
import time
import random
from pygame.sprite import Sprite
import settings
import entities

vec = pygame.math.Vector2

pygame.init()

pygame.display.set_caption('A fishy situation')
clock = pygame.time.Clock()


# import images
Life_img = pygame.transform.scale(pygame.image.load('resources/life.png'), (20, 20))
Banana_img = pygame.transform.scale(pygame.image.load('resources/banana.png'), (30, 30))


class FoodPebble(Sprite):
    def __init__(self):
        super(FoodPebble, self).__init__()
        self.radius = 5
        self.speed = 1
        self.color = settings.ORANGE
        self.pos = vec(random.randrange(1, settings.DISPLAY_WIDTH), 0)
        # raw_img = pygame.image.load('resources/Fish_l.png')
        # self.image = pygame.transform.scale(raw_img, (self.width, self.height))
        self.image = pygame.Surface([self.radius, self.radius])
        self.image.fill(settings.ORANGE)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos + vec(self.radius/2, self.radius/2)

    def draw(self, screen):
        self.image = pygame.draw.circle(screen, self.color, self.pos, self.radius)

    def fall(self):
        if self.pos.y > settings.DISPLAY_HEIGHT:
            self.pos = vec(random.randrange(0, settings.DISPLAY_WIDTH), 0 - self.radius)
        else:
            self.pos.y += self.speed
            self.rect.center = self.pos + vec(self.radius/2, self.radius/2)

    def update(self, screen):
        self.fall()
        self.draw(screen)


def game_loop():
    screen = pygame.display.set_mode((settings.DISPLAY_WIDTH, settings.DISPLAY_HEIGHT))

    # Definitions
    def extra_food(extra_food_x, extra_food_y, foodw, color):
        for i in range(len(extra_food_y)):
            pygame.draw.circle(screen, color, (extra_food_x[i], extra_food_y[i]), foodw)

    def Display_Score(highscore, score, lives):
        font = pygame.font.SysFont('calibri', 25)
        text1 = font.render("Highscore: " + str(highscore), True, settings.BLACK)
        screen.blit(text1, (3, 3))
        text2 = font.render("Score: " + str(score), True, settings.BLACK)
        screen.blit(text2, (3, 23))
        for i in range(lives):
            screen.blit(Life_img, (3+i*30, 43))

    def GameOver_Display(texte):
        textefont = pygame.font.SysFont('comicsansms', 72)
        textSurface = textefont.render(texte, True, settings.BLACK)
        TextSurf,  TextRect = textSurface, textSurface.get_rect()
        TextRect.center = ((settings.DISPLAY_WIDTH/2), (settings.DISPLAY_HEIGHT/2))
        screen.fill(settings.BLUE)
        screen.blit(TextSurf, TextRect)
        pygame.display.flip()

    # LOCAL VARIABLES #
    # food position
    food_radius = 5
    food_speed = 2
    # Score
    score = 0
    highscore = 0
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

    my_fish_entity = entities.MyFish()
    big_fish_entity = entities.BigFish()
    pebble_all = pygame.sprite.Group()
    pebble_all.add(FoodPebble())


    while True:
        # === KEY EVENTS ===
        my_fish_entity.check_key_events()

        # ===  DISPLAY ===
        screen.fill(settings.BLUE)
        Display_Score(highscore, score, my_fish_entity.lives)
        my_fish_entity.draw(screen)
        big_fish_entity.draw(screen)
        pebble_all.update(screen)

        # === EVENTS ===
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
                # pygame.draw.circle(screen, settings.RED, (extra_food_special_x, extra_food_special_y), food_radius+1)
                screen.blit(Banana_img, (extra_food_special_x, extra_food_special_y))
                extra_food_special_y += 1

            if extra_food_special_x + 30 > my_fish_entity.pos.x and extra_food_special_x < my_fish_entity.pos.x + my_fish_entity.width and extra_food_special_y + 30 > my_fish_entity.pos.y and extra_food_special_y < my_fish_entity.pos.y + my_fish_entity.height:
                extra_food_special_y = settings.DISPLAY_HEIGHT
                draw = False
                # start_bonus_food = 1
                start_time = time.process_time()
                start_bonus_food = 1

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
            screen.blit(Life_img, (life_x, life_y))
            life_y += 1

        if life_x > my_fish_entity.pos.x and life_x < my_fish_entity.pos.x + my_fish_entity.width and life_y > my_fish_entity.pos.y and life_y < my_fish_entity.pos.y + my_fish_entity.height:
            life_y = settings.DISPLAY_HEIGHT
            my_fish_entity.lives += 1

        if life_y > settings.DISPLAY_HEIGHT:
            extra_life = 0
            once_life = 0

        # fish catches food
        for i in range(len(extra_food_x)):
            if extra_food_x[i] > my_fish_entity.pos.x and extra_food_x[i] < my_fish_entity.pos.x + my_fish_entity.width and extra_food_y[i] > my_fish_entity.pos.y and extra_food_y[i] < my_fish_entity.pos.y + my_fish_entity.height:
                extra_food_y[i] = settings.DISPLAY_HEIGHT
                score += 1
                my_fish_entity.grow()

        # if my_fish collides with a food pebble
        if pygame.sprite.spritecollide(my_fish_entity, pebble_all, True):
            pebble_all.add(FoodPebble())
            score += 1
            my_fish_entity.grow()

        if settings.DEBUG:
            # move big_fish
            big_fish_entity.wander()

            scale = 25
            # vel
            pygame.draw.line(screen, settings.GREEN, big_fish_entity.pos, (big_fish_entity.pos + big_fish_entity.vel * scale), 5)
            # desired
            pygame.draw.line(screen, settings.RED, big_fish_entity.pos, (big_fish_entity.pos + big_fish_entity.desired * scale), 5)
            # target
            center = big_fish_entity.pos + big_fish_entity.vel.normalize() * entities.WANDER_RING_DISTANCE
            pygame.draw.circle(screen, settings.WHITE, (int(center.x), int(center.y)), entities.WANDER_RING_RADIUS, 1)
            pygame.draw.line(screen, settings.CYAN, center, big_fish_entity.displacement, 5)

        # Collision Bigfish/myfish
        if my_fish_entity.rect.colliderect(big_fish_entity.rect):
            if my_fish_entity.can_take_revenge:
                my_fish_entity.eat(big_fish_entity)
            else:
                big_fish_entity.eat(my_fish_entity)

        # Highscore calculation
        if score > highscore:
            highscore = score

        if my_fish_entity.lives == 0:
            GameOver_Display('No more lives left :(')
            time.sleep(2)
            pygame.quit()
            quit()

        # frame counter
        if framecount > 59:
            framecount = 0
        else:
            framecount += 1

        pygame.display.update()
        clock.tick(settings.FPS)


game_loop()
pygame.quit()
quit()
