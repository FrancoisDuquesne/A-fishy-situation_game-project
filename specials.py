import pygame
import settings
from random import randint, uniform


vec = pygame.math.Vector2


class Special():
    def __init__(self):
        self.width = 60


class Banana(Special):
    def __init__(self):
        self.width = 60

    def give_bonus(self, entity):
        entity.lives += 1
