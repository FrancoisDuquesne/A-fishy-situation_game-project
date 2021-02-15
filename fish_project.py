"""
Created on Fri May 25 17:12:20 2018
@author: Francois, Jillian
"""

import pygame
import time
import settings
import fish
import specials
import user_interface as ui


def game_loop():
    screen = pygame.display.set_mode((settings.DISPLAY_WIDTH, settings.DISPLAY_HEIGHT))

    # Entities
    my_fish_entity = fish.MyFish()
    big_fish_entity = fish.BigFish()

    Pebbles = pygame.sprite.Group()
    Pebbles.add(specials.FoodPebble())

    Specials = pygame.sprite.Group()
    Specials.add(specials.Banana())
    Specials.add(specials.Heart())

    while True:

        # === KEY EVENTS ===
        my_fish_entity.check_key_events()

        # === DISPLAY ===
        screen.fill(settings.BLUE)
        ui.Display_Score(screen, ui.HIGHSCORE, ui.SCORE, my_fish_entity.lives)
        my_fish_entity.draw(screen)
        big_fish_entity.draw(screen)
        Pebbles.update(screen)
        Specials.update(screen)

        # move big_fish
        big_fish_entity.wander()
        if settings.DEBUG:
            scale = 25
            # vel
            pygame.draw.line(screen, settings.GREEN, big_fish_entity.pos, (big_fish_entity.pos + big_fish_entity.vel * scale), 5)
            # desired
            pygame.draw.line(screen, settings.RED, big_fish_entity.pos, (big_fish_entity.pos + big_fish_entity.desired * scale), 5)
            # target
            center = big_fish_entity.pos + big_fish_entity.vel.normalize() * fish.WANDER_RING_DISTANCE
            pygame.draw.circle(screen, settings.WHITE, (int(center.x), int(center.y)), fish.WANDER_RING_RADIUS, 1)
            pygame.draw.line(screen, settings.CYAN, center, big_fish_entity.displacement, 5)

        # === EVENTS ===
        # Collision Bigfish/myfish
        if my_fish_entity.rect.colliderect(big_fish_entity.rect):
            if my_fish_entity.can_take_revenge:
                my_fish_entity.eat(big_fish_entity)
            else:
                big_fish_entity.eat(my_fish_entity)

        # if my_fish collides with a food pebble
        if pygame.sprite.spritecollide(my_fish_entity, Pebbles, True):
            ui.SCORE += 1
            my_fish_entity.grow()

        # if my_fish collides with a special
        obj = pygame.sprite.spritecollide(my_fish_entity, Specials, True)
        if obj:
            if isinstance(obj[0], specials.Banana):
                Specials.add(specials.Banana())
                for i in range(10):
                    Pebbles.add(specials.FoodPebble())
            elif isinstance(obj[0], specials.Heart):
                Specials.add(specials.Heart())
                my_fish_entity.lives += 1

        # Drop food
        if len(Pebbles) == 0:
            Pebbles.add(specials.FoodPebble())

        # Highscore calculation
        if ui.SCORE > ui.HIGHSCORE:
            ui.HIGHSCORE = ui.SCORE

        if my_fish_entity.lives == 0:
            ui.GameOver_Display(screen, 'No more lives left :(')
            time.sleep(2)
            pygame.quit()
            quit()

        pygame.display.update()
        clock.tick(settings.FPS)



if __name__ == '__main__':
    pygame.display.set_caption('A fishy situation')
    clock = pygame.time.Clock()

    pygame.init()
    game_loop()
    pygame.quit()
    quit()
