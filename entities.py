import pygame
import settings
from random import randint, uniform


vec = pygame.math.Vector2

MAX_SPEED = 3
MAX_FORCE = 0.9
WANDER_RING_DISTANCE = 200
WANDER_RING_RADIUS = 20


class Fish():
    def __init__(self):
        self.width = 60
        self.height = 35
        self.orientation = 'l'
        self.pos = vec(0, 0)
        self.display_img = ''

    def move(self, dx, dy):
        self.pos += vec(dx, dy)
        # define boundaries for fish movement on on display
        max_x = settings.DISPLAY_WIDTH - self.width
        max_y = settings.DISPLAY_HEIGHT - self.height

        if self.pos[0] > max_x:
            self.pos[0] = max_x
        if self.pos[0] < 0:
            self.pos[0] = 0
        if self.pos[1] > max_y:
            self.pos[1] = max_y
        if self.pos[1] < 0:
            self.pos[1] = 0

    def get_img(self):
        if self.orientation == 'l':
            return self.display_img
        if self.orientation == 'r':
            return pygame.transform.flip(self.display_img, 1, 0)


class MyFish(Fish):
    def __init__(self):
        super(MyFish, self).__init__()
        self.pos = vec(settings.DISPLAY_WIDTH * 0.45, settings.DISPLAY_HEIGHT * 0.8)
        self.evolved = False
        self.evolution_width = 100

        raw_img = pygame.image.load('resources/Fish_l.png')
        self.display_img = pygame.transform.scale(raw_img, (self.width, self.height))

    def grow(self):
        self.width += 10
        self.height += 10
        if self.width >= self.evolution_width and not self.evolved:
            self.evolve()

    def evolve(self):
        print("EVOLVING")
        raw_img = pygame.image.load('resources/angry_fish.png')
        self.display_img = pygame.transform.scale(raw_img, (self.width, self.height))
        self.evolved = True


class BigFish(Fish):
    def __init__(self):
        super(BigFish, self).__init__()
        self.width = 250
        self.height = 120
        self.evolved = False
        self.evolution_width = 100
        self.pos = vec(settings.DISPLAY_WIDTH * 0.40, settings.DISPLAY_HEIGHT * 0.45)
        self.center = self.pos
        self.vel = vec(MAX_SPEED, 0).rotate(uniform(0, 360))
        self.acc = vec(0, 0)
        self.target = vec(randint(0, settings.DISPLAY_WIDTH), randint(0, settings.DISPLAY_HEIGHT))

        self.last_target = 0
        self.target = vec(randint(0, self.width), randint(0, self.height))

        raw_img = pygame.image.load('resources/Bigfish.png')
        self.display_img = pygame.transform.scale(raw_img, (self.width, self.height))

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
        if self.pos.x > settings.DISPLAY_WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = settings.DISPLAY_WIDTH
        if self.pos.y > settings.DISPLAY_HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = settings.DISPLAY_HEIGHT
