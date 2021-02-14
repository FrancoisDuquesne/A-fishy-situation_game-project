import pygame
import settings
from random import randint, uniform
from pygame.sprite import Sprite


vec = pygame.math.Vector2

MAX_SPEED = 3
MAX_FORCE = 0.9
WANDER_RING_DISTANCE = 200
WANDER_RING_RADIUS = 20
MAX_WIDTH = 200


class Fish(Sprite):
    def __init__(self):
        super().__init__()
        self.width = 40
        self.height = 20
        self.orientation = 'l'
        self.pos = vec(0, 0)
        self.image = ''
        self.lives = 1

    def get_img(self):
        if self.orientation == 'l':
            return self.image
        if self.orientation == 'r':
            return pygame.transform.flip(self.image, 1, 0)

    def eat(self, entity):
        entity.get_eaten()

    def draw(self, screen):
        screen.blit(self.get_img(), self.pos)


class MyFish(Fish):
    def __init__(self):
        super().__init__()
        self.pos = vec(settings.DISPLAY_WIDTH * 0.45, settings.DISPLAY_HEIGHT * 0.8)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.friction = 0.05
        self.max_speed = 10
        self.evolved = False
        self.evolution_width = 100
        self.lives = 3
        self.can_take_revenge = False
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        if settings.DEBUG:
            self.image = pygame.Surface([self.width, self.height])
            self.image.fill(settings.ORANGE)
        else:
            raw_img = pygame.image.load('resources/Fish_l.png')
            self.image = pygame.transform.scale(raw_img, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos + vec(self.width/2, self.height/2)

    def check_key_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Movement keys
            # self.acc = vec(0, 0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.acc.x += 3
                elif event.key == pygame.K_LEFT:
                    self.acc.x += -3
                elif event.key == pygame.K_UP:
                    self.acc.y += -3
                elif event.key == pygame.K_DOWN:
                    self.acc.y += 3
                # quit game
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                # elif event.key == pygame.K_d:
                #     print("TOGGLE DEBUG")
                #     settings.DEBUG = not settings.DEBUG

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.acc.x = 0
                elif event.key == pygame.K_LEFT:
                    self.acc.x = 0
                elif event.key == pygame.K_UP:
                    self.acc.y = 0
                elif event.key == pygame.K_DOWN:
                    self.acc.y = 0
    # pressed_keys = pygame.key.get_pressed()
    # # print("pressed_keys", pressed_keys)
    # if pressed_keys[K_RIGHT]:
    #     self.acc.x += 3
    # if pressed_keys[K_LEFT]:
    #     self.acc.x += -3
    # if pressed_keys[K_UP]:
    #     self.acc.y += -3
    # if pressed_keys[K_DOWN]:
    #     self.acc.y += 3

        # update speed
        self.vel += self.acc - self.vel*self.friction
        if self.vel.length() > self.max_speed:
            self.vel.scale_to_length(MAX_SPEED)
        self.pos += self.vel
        self.rect.center = self.pos + vec(self.width/2, self.height/2)

        # set orientation
        self.orientation = 'r' if self.vel.x > 0 else 'l'

        # boundaries for fish movement on on display
        max_x = settings.DISPLAY_WIDTH - self.width
        max_y = settings.DISPLAY_HEIGHT - self.height
        if self.pos.x > max_x:
            self.pos.x = max_x
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.y > max_y:
            self.pos.y = max_y
        if self.pos.y < 0:
            self.pos.y = 0

    def grow(self):
        if not self.width > MAX_WIDTH:
            self.width = self.width + round(self.width * 0.3)
            self.height = self.height + round(self.height * 0.3)
        if self.width >= self.evolution_width and not self.evolved:
            self.evolve()
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(settings.ORANGE)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos + vec(self.width/2, self.height/2)

    def evolve(self):
        if settings.DEBUG:
            self.image.fill(settings.RED)
        else:
            raw_img = pygame.image.load('resources/angry_fish.png')
            self.image = pygame.transform.scale(raw_img, (self.width, self.height))
        self.evolved = True
        self.can_take_revenge = True

    def respawn(self):
        self.pos = vec(0, 0)

    def get_eaten(self):
        self.lives -= 1
        self.respawn()


class BigFish(Fish):
    def __init__(self):
        super().__init__()
        self.width = 250
        self.height = 120
        self.evolved = False
        self.evolution_width = 100
        if settings.DEBUG:
            self.image = pygame.Surface([self.width, self.height])
            self.image.fill(settings.WHITE)
        else:
            raw_img = pygame.image.load('resources/Bigfish.png')
            self.image = pygame.transform.scale(raw_img, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.pos = vec(settings.DISPLAY_WIDTH * 0.40, settings.DISPLAY_HEIGHT * 0.45)
        self.rect.center = self.pos + vec(self.width/2, self.height/2)
        self.vel = vec(MAX_SPEED, 0).rotate(uniform(0, 360))
        self.acc = vec(0, 0)
        self.target = vec(randint(0, settings.DISPLAY_WIDTH), randint(0, settings.DISPLAY_HEIGHT))
        self.last_target = 0
        self.target = vec(randint(0, self.width), randint(0, self.height))

    def seek(self, target):
        self.desired = (target - self.pos).normalize() * MAX_SPEED
        steer = (self.desired - self.vel)
        if steer.length() > MAX_FORCE:
            steer.scale_to_length(MAX_FORCE)
        return steer

    def wander(self):
        future = self.pos + self.vel.normalize() * WANDER_RING_DISTANCE
        target = future + vec(WANDER_RING_RADIUS, 0).rotate(uniform(0, 360))
        self.displacement = target

        self.acc = self.seek(target)
        # equations of motion
        self.vel += self.acc
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)
        self.pos += self.vel
        self.rect.center = self.pos + vec(self.width/2, self.height/2)
        self.orientation = 'r' if self.vel.x > 0 else 'l'
        if self.pos.x > settings.DISPLAY_WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = settings.DISPLAY_WIDTH
        if self.pos.y > settings.DISPLAY_HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = settings.DISPLAY_HEIGHT

    def get_eaten(self):
        self.pos = vec(0, 0)
