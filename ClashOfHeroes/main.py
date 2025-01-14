import random

COMPUTER_NAMES = [
    "Константин", "Джон Уик", "Кратос", "Геракл", "Конан-варвар",
    "Геральт из Ривии", "Мастер Чиф", "Эцио Аудиторе", "Кассиус Клей", "Лара Крофт",
    "Безумный Макс", "Робин Гуд", "Тор", "Локи", "Артас", "Саурон",
    "Чёрная Вдова", "Железный Человек", "Вергилий", "Морфеус",
    "Танос", "Капитан Америка", "Бэтмен", "Супермен", "Джек Воробей",
    "Кафка", "Арагорн", "Леголас", "Гимли", "Гаррош Адский Крик",
    "Джон Сноу", "Кхал Дрого", "Дракс Разрушитель", "Спартак", "Цезарь",
    "Конор Макгрегор", "Хитман", "Кейси Джонс", "Гуннар", "Синбад",
    "Люк Скайуокер", "Мастер Йода", "Дарт Вейдер", "Энакин Скайуокер",
    "Оби-Ван Кеноби", "Кенши", "Саб-Зиро", "Скорпион", "Райден Мэй", "О-Рэн Ишии"
]

# Класс героя
class Hero:
    def __init__(self, name, health=100, attack_power=20, crit_chance=0.2):
        self.name = name
        self.max_health = health  # Устанавливаем максимальное здоровье при создании героя
        self.health = health  # Текущее здоровье
        self.attack_power = attack_power
        self.crit_chance = crit_chance

    def attack(self, other):
        damage = random.randint(0, self.attack_power)  # Случайный урон до максимальной силы удара

        if damage == 0:  # Если урон равен 0, это промах
            print(f"{self.name} атакует {other.name} — промах!")
            return  # Промах завершает атаку без дальнейших действий

        is_critical = random.random() < self.crit_chance  # Проверка на критический удар

        if is_critical:
            damage *= 2
            print(f"{self.name} наносит критический удар! {other.name} получает {damage} урона!")
        else:
            print(f"{self.name} атакует {other.name} и наносит {damage} урона!")

        # Уменьшаем здоровье противника
        other.health -= damage
        if other.health < 0:
            other.health = 0  # Чтобы здоровье не уходило в отрицательные значения

    def is_alive(self):
        return self.health > 0

    def __str__(self):
        return f"{self.name} ({self.health} HP)"


