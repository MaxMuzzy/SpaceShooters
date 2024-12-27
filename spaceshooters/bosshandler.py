import pygame
from cfg import *
from boss import Boss

class BossHandler():
    def __init__(self):
        self.boss = pygame.sprite.GroupSingle()
        self.defeated = False
        self.spawned = False

    def update(self):
            if self.boss.sprite:
                self.boss.update()
            elif self.spawned:
                    self.defeated = True

    def start_boss_battle(self):
        if not self.boss.sprite:
            self.boss_sprite = Boss(SCREEN_WIDTH // 2, 150)
            self.boss = pygame.sprite.GroupSingle(self.boss_sprite)
            self.spawned = True

    def draw_health_bar(self, screen):
        if self.boss.sprite:
            pygame.draw.rect(screen, 'red', (SCREEN_WIDTH // 4, 75, SCREEN_WIDTH // 2, 10))
            health_ratio = self.boss.sprite.health / (
                BOSS_STAGE1_HEALTH if self.boss.sprite.current_stage == 1 else BOSS_STAGE2_HEALTH)
            pygame.draw.rect(screen, 'green', (SCREEN_WIDTH // 4, 75, (SCREEN_WIDTH // 2) * health_ratio, 10))
