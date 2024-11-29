import pygame
from cfg import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_index, x, y):
        super().__init__()
        file_path = 'PNG/new/' + enemy_index + '.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft = (x,y))
        self.enemy_index = enemy_index
        match self.enemy_index:
            case '1':
                self.value = ENEMY_1_VALUE
            case '2':
                self.value = ENEMY_2_VALUE
            case '3':
                self.value = ENEMY_3_VALUE

    def update(self, direction):
        self.rect.x += direction

class UFO(pygame.sprite.Sprite):
    def __init__(self, side):
        super().__init__()
        self.image = pygame.image.load("PNG/new/newUFO.png").convert_alpha()

        if side == "right":
            x = SCREEN_WIDTH + 50
            self.speed = -UFO_SPEED
        else:
            x = -50
            self.speed = UFO_SPEED

        self.rect = self.image.get_rect(topleft = (x, UFO_Y))
    def update(self):
        self.rect.x += self.speed