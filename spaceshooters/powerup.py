import pygame
from cfg import *

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, powerup_type, pos):
        super().__init__()
        self.type = powerup_type  # Тип улучшения: "lives", "speed", "cooldown", "bullets"
        self.image = pygame.image.load(f'PNG/new/{self.type}_powerup.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.speed = 2  # Скорость падения

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()  # Уничтожить, если улучшение вышло за экран