import pygame
from bullet import Bullet
from cfg import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint, speed):
        super().__init__()
        self.image = pygame.image.load('PNG/new/newPlayer.png').convert_alpha()
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
        # if self.shoot_time is None:
        #     self.shoot_time = self.shoot_cooldown
        # self.shoot_time -= 1 / 60
        # if self.shoot_time <= 0:
        #     self.shoot_time = None
        #     self.ready = True

    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint

    def shoot(self):
        # Расстояние между пулями
        spacing = 20  # Вы можете настроить это значение в зависимости от нужной плотности

        # Генерируем пули в зависимости от количества
        for i in range(self.bullets_per_shot):
            # Расчёт смещения для пуль в зависимости от их количества
            offset = (i - (self.bullets_per_shot // 2)) * spacing  # Смещаем пули относительно центра
            self.bullets.add(Bullet((self.rect.centerx + offset, self.rect.top), -PLAYER_BULLET_SPEED, True, 0))

    def update(self):
        self.get_input()
        self.constraint()
        self.recharge()
        self.bullets.update()