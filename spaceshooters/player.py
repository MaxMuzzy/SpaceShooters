import pygame
from bullet import Bullet
from cfg import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint, speed):
        super().__init__()
        self.image = pygame.image.load('PNG/newPlayer.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = speed
        self.lives = MAX_PLAYER_LIVES
        self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN
        self.bullets_per_shot = 1  # Количество пуль за выстрел

        self.ready = True
        self.shoot_time = 0
        self.max_x_constraint = constraint
        self.bullets = pygame.sprite.Group()

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_SPACE] and self.ready:
            self.shoot()
            self.shoot_time = pygame.time.get_ticks()
            self.ready = False

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.shoot_cooldown:
                self.ready = True

    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint

    def shoot(self):
        bullets_count = self.bullets_per_shot
        # Расстояние между пулями
        spacing = 20

        if bullets_count % 2 == 1:
            self.bullets.add(Bullet(self.rect.center, -PLAYER_BULLET_SPEED, True, 0))
            for i in range(1, bullets_count // 2 + 1):
                offset = spacing * i
                self.bullets.add(Bullet((self.rect.centerx - offset, self.rect.centery), -PLAYER_BULLET_SPEED, True, 0))
                self.bullets.add(Bullet((self.rect.centerx + offset, self.rect.centery), -PLAYER_BULLET_SPEED, True, 0))
        else:
            for i in range(1, bullets_count // 2 + 1):
                offset = spacing * (i - 0.5)
                self.bullets.add(Bullet((self.rect.centerx - offset, self.rect.centery), -PLAYER_BULLET_SPEED, True, 0))
                self.bullets.add(Bullet((self.rect.centerx + offset, self.rect.centery), -PLAYER_BULLET_SPEED, True, 0))

    def update(self):
        self.get_input()
        self.constraint()
        self.recharge()
        self.bullets.update()