import pygame, sys
from player import Player
import obstacle
from enemy import Enemy, UFO
from bullet import Bullet
from random import choice, randint
from cfg import *


class Game:
    def __init__(self):
        #player
        player_sprite = Player((screen_width / 2, screen_height - 25), screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        #health and score
        self.lives = 3
        self.live_surf = pygame.image.load('PNG/new/newPlayer.png').convert_alpha()
        self.live_x_start_pos = screen_width - (self.live_surf.get_size()[0] * 2 + 20)
        self.score = 0
        self.font = pygame.font.Font('font/PublicPixel.ttf', FONT_SIZE)

        #obstacles
        self.shape = obstacle.shape
        self.block_size = BLOCK_SIZE
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = OBSTACLE_AMOUNT
        self.obstacle_x_positions = [num * (screen_width/self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles( *self.obstacle_x_positions, x_start = screen_width / 12.625, y_start = OBSTACLE_Y_START)

        #enemies
        self.enemies = pygame.sprite.Group()
        self.enemy_setup(3, 8)
        self.enemy_direction = 1
        self.enemy_bullets = pygame.sprite.Group()

        #ufo
        self.ufo = pygame.sprite.GroupSingle()
        self.ufo_spawn_time = randint(UFO_MIN_TIME, UFO_MAX_TIME)

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

    def enemy_setup(self, rows, cols, x_distance = ENEMY_X_DISTANCE, y_distance= ENEMY_Y_DISTANCE, x_offset = ENEMY_X_OFFSET, y_offset = ENEMY_Y_OFFSET):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset
                enemy_sprite = Enemy('1', x,y)
                self.enemies.add(enemy_sprite)

    def enemy_position_checker(self):
        for enemy in self.enemies.sprites():
            if enemy.rect.right >= screen_width:
                self.enemy_direction = -ENEMY_MOVE_SPEED
                self.enemy_move_down(ENEMY_MOVE_DOWN_SPEED)
            elif enemy.rect.left <= 0:
                self.enemy_direction = ENEMY_MOVE_SPEED
                self.enemy_move_down(ENEMY_MOVE_DOWN_SPEED)

    def enemy_move_down(self, distance):
        if self.enemies.sprites():
            for enemy in self.enemies.sprites():
                enemy.rect.y += distance

    def enemy_shoot(self):
        if self.enemies.sprites():
            random_enemy = choice(self.enemies.sprites())
            bullet_sprite = Bullet(random_enemy.rect.center, ENEMY_BULLET_SPEED, False, random_enemy.enemy_index)
            self.enemy_bullets.add(bullet_sprite)

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
                enemies_hit = pygame.sprite.spritecollide(bullet, self.enemies, True)
                if enemies_hit:
                    for enemy in enemies_hit:
                        self.score += enemy.value
                    bullet.kill()
                #ufo collision
                if pygame.sprite.spritecollide(bullet, self.ufo, True):
                    self.score += UFO_VALUE
                    bullet.kill()

        if self.enemy_bullets:
            for bullet in self.enemy_bullets:
                # obstacle collision
                if pygame.sprite.spritecollide(bullet, self.blocks, True):
                    bullet.kill()
                if pygame.sprite.spritecollide(bullet, self.player, False):
                    bullet.kill()
                    self.lives -=1
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()

        if self.enemies:
            for enemy in self.enemies:
                pygame.sprite.spritecollide(enemy, self.blocks, True)
                if pygame.sprite.spritecollide(enemy, self.player, False):
                    pygame.quit()
                    sys.exit()

    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
            screen.blit(self.live_surf, (x, 8))

    def display_score(self):
        score_surf = self.font.render(f'SCORE: {self.score}', False, 'white')
        score_rect = score_surf.get_rect(topleft = (10,10))
        screen.blit(score_surf, score_rect)

    def victory_message(self):
        if not self.enemies.sprites():
            victory_surf = self.font.render('YOU WON!', False, 'white')
            victory_rect = victory_surf.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            screen.blit(victory_surf, victory_rect)

    def run(self):
        if self.enemies.sprites():
            self.player.update()
            self.enemies.update(self.enemy_direction)
            self.ufo.update()
            self.enemy_bullets.update()
            self.enemy_position_checker()

            self.ufo_timer()
            self.collision_checks()
        else:
            victory_surf = self.font.render('YOU WON!', False, 'white')
            victory_rect = victory_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            screen.blit(victory_surf, victory_rect)

        self.player.sprite.bullets.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.enemies.draw(screen)
        self.enemy_bullets.draw(screen)
        self.ufo.draw(screen)
        self.display_lives()
        self.display_score()

pygame.init()
screen_width = SCREEN_WIDTH
screen_height = SCREEN_HEIGHT
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Space Shooters')
clock = pygame.time.Clock()
game = Game()

ENEMYLASER = pygame.USEREVENT + 1
pygame.time.set_timer(ENEMYLASER, ENEMY_SHOOT_TIME)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == ENEMYLASER:
            game.enemy_shoot()
    screen.fill((30,30,30))
    game.run()
    pygame.display.flip()
    clock.tick(60)