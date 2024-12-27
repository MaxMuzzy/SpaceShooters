import pygame, sys
from player import Player
import obstacle
from enemy import UFO
from random import choice, randint, random
from cfg import *
from enemyhandler import EnemyHandler
from poweruphandler import PowerUpHandler
from bosshandler import BossHandler

class Game:
    def __init__(self):
        #player
        player_sprite = Player((screen_width / 2, screen_height - 25), screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        #health and score
        self.live_surf = pygame.image.load('PNG/newPlayer.png').convert_alpha()
        self.live_x_start_pos = screen_width - (self.live_surf.get_size()[0] * 3 + 20)
        self.score = 0
        self.font = pygame.font.Font('font/PublicPixel.ttf', FONT_SIZE)

        #obstacles
        self.shape = obstacle.shape
        self.block_size = BLOCK_SIZE
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = OBSTACLE_AMOUNT
        self.obstacle_x_positions = [num * (screen_width/self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_positions, x_start = screen_width / 12.625, y_start = OBSTACLE_Y_START)

        #enemies
        self.enemy_handler = EnemyHandler()
        self.enemy_handler.enemy_setup(LEVELS[0])

        #ufo
        self.ufo = pygame.sprite.GroupSingle()
        self.ufo_spawn_time = randint(UFO_MIN_TIME, UFO_MAX_TIME)

        #levels
        self.time_til_next_level = TIME_TIL_NEXT_LEVEL
        self.starting_level = 0
        self.current_level = self.starting_level
        self.game_over = False

        #powerups
        self.powerup_handler = PowerUpHandler()

        #boss
        self.boss_handler = BossHandler()

    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = obstacle.Block(self.block_size, (241, 79, 80), x, y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self, *offset, x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

    def ufo_timer(self):
        self.ufo_spawn_time -= 1
        if self.ufo_spawn_time <= 0:
            self.ufo.add(UFO(choice(['right', 'left'])))
            self.ufo_spawn_time = randint(UFO_MIN_TIME, UFO_MAX_TIME)

    def collision_checks(self):
        if self.player.sprite.bullets:
            for bullet in self.player.sprite.bullets:
                #obstacle collision
                if pygame.sprite.spritecollide(bullet, self.blocks, True):
                    bullet.kill()
                #enemy collision
                enemies_hit = pygame.sprite.spritecollide(bullet, self.enemy_handler.enemies, False)
                if enemies_hit:
                    for enemy in enemies_hit:
                        enemy.health -= 1
                        if enemy.health <= 0 and not enemy.is_hit:
                            enemy.is_hit = True
                            self.score += enemy.value
                            if random() <= POWERUP_DROP_CHANCE:
                                self.powerup_handler.spawn_powerup(enemy.rect.center, self.current_level)
                    bullet.kill()
                #ufo collision
                if pygame.sprite.spritecollide(bullet, self.ufo, True):
                    self.score += UFO_VALUE
                    bullet.kill()
                #boss collision
                if self.boss_handler.boss.sprite:
                    if pygame.sprite.spritecollide(bullet, self.boss_handler.boss, False):
                        bullet.kill()
                        self.boss_handler.boss.sprite.take_damage(1)

        if self.enemy_handler.enemy_bullets:
            for bullet in self.enemy_handler.enemy_bullets:
                # obstacle collision
                if pygame.sprite.spritecollide(bullet, self.blocks, True):
                    bullet.kill()
                # player collision
                if pygame.sprite.spritecollide(bullet, self.player, False):
                    bullet.kill()
                    if bullet.owner_index == '3':
                        self.player.sprite.lives -= 2
                    else:
                        self.player.sprite.lives -= 1
                    if self.player.sprite.lives <= 0:
                        pygame.quit()
                        sys.exit()

        if self.enemy_handler.enemies:
            for enemy in self.enemy_handler.enemies:
                pygame.sprite.spritecollide(enemy, self.blocks, True)
                if pygame.sprite.spritecollide(enemy, self.player, False):
                    pygame.quit()
                    sys.exit()

        for enemy in self.enemy_handler.enemies.sprites():
            enemy.reset_hit()

        #boss
        if self.boss_handler.boss.sprite: #and not self.boss_handler.defeated:
            if self.boss_handler.boss.sprite.bullets:
                for bullet in self.boss_handler.boss.sprite.bullets:
                    # obstacle collision
                    if pygame.sprite.spritecollide(bullet, self.blocks, True):
                        bullet.kill()
                    # player collision
                    if pygame.sprite.spritecollide(bullet, self.player, False):
                        bullet.kill()
                        damage = BOSS_STAGE2_DAMAGE if self.boss_handler.boss.sprite.current_stage == 2 else 1
                        self.player.sprite.lives -= damage
                        if self.player.sprite.lives <= 0:
                            pygame.quit()
                            sys.exit()


    def display_lives(self):
        for live in range(self.player.sprite.lives):
            x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
            screen.blit(self.live_surf, (x, 8))

    def display_score(self):
        score_surf = self.font.render(f'SCORE: {self.score}', False, 'white')
        score_rect = score_surf.get_rect(topleft=(10, 10))
        screen.blit(score_surf, score_rect)

    def display_text(self, message, offset_x, offset_y):
        victory_surf = self.font.render(f'{message}', False, 'white')
        victory_rect = victory_surf.get_rect(center=(SCREEN_WIDTH / 2 + offset_x, SCREEN_HEIGHT / 2 + offset_y))
        screen.blit(victory_surf, victory_rect)

    def run(self):
        if self.enemy_handler.enemies.sprites():
            self.level_clear_timer = None
        elif not self.game_over:
            if self.current_level + 1 < len(LEVELS):
                if self.level_clear_timer is None:
                    self.level_clear_timer = self.time_til_next_level

                self.level_clear_timer -= 1 / 60
                time_remaining = max(0, int(self.level_clear_timer))
                self.display_text(f"NEXT STAGE IN: {time_remaining + 1}", 0, 0)

                if self.level_clear_timer <= 0:
                    self.level_clear_timer = None
                    self.current_level += 1
                    self.enemy_handler.enemy_setup(LEVELS[self.current_level])
                    self.powerup_handler.__init__()
                    self.time_til_next_level = TIME_TIL_NEXT_LEVEL
            else:
                if not self.boss_handler.boss and not self.boss_handler.defeated:
                    if self.level_clear_timer is None:
                        self.level_clear_timer = self.time_til_next_level

                    self.level_clear_timer -= 1 / 60
                    time_remaining = max(0, int(self.level_clear_timer))
                    self.display_text(f"BOSS STAGE IN: {time_remaining + 1}", 0, 0)

                    if self.level_clear_timer <= 0:
                        self.boss_handler.start_boss_battle()
                elif self.boss_handler.defeated:
                    self.score += BOSS_VALUE
                    self.game_over = True

        if self.game_over:
            self.display_text("YOU WIN!", 0, 0)
            self.display_text("PRESS R TO RESTART", 0, 35)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self.__init__()
        else:
            self.player.update()
            self.ufo.update()
            self.enemy_handler.update()
            self.ufo_timer()
            self.collision_checks()
            self.powerup_handler.update()
            self.powerup_handler.check_collision(self.player.sprite)
            self.boss_handler.update()


        self.player.sprite.bullets.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.enemy_handler.enemies.draw(screen)
        self.enemy_handler.enemy_bullets.draw(screen)
        self.ufo.draw(screen)
        self.display_lives()
        self.display_score()
        self.powerup_handler.powerups.draw(screen)
        if self.boss_handler.boss.sprite:
            self.boss_handler.boss.draw(screen)
            self.boss_handler.boss.sprite.bullets.draw(screen)
            self.boss_handler.draw_health_bar(screen)

pygame.init()
screen_width = SCREEN_WIDTH
screen_height = SCREEN_HEIGHT
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Shooters')
clock = pygame.time.Clock()
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((30, 30, 30))
    game.run()
    pygame.display.flip()
    clock.tick(60)