import pygame
import sys
import os

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
PROPASST_LIMIT = SCREEN_HEIGHT + 50  # Нижний предел для пропасти

# Цвета
WHITE = (255, 255, 255)
LIGHT_BLUE = (135, 206, 235)

# Путь к ресурсам
ASSETS_DIR = "assets"

# Создание окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Платформер с улучшенной графикой")
clock = pygame.time.Clock()

# Загрузка изображений
def load_image(filename, scale=None):
    path = os.path.join(ASSETS_DIR, filename)
    image = pygame.image.load(path).convert_alpha()
    if scale:
        image = pygame.transform.scale(image, scale)
    return image

PLAYER_IMG = load_image("player.png", (50, 50))
PLATFORM_IMG = load_image("platform.png", (200, 20))
COIN_IMG = load_image("coin.png", (20, 20))
FINISH_IMG = load_image("finish.png", (50, 50))

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = PLAYER_IMG
        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT - 70)  # Начальная позиция
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = 5
        self.jump_strength = -20  # Увеличили высоту прыжка
        self.gravity = 0.8
        self.health = 100
        self.score = 0

    def update(self, keys, platforms):
        # Горизонтальное движение
        self.velocity.x = 0
        if keys[pygame.K_LEFT]:
            self.velocity.x = -self.speed
        if keys[pygame.K_RIGHT]:
            self.velocity.x = self.speed

        # Прыжок
        if keys[pygame.K_SPACE] and self.is_on_ground(platforms):
            self.velocity.y = self.jump_strength

        # Гравитация
        self.velocity.y += self.gravity

        # Движение
        self.rect.x += self.velocity.x
        self.handle_horizontal_collisions(platforms)

        self.rect.y += self.velocity.y
        self.handle_vertical_collisions(platforms)

        # Проверяем, не упал ли игрок за пределы карты
        if self.rect.top > PROPASST_LIMIT:
            restart_game()

    def is_on_ground(self, platforms):
        self.rect.y += 1
        collisions = pygame.sprite.spritecollide(self, platforms, False)
        self.rect.y -= 1
        return len(collisions) > 0

    def handle_horizontal_collisions(self, platforms):
        collisions = pygame.sprite.spritecollide(self, platforms, False)
        for platform in collisions:
            if self.velocity.x > 0:  # Движение вправо
                self.rect.right = platform.rect.left
            elif self.velocity.x < 0:  # Движение влево
                self.rect.left = platform.rect.right

    def handle_vertical_collisions(self, platforms):
        collisions = pygame.sprite.spritecollide(self, platforms, False)
        for platform in collisions:
            if self.velocity.y > 0:  # Падение вниз
                self.rect.bottom = platform.rect.top
                self.velocity.y = 0
            elif self.velocity.y < 0:  # Прыжок вверх
                self.rect.top = platform.rect.bottom
                self.velocity.y = 0


# Класс платформы
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)  # Прозрачный фон
        tile_width = PLATFORM_IMG.get_width()
        tile_height = PLATFORM_IMG.get_height()

        # Заполняем платформу повторяющимися тайлами
        for i in range(0, width, tile_width):
            for j in range(0, height, tile_height):
                self.image.blit(PLATFORM_IMG, (i, j))

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


# Класс монеты
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = COIN_IMG
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.angle = 0  # Угол для вращения

    def update(self):
        # Вращение монеты
        self.angle += 5
        if self.angle >= 360:
            self.angle = 0
        self.image = pygame.transform.rotate(COIN_IMG, self.angle)


# Класс финиша
class Finish(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.transform.scale(FINISH_IMG, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


# Класс камеры
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + SCREEN_WIDTH // 2
        y = -target.rect.centery + SCREEN_HEIGHT // 2
        x = min(0, x)
        x = max(-(self.width - SCREEN_WIDTH), x)
        y = min(0, y)
        y = max(-(self.height - SCREEN_HEIGHT), y)
        self.camera = pygame.Rect(x, y, self.width, self.height)


# Список уровней
levels = [
    {  # Уровень 1: Базовый
        "platforms": [
            (0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20),
            (200, 500, 200, 20),
            (400, 400, 200, 20),
            (600, 300, 200, 20),
        ],
        "coins": [
            (250, 470),
            (450, 370),
            (650, 270),
        ],
        "finish": (700, 250, 50, 50)
    },
    {  # Уровень 2: Пропасти и длинные прыжки
        "platforms": [
            (0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20),
            (300, 500, 200, 20),
            (700, 400, 200, 20),
            (1100, 300, 200, 20),
            (1500, 200, 300, 20),  # Длинная платформа
        ],
        "coins": [
            (350, 470),
            (750, 370),
            (1150, 270),
        ],
        "finish": (1600, 150, 50, 50)
    },
    {  # Уровень 3: Лабиринт платформ
        "platforms": [
            (0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20),
            (200, 550, 150, 20),
            (400, 500, 150, 20),
            (600, 450, 150, 20),
            (800, 400, 200, 20),
            (1200, 350, 200, 20),
            (1600, 300, 200, 20),
        ],
        "coins": [
            (250, 520),
            (450, 470),
            (650, 420),
            (850, 370),
            (1250, 320),
        ],
        "finish": (1700, 250, 50, 50)
    }
]

# Текущий уровень
current_level = 0

# Функция загрузки уровня
def load_level(level_index):
    global player, all_sprites, platforms, coins, finish
    level = levels[level_index]
    player = Player()
    all_sprites = pygame.sprite.Group(player)

    platforms = pygame.sprite.Group()
    for data in level["platforms"]:
        platform = Platform(*data)
        platforms.add(platform)
        all_sprites.add(platform)

    coins = pygame.sprite.Group()
    for data in level["coins"]:
        coin = Coin(*data)
        coins.add(coin)
        all_sprites.add(coin)

    finish_data = level["finish"]
    finish = Finish(*finish_data)
    all_sprites.add(finish)

# Инициализация уровня
load_level(current_level)

# Создание камеры
level_width = 1800  # Уровень 3 длиннее
level_height = 800  # Высота уровня остаётся неизменной
camera = Camera(level_width, level_height)


def show_in_game_win_message():
    font = pygame.font.Font(None, 40)
    small_font = pygame.font.Font(None, 30)

    # Текстовые сообщения
    message = font.render("Вы победили!", True, WHITE)
    restart_message = small_font.render("Нажмите 'R' для рестарта или 'Q' для выхода", True, WHITE)

    # Размер и позиция окна
    window_width, window_height = 500, 150
    window_x = (SCREEN_WIDTH - window_width) // 2
    window_y = (SCREEN_HEIGHT - window_height) // 2

    while True:
        # Отображение текущего игрового экрана
        screen.fill(LIGHT_BLUE)  # Фон игры
        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite))

        # Отрисовка всплывающего окна
        pygame.draw.rect(screen, (0, 0, 0), (window_x, window_y, window_width, window_height), border_radius=15)  # Чёрный фон окна
        pygame.draw.rect(screen, WHITE, (window_x, window_y, window_width, window_height), 3, border_radius=15)  # Белая рамка

        # Отображение текста внутри окна
        screen.blit(message, (SCREEN_WIDTH // 2 - message.get_width() // 2, window_y + 20))
        screen.blit(restart_message, (SCREEN_WIDTH // 2 - restart_message.get_width() // 2, window_y + 80))

        # Обновляем экран
        pygame.display.flip()

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Перезапуск игры
                    return "restart"
                if event.key == pygame.K_q:  # Завершение игры
                    return "quit"

# Изменения в главном игровом цикле:
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление игроком
    keys = pygame.key.get_pressed()
    player.update(keys, platforms)

    # Обновление монет
    coins.update()

    # Сбор монет
    collected_coins = pygame.sprite.spritecollide(player, coins, True)
    player.score += len(collected_coins)

    # Проверка финиша
    if pygame.sprite.collide_rect(player, finish):
        print("🏆 Уровень завершён!")
        print(f"Собрано монет: {player.score}")
        current_level += 1
        if current_level < len(levels):
            load_level(current_level)  # Загружаем следующий уровень
        else:
            result = show_in_game_win_message()
            if result == "restart":
                current_level = 0
                load_level(current_level)
            elif result == "quit":
                running = False

    # Обновление камеры
    camera.update(player)

    # Рендеринг
    screen.fill(LIGHT_BLUE)
    for sprite in all_sprites:
        screen.blit(sprite.image, camera.apply(sprite))

    # Отображение очков
    score_text = pygame.font.Font(None, 36).render(f"Монеты: {player.score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Обновление экрана
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()