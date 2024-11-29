import pygame
from cfg import SCREEN_HEIGHT

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, speed, is_player = True, enemy_index = 0):
        super().__init__()
        if is_player:
            self.image = pygame.image.load("PNG/new/newPlayerBullet.png").convert_alpha()
        else:
            if enemy_index != 0:
                self.image = pygame.image.load("PNG/new/newEnemy" + enemy_index + "Bullet.png").convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.height_y_constraint = SCREEN_HEIGHT

    def update(self):
        self.rect.y += self.speed
        self.destroy()

    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
            self.kill()

