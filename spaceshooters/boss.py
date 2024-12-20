import pygame
from cfg import *
from bullet import Bullet


class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("PNG/boss.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

        # Стадия 1
        self.health_stage1 = BOSS_STAGE1_HEALTH
        self.speed_stage1 = BOSS_STAGE1_SPEED
        self.shoot_cooldown_stage1 = BOSS_STAGE1_SHOOT_COOLDOWN

        # Стадия 2
        self.health_stage2 = BOSS_STAGE2_HEALTH
        self.damage_stage2 = BOSS_STAGE2_DAMAGE
        self.speed_stage2 = BOSS_STAGE2_SPEED
        self.shoot_cooldown_stage2 = BOSS_STAGE2_SHOOT_COOLDOWN

        # Начальная стадия
        self.current_stage = 1
        self.health = self.health_stage1
        self.speed = self.speed_stage1
        self.shoot_cooldown = self.shoot_cooldown_stage1
        self.shoot_timer = self.shoot_cooldown
        self.direction = 1  # Начальное направление движения

        self.bullets = pygame.sprite.Group()

    def update(self):
        # Движение босса
        self.rect.x += self.speed * self.direction
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.direction *= -1
            self.rect.y += ENEMY_MOVE_DOWN_SPEED

        self.shoot_timer -= 1 / 60
        if self.shoot_timer <= 0:
            self.shoot()
            self.shoot_timer = self.shoot_cooldown

        self.bullets.update()

    def shoot(self):
        self.bullets.add(Bullet(self.rect.midbottom, BOSS_BULLET_SPEED, False, '1'))

    def start_stage2(self):
        """Переход босса на стадию 2"""
        self.current_stage = 2
        self.health = self.health_stage2
        self.speed = self.speed_stage2
        self.shoot_cooldown = self.shoot_cooldown_stage2

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.start_stage2() if self.current_stage == 1 else self.kill()