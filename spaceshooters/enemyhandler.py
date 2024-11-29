import pygame
from cfg import *
from enemy import Enemy

class EnemyHandler():
    def __init__(self, current_level_enemies, enemy_bullets):
        if type(current_level_enemies) == pygame.sprite.Group and type(enemy_bullets) == pygame.sprite.Group:
            self.enemies = current_level_enemies
            self.enemyBullets = enemy_bullets
            self.enemy_direction = 1
            self.enemy_setup()
        else:
            raise ValueError

    def update(self):
        self.enemies.update(self.enemy_direction)
        self.enemyBullets.update()
        self.enemy_position_checker()

    def enemy_setup(self, x_distance = ENEMY_X_DISTANCE, y_distance= ENEMY_Y_DISTANCE, x_offset = ENEMY_X_OFFSET, y_offset = ENEMY_Y_OFFSET):
        for row_index, row in enumerate(LEVEL_1):
            for col_index, col in enumerate(row):
                x = x_offset + col_index * x_distance
                y = y_offset + row_index * y_distance
                if col == '1':
                    enemy_sprite = Enemy('1', x, y)
                if col == '2':
                    enemy_sprite = Enemy('2', x, y)
                if col == '3':
                    enemy_sprite = Enemy('3', x, y)

                self.enemies.add(enemy_sprite)

    def enemy_position_checker(self):
        for enemy in self.enemies.sprites():
            if enemy.rect.right >= SCREEN_WIDTH:
                self.enemy_direction = -ENEMY_1_MOVE_SPEED
                self.enemy_move_down(ENEMY_MOVE_DOWN_SPEED)
            elif enemy.rect.left <= 0:
                self.enemy_direction = ENEMY_1_MOVE_SPEED
                self.enemy_move_down(ENEMY_MOVE_DOWN_SPEED)

    def enemy_move_down(self, distance):
        if self.enemies.sprites():
            for enemy in self.enemies.sprites():
                enemy.rect.y += distance
