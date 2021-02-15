import pygame
import settings
import random
from pygame.sprite import Sprite


vec = pygame.math.Vector2
MAX_FOOD_SPEED = 3


class Special(Sprite):
    def __init__(self):
        super().__init__()
        self.width = 60
        self.radius = 60
        self.pos = vec(random.randrange(1, settings.DISPLAY_WIDTH-self.width), -random.randrange(settings.DISPLAY_HEIGHT, settings.DISPLAY_HEIGHT*2))
        self.speed = 2

    def draw(self, screen):
        screen.blit(self.image, self.pos)

    def fall(self):
        if self.pos.y > settings.DISPLAY_HEIGHT:
            self.pos = vec(random.randrange(0, settings.DISPLAY_WIDTH), 0 - self.radius)
        else:
            self.pos.y += self.speed
            self.rect.center = self.pos + vec(self.radius/2, self.radius/2)

    def update(self, screen):
        self.fall()
        self.draw(screen)


class Banana(Special):
    def __init__(self):
        super().__init__()
        self.width = 60
        self.height = 60
        self.image = pygame.transform.scale(pygame.image.load('resources/banana.png'), (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos + vec(self.width/2, self.height/2)

    def give_bonus(self, entity):
        entity.lives += 1


class Heart(Special):
    def __init__(self):
        super().__init__()
        self.width = 60
        self.height = 60
        self.image = pygame.transform.scale(pygame.image.load('resources/life.png'), (20, 20))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos + vec(self.width/2, self.height/2)


class FoodPebble(Sprite):
    def __init__(self):
        super().__init__()
        self.radius = 5
        self.speed = random.uniform(1, MAX_FOOD_SPEED)
        self.color = settings.ORANGE
        self.pos = vec(random.randrange(1, settings.DISPLAY_WIDTH - self.radius), -random.randrange(0, 100))
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
