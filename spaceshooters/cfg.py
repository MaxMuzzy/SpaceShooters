FONT_SIZE = 20
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

PLAYER_SHOOT_COOLDOWN = 600 # Миллисекунды
PLAYER_BULLET_SPEED = 8

BLOCK_SIZE = 7
OBSTACLE_AMOUNT = 4
OBSTACLE_Y_START = 650

UFO_MIN_TIME = 600
UFO_MAX_TIME = 1000
UFO_VALUE = 500
UFO_SPEED = 3
UFO_Y = 60

ENEMY_X_DISTANCE = 65
ENEMY_Y_DISTANCE = 65
ENEMY_X_OFFSET = 75
ENEMY_Y_OFFSET = 100
ENEMY_1_MOVE_SPEED = 1
ENEMY_2_MOVE_SPEED = 2
ENEMY_3_MOVE_SPEED = 1
ENEMY_MOVE_DOWN_SPEED = 3
ENEMY_1_VALUE = 100
ENEMY_2_VALUE = 200
ENEMY_3_VALUE = 300
ENEMY_SHOOT_TIME = 0.8 # Секунды
ENEMY_BULLET_SPEED = 6


TIME_TIL_NEXT_LEVEL = 3 # Секунды
LEVELS = [
    [
        '1111111111',
        '1111111111',
        '1111111111',
    ],
    [
        '2222222222',
        '2222222222',
        '2222222222',
        '1111111111',
    ],
    [
        '3333333333',
        '3333333333',
        '3333333333',
        '2222222222',
        '1111111111',
    ],
]

# Максимальные значения улучшений
MAX_PLAYER_LIVES = 3
MAX_PLAYER_SPEED = 10
MAX_PLAYER_SHOOT_COOLDOWN = 200  # Миллисекунды
MAX_PLAYER_BULLETS_PER_SHOT = 5

# Приросты улучшений
PLAYER_SPEED_INCREASE = 1
PLAYER_SHOOT_COOLDOWN_DECREASE = 50  # Миллисекунды
PLAYER_BULLETS_PER_SHOT_INCREASE = 1

# Шанс выпадения улучшения (0.0 - 1.0)
POWERUP_DROP_CHANCE = 0.15

# Улучшения по уровням
LEVEL_POWERUPS = [
    {"lives": 0, "speed": 0, "cooldown": 0, "bullets": 0},  # Уровень 1
    {"lives": 4, "speed": 2, "cooldown": 0, "bullets": 0},  # Уровень 2
    {"lives": 2, "speed": 1, "cooldown": 3, "bullets": 3},  # Уровень 3
]

# Параметры босса
BOSS_STAGE1_HEALTH = 50
BOSS_STAGE1_SPEED = 2
BOSS_STAGE1_DAMAGE = 1
BOSS_STAGE1_SHOOT_COOLDOWN = 0.6  # В секундах

BOSS_STAGE2_HEALTH = 75
BOSS_STAGE2_SPEED = 1
BOSS_STAGE2_DAMAGE = 2
BOSS_STAGE2_SHOOT_COOLDOWN = 0.8  # В секундах

BOSS_BULLET_SPEED = 5
BOSS_VALUE = 10000