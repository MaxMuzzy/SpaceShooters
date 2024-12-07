import pygame

from random import choice
from cfg import *
from enemy import Enemy
from bullet import Bullet


class EnemyHandler():
    def __init__(self, current_level_enemies, enemy_bullets):
        if type(current_level_enemies) == pygame.sprite.Group and type(enemy_bullets) == pygame.sprite.Group:
            self.enemies = current_level_enemies
            self.enemy_bullets = enemy_bullets
            self.enemy_direction = ENEMY_1_MOVE_SPEED
            self.enemy_shoot_interval = ENEMY_SHOOT_TIME
            self.enemy_shoot_timer = self.enemy_shoot_interval
        else:
            raise ValueError

    def update(self):
        self.enemies.update(self.enemy_direction)
        self.enemy_bullets.update()
        self.enemy_position_checker()

        if self.enemy_shoot_timer is None:
            self.enemy_shoot_timer = self.enemy_shoot_interval
        self.enemy_shoot_timer -= 1 / 60
        if self.enemy_shoot_timer <= 0:
            self.enemy_shoot_timer = None
            self.enemy_shoot()

    def enemy_setup(self, currentLevel):
        for row_index, row in enumerate(currentLevel):
            for col_index, col in enumerate(row):
                x = ENEMY_X_OFFSET + col_index * ENEMY_X_DISTANCE
                y = ENEMY_Y_OFFSET + row_index * ENEMY_Y_DISTANCE
                if col == '1':
                    enemy_sprite = Enemy('1', x, y)
                elif col == '2':
                    enemy_sprite = Enemy('2', x, y)
                elif col == '3':
                    enemy_sprite = Enemy('3', x, y)
                else:
                    continue

                self.enemies.add(enemy_sprite)
                self.enemy_direction = self.get_enemy_move_speed()

    def enemy_position_checker(self):
        for enemy in self.enemies.sprites():
            if enemy.rect.right >= SCREEN_WIDTH:
                self.enemy_direction = -self.get_enemy_move_speed()
                self.enemy_move_down(ENEMY_MOVE_DOWN_SPEED)
            elif enemy.rect.left <= 0:
                self.enemy_direction = self.get_enemy_move_speed()
                self.enemy_move_down(ENEMY_MOVE_DOWN_SPEED)

    def enemy_move_down(self, distance):
        if self.enemies.sprites():
            for enemy in self.enemies.sprites():
                enemy.rect.y += distance

    def get_enemy_move_speed(self):
        c1 = 0
        c2 = 0
        c3 = 0
        for enemy in self.enemies.sprites():
            match enemy.enemy_index:
                case '1':
                    c1 += 1
                case '2':
                    c2 += 1
                case '3':
                    c3 += 1
        res = max(c1, c2, c3)
        if res == c1:
            return ENEMY_1_MOVE_SPEED
        elif res == c2:
            return ENEMY_2_MOVE_SPEED
        elif res == c3:
            return ENEMY_3_MOVE_SPEED

    def enemy_shoot(self):
        if self.enemies.sprites():
            random_enemy = choice(self.enemies.sprites())
            bullet_sprite = Bullet(random_enemy.rect.center, ENEMY_BULLET_SPEED, False, random_enemy.enemy_index)
            self.enemy_bullets.add(bullet_sprite)