# Класс игры
class Game:
    def __init__(self):
        self.player = None
        self.computer = None

    # Основной метод запуска игры
    def start(self):
        print("Добро пожаловать в 'Битву героев'!")

        # ASCII-арт черепа
        print(r"""
                     ______
                  .-        -.
                 /            \\
                |,  .-.  .-.  ,|
                | )(_o/  \o_)( |
                |/     /\     \|
                (_     ^^     _)
                 \__|IIIIII|__/
                  | \IIIIII/ |
                  \          /
                   `--------`
            """)

        # Проверка ввода для выбора режима
        while True:
            mode = input("Выберите режим игры (1 - Одиночный бой, 2 - Кампания): ")
            if mode in ("1", "2"):
                break  # Выход из цикла при корректном вводе
            print("\nНу же, вы сможете: введите 1 или 2.")

        player_name = input("Введите имя своего героя: ")
        self.player = Hero(player_name)

        if mode == "1":
            computer_name = random.choice(COMPUTER_NAMES)
            self.computer = Hero(computer_name, health=100, attack_power=20)
            self.start_battle()
        elif mode == "2":
            self.start_campaign()
        else:
            print("Неверный выбор, начинаем одиночный бой.")
            computer_name = random.choice(COMPUTER_NAMES)
            self.computer = Hero(computer_name, health=100, attack_power=20)
            self.start_battle()

    # Метод выбора сложности
    def choose_difficulty(self):
        print("Выберите уровень сложности:")
        print("1 - Лёгкий")
        print("2 - Средний")
        print("3 - Сложный")

        while True:
            choice = input("Ваш выбор: ")
            if choice in ("1", "2", "3"):
                if choice == "1":
                    return 0.8  # Противники слабее
                elif choice == "3":
                    return 1.2  # Противники сильнее
                else:
                    return 1.0  # Нормальный режим
            else:
                print("\nЭто не так трудно, просто выберите 1, 2 или 3.")

    # Метод одиночного боя
    def start_battle(self):
        print(f"\n{self.player.name} вступает в бой с {self.computer.name}!")

        while self.player.is_alive() and self.computer.is_alive():
            # Ход игрока
            print(f"\nВаш ход. {self.player} против {self.computer}")
            input("Нажмите Enter, чтобы атаковать...\n")

            # ASCII-арт перекрещённых мечей
            print(r"""
                      /| ________________
                O|===|* >________________>
                      \|
                    """)

            self.player.attack(self.computer)

            if not self.computer.is_alive():
                print(f"\nВы победили {self.computer.name}!")
                return

            # Ход компьютера
            print(f"Теперь ход противника.")
            self.computer.attack(self.player)

            if not self.player.is_alive():
                print(f"\n{self.computer.name} побеждает! А вы — нет.")
                return

    def start_campaign(self):
        num_enemies = 5  # Сколько врагов будет в кампании
        difficulty_multiplier = self.choose_difficulty()  # Уровень сложности

        for i in range(num_enemies):
            # Генерация характеристик врага
            computer_name = random.choice(COMPUTER_NAMES)
            computer_health = int(random.randint(80, 120) * difficulty_multiplier)
            computer_attack = int(random.randint(15, 25) * difficulty_multiplier)
            computer_crit = random.uniform(0.1, 0.3)

            self.computer = Hero(computer_name, health=computer_health, attack_power=computer_attack,
                                 crit_chance=computer_crit)

            print(f"\nВаш противник №{i + 1}: {self.computer.name}")
            print(
                f"Здоровье: {self.computer.health}, Атака: {self.computer.attack_power}, Шанс крита: {self.computer.crit_chance:.2f}")

            # Начинаем бой
            self.start_battle()

            if not self.player.is_alive():
                print(f"{self.player.name} погиб. Кампания завершена!")
                break

            # Если это последний враг, завершаем кампанию
            if i == num_enemies - 1:
                print(f"\nПоздравляем! Вы завершили кампанию, победив всех врагов!")
                break

            # Восстановление здоровья игрока до 100% от текущего максимума
            self.player.health = self.player.max_health

            # Прокачка игрока
            self.level_up()

            # Отображение актуальных характеристик игрока
            print(f"\nТекущие характеристики вашего героя: {self.player.name}")
            print(
                f"Здоровье: {self.player.health}, Атака: {self.player.attack_power}, Шанс крита: {self.player.crit_chance:.2f}")

    def player_turn(self):
        print(f"\nВаш ход. {self.player} против {self.computer}")
        input("Нажмите Enter, чтобы атаковать...")
        self.player.attack(self.computer)
        print(self.computer)

    def computer_turn(self):
        print(f"Теперь ход противника.")
        self.computer.attack(self.player)
        print(self.player)

    def level_up(self):
        print(f"\nПоздравляем, {self.player.name}, вы переходите на новый уровень!")

        while True:
            print("1 - Увеличить здоровье")
            print("2 - Увеличить силу атаки")
            print("3 - Увеличить шанс критического удара")
            choice = input("Выберите улучшение (1, 2 или 3): ")

            if choice == "1":
                increase = 10  # Сколько добавлять к максимальному здоровью
                self.player.max_health += increase
                self.player.health += increase  # Увеличиваем текущее здоровье
                print(
                    f"Максимальное здоровье увеличено до {self.player.max_health}. Текущее здоровье: {self.player.health}.")
                break  # Завершаем цикл, если выбор корректен
            elif choice == "2":
                self.player.attack_power += 5
                print(f"Сила атаки увеличена до {self.player.attack_power}.")
                break  # Завершаем цикл, если выбор корректен
            elif choice == "3":
                self.player.crit_chance += 0.05
                print(f"Шанс критического удара увеличен до {self.player.crit_chance:.2f}.")
                break  # Завершаем цикл, если выбор корректен
            else:
                print("\nНе безобразничайте! Введите 1, 2 или 3.")


# Запуск игры
if __name__ == "__main__":
    game = Game()
    game.start()