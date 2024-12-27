from random import random, choice
import pygame
from cfg import *
from powerup import PowerUp

class PowerUpHandler:
    def __init__(self):
        self.powerups = pygame.sprite.Group()
        self.powerup_counts = {"lives": 0, "speed": 0, "cooldown": 0, "bullets": 0}  # Хранит количество выпавших улучшений

    def spawn_powerup(self, position, current_level):
        # Получаем информацию о лимитах улучшений на текущем уровне
        level_powerups = LEVEL_POWERUPS[current_level]

        # Собираем список возможных улучшений
        possible_powerups = []
        if self.powerup_counts["lives"] < level_powerups["lives"]:
            possible_powerups.append("lives")
        if self.powerup_counts["speed"] < level_powerups["speed"]:
            possible_powerups.append("speed")
        if self.powerup_counts["cooldown"] < level_powerups["cooldown"]:
            possible_powerups.append("cooldown")
        if self.powerup_counts["bullets"] < level_powerups["bullets"]:
            possible_powerups.append("bullets")

        if possible_powerups:
            # Выбираем случайное улучшение
            chosen_powerup = choice(possible_powerups)
            # Спавним улучшение
            new_powerup = PowerUp(chosen_powerup, position)
            self.powerups.add(new_powerup)
            self.powerup_counts[chosen_powerup] += 1  # Увеличиваем счетчик для выбранного улучшения

    def check_collision(self, player):
        # Проверка столкновения улучшений с игроком.
        for powerup in pygame.sprite.spritecollide(player, self.powerups, dokill=True):
            match powerup.type:
                case "lives":
                    if player.lives < MAX_PLAYER_LIVES:
                        player.lives += 1
                case "speed":
                    if player.speed < MAX_PLAYER_SPEED:
                        player.speed += PLAYER_SPEED_INCREASE
                case "cooldown":
                    if player.shoot_cooldown > MAX_PLAYER_SHOOT_COOLDOWN:
                        player.shoot_cooldown -= PLAYER_SHOOT_COOLDOWN_DECREASE
                case "bullets":
                    if player.bullets_per_shot < MAX_PLAYER_BULLETS_PER_SHOT:
                        player.bullets_per_shot += PLAYER_BULLETS_PER_SHOT_INCREASE

    def update(self):
        # Обновление всех улучшений.
        self.powerups.update()