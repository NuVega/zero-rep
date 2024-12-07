from abc import ABC, abstractmethod
import random

# ---------------- Оружия ----------------
class Weapon(ABC):
    @abstractmethod
    def attack(self) -> int:
        pass

    @property
    @abstractmethod
    def weapon_type(self) -> str:
        pass

    @property
    @abstractmethod
    def crit_chance(self) -> float:
        pass

    @property
    @abstractmethod
    def crit_multiplier(self) -> float:
        pass

    def calculate_damage(self) -> int:
        base_damage = self.attack()
        # Проверка на крит
        if random.random() < self.crit_chance:
            crit_damage = int(base_damage * self.crit_multiplier)
            print("💥 Критический удар оружием! Урон увеличен!")
            return crit_damage
        return base_damage

class Sword(Weapon):
    def attack(self) -> int:
        print("🗡️ Мощный удар мечом!")
        return random.randint(10, 20)

    @property
    def weapon_type(self) -> str:
        return "slash"

    @property
    def crit_chance(self) -> float:
        return 0.15

    @property
    def crit_multiplier(self) -> float:
        return 2.0

class Bow(Weapon):
    def attack(self) -> int:
        print("🏹 Точный выстрел из лука!")
        return random.randint(5, 15)

    @property
    def weapon_type(self) -> str:
        return "pierce"

    @property
    def crit_chance(self) -> float:
        return 0.2

    @property
    def crit_multiplier(self) -> float:
        return 1.5

class Axe(Weapon):
    def attack(self) -> int:
        print("🪓 Сокрушительный удар топором!")
        return random.randint(15, 25)

    @property
    def weapon_type(self) -> str:
        return "crush"

    @property
    def crit_chance(self) -> float:
        return 0.1

    @property
    def crit_multiplier(self) -> float:
        return 2.5

class Staff(Weapon):
    def attack(self) -> int:
        print("✨ Магический удар посохом!")
        return random.randint(20, 30)

    @property
    def weapon_type(self) -> str:
        return "magic"

    @property
    def crit_chance(self) -> float:
        return 0.15

    @property
    def crit_multiplier(self) -> float:
        return 2.0


class HealthPotion:
    def __init__(self, heal_amount: int):
        self.heal_amount = heal_amount

    def __str__(self):
        return f"Зелье здоровья (+{self.heal_amount} HP)"

# ---------------- Фабрика монстров ----------------
def create_monster():
    monster_data = [
        {
            "name": "Гоблин",
            "health": random.randint(40, 50),
            "res": {"magic": 0.5},       # Гоблин устойчив к магии
            "vul": {"pierce": 1.5},      # Уязвим к луку
            "crit_chance": 0.1,
            "crit_multiplier": 1.5
        },
        {
            "name": "Дракон",
            "health": random.randint(60, 70),
            "res": {"pierce": 0.5, "slash": 0.8},
            "vul": {"magic": 1.5},       # Дракон уязвим к магии
            "crit_chance": 0.2,
            "crit_multiplier": 2.0
        },
        {
            "name": "Скелет",
            "health": random.randint(40, 50),
            "res": {"slash": 0.5},       # Скелет устойчив к slash
            "vul": {"crush": 1.5},       # Уязвим к crush (топору)
            "crit_chance": 0.1,
            "crit_multiplier": 2.0
        },
        {
            "name": "Тролль",
            "health": random.randint(50, 60),
            "res": {"slash": 0.8, "pierce":0.8}, # Тролль устойчив к рубящему и колющему
            "vul": {"magic": 1.5},       # Уязвим к магии
            "crit_chance": 0.1,
            "crit_multiplier": 2.0
        },
        {
            "name": "Огр",
            "health": random.randint(50, 60),
            "res": {"pierce": 0.8},      # устойчив к луку
            "vul": {"crush": 1.5},       # уязвим к топору
            "crit_chance": 0.05,
            "crit_multiplier": 3.0
        }
    ]

    data = random.choice(monster_data)
    return Monster(
        health=data["health"],
        name=data["name"],
        resistances=data["res"],
        vulnerabilities=data["vul"],
        crit_chance=data["crit_chance"],
        crit_multiplier=data["crit_multiplier"]
    )

# ---------------- Монстр ----------------
class Monster:
    def __init__(self, health: int, name: str, resistances: dict, vulnerabilities: dict, crit_chance: float, crit_multiplier: float):
        self.max_health = health
        self.health = health
        self.name = name
        self.resistances = resistances
        self.vulnerabilities = vulnerabilities
        self.crit_chance = crit_chance
        self.crit_multiplier = crit_multiplier

    def take_damage(self, damage: int, weapon_type: str):
        original_damage = damage
        multiplier = 1.0

        if weapon_type in self.resistances:
            multiplier *= self.resistances[weapon_type]

        if weapon_type in self.vulnerabilities:
            multiplier *= self.vulnerabilities[weapon_type]

        final_damage = int(damage * multiplier)

        # Сначала сообщаем о уроне и эффективности:
        if multiplier < 1.0:
            # Урон снижен
            if weapon_type == "pierce":
                print("Стрелы едва пробивают толстую шкуру монстра.")
            elif weapon_type == "slash":
                print("Клинок оставляет лишь поверхностные царапины.")
            elif weapon_type == "crush":
                print("Удар топором кажется недостаточно разрушительным.")
            elif weapon_type == "magic":
                print("Заклинания действуют слабо, монстр почти не страдает.")
        elif multiplier > 1.0:
            # Урон повышен
            if weapon_type == "pierce":
                print("Стрелы находят слабые места, урон повышен!")
            elif weapon_type == "slash":
                print("Клинок легко разрезает плоть, урон усилен!")
            elif weapon_type == "crush":
                print("Топор наносит глубокие и болезненные раны!")
            elif weapon_type == "magic":
                print("Магия сжигает внутренности монстра, урон значительно повышен!")

        # Теперь применяем урон и выводим здоровье
        self.health -= final_damage
        print(f"🩸 {self.name} получает {final_damage} урона.")

        if self.health <= 0:
            print(f"💀 Монстр побежден!")
        else:
            print(f"❤ Здоровье монстра: {self.health}/{self.max_health}")

    def is_alive(self):
        return self.health > 0

    def drop_loot(self):
        if random.random() < 0.5:
            heal_amount = random.randint(15, 30)
            print(f"💰 {self.name} уронил зелье здоровья на +{heal_amount} HP!")
            return HealthPotion(heal_amount)
        return None

    def attack(self, fighter):
        damage = random.randint(5, 15)
        # Крит для монстра
        if random.random() < self.crit_chance:
            crit_damage = int(damage * self.crit_multiplier)
            print("💥 Монстр наносит критический удар!")
            damage = crit_damage

        fighter.take_damage(damage)

# ---------------- Боец ----------------
class Fighter:
    def __init__(self, name: str):
        self.name = name
        self._weapon = None
        self.max_health = 100
        self.health = 100
        self.inventory = []

    def change_weapon(self, new_weapon: Weapon):
        self._weapon = new_weapon
        print(f"{self.name} теперь вооружен: {type(self._weapon).__name__}")

    def attack(self, target: Monster):
        if not self._weapon:
            print("❌ Сначала выберите оружие!")
            return False

        damage = self._weapon.calculate_damage()
        target.take_damage(damage, self._weapon.weapon_type)
        return True

    def take_damage(self, damage: int):
        self.health -= damage
        print(f"💥 {self.name} получает {damage} урона. Осталось здоровья: {self.health}")

    def is_alive(self):
        return self.health > 0

    def heal(self, amount: int):
        old_health = self.health
        self.health = min(self.max_health, self.health + amount)
        print(f"💚 {self.name} восстанавливает {self.health - old_health} HP! (Текущее здоровье: {self.health})")

    def show_inventory(self):
        if not self.inventory:
            print("🎒 Ваш инвентарь пуст.")
        else:
            print("🎒 Ваш инвентарь:")
            for i, item in enumerate(self.inventory, 1):
                print(f"{i}. {item}")

    def use_potion(self):
        if not self.inventory:
            print("❌ У вас нет зелий!")
            return
        print("Выберите зелье для использования:")
        for i, item in enumerate(self.inventory, 1):
            print(f"{i}. {item}")

        while True:
            choice = input("Ваш выбор: ").strip()
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(self.inventory):
                    potion = self.inventory.pop(idx)
                    if isinstance(potion, HealthPotion):
                        self.heal(potion.heal_amount)
                    return
                else:
                    print("❌ Неверный выбор.")
            else:
                print("❌ Введите число.")

# ---------------- Менеджер игры ----------------
class GameManager:
    def __init__(self):
        self.player = None
        self.monster = None
        self.weapons = {
            '1': Sword,
            '2': Bow,
            '3': Axe,
            '4': Staff
        }

    def create_player(self):
        name = input("Введите имя вашего героя: ")
        self.player = Fighter(name)

    def create_monster(self):
        self.monster = create_monster()
        print(f"\n🧟 Появился монстр: {self.monster.name} со здоровьем {self.monster.health}!")

    def choose_weapon_for_player(self):
        self._print_weapon_choices()
        while True:
            choice = input("Ваш выбор: ")
            if choice in self.weapons:
                weapon_class = self.weapons[choice]
                self.player.change_weapon(weapon_class())
                break
            else:
                print("❌ Неверный выбор. Попробуйте снова.")

    def change_weapon_mid_battle(self):
        print("\n⚔️ Смена оружия во время боя!")
        self._print_weapon_choices()
        while True:
            choice = input("Ваш выбор: ")
            if choice in self.weapons:
                weapon_class = self.weapons[choice]
                self.player.change_weapon(weapon_class())
                break
            else:
                print("❌ Неверный выбор. Попробуйте снова.")

    def _print_weapon_choices(self):
        print("\nВыберите оружие:")
        print("1. Меч (slash, 10-20 урона, crit 15%, x2)")
        print("2. Лук (pierce, 5-15 урона, crit 20%, x1.5)")
        print("3. Топор (crush, 15-25 урона, crit 10%, x2.5)")
        print("4. Посох (magic, 20-30 урона, crit 15%, x2)")

    def battle(self):
        self.choose_weapon_for_player()
        print(f"\n⚔️ Битва {self.player.name} против {self.monster.name}!")

        while self.player.is_alive() and self.monster.is_alive():
            print("\nНажмите Enter для удара, 'w' для смены оружия или 'p' для использования зелья.")
            action = input("Ваш выбор: ").strip().lower()

            player_attacked = False

            if action == "w":
                self.change_weapon_mid_battle()
                # Не атакуем
            elif action == "p":
                if not self.player.inventory:
                    print("❌ У вас нет зелий!")
                else:
                    self.player.use_potion()
                # Не атакуем, монстр не контратакует
            else:
                # Игрок атакует
                self.player.attack(self.monster)
                player_attacked = True

            if not self.monster.is_alive():
                print(f"\n🏆 {self.player.name} победил чудовище!")
                loot = self.monster.drop_loot()
                if loot:
                    self.player.inventory.append(loot)
                return True

            # Монстр атакует только если игрок атаковал
            if player_attacked and self.monster.is_alive():
                self.monster.attack(self.player)
                if not self.player.is_alive():
                    print(f"\n💀 {self.player.name} погиб в бою с чудовищем!")
                    return False

    def between_battles_menu(self):
        while True:
            print("\nЧто дальше?")
            print("1. Отправиться в следующий бой")
            print("2. Посмотреть инвентарь")
            print("3. Использовать зелье")
            print("4. Выйти из игры")

            choice = input("Ваш выбор: ").strip()
            if choice == '1':
                return True
            elif choice == '2':
                self.player.show_inventory()
            elif choice == '3':
                if not self.player.inventory:
                    print("❌ У вас нет зелий!")
                else:
                    self.player.use_potion()
            elif choice == '4':
                return False
            else:
                print("❌ Неверный выбор.")

    def start_game(self):
        # Предыстория
        print("Столько боли...")
        input("(Нажмите Enter)")

        print("Столько крови...")
        input("(Нажмите Enter)")

        print("В последнее время вы не видели ничего кроме смерти.")
        input("(Нажмите Enter)")

        print("Порою вы с трудом вспоминаете самого себя...")
        input("(Нажмите Enter)")

        name = input("У человека же есть имя. Как там мое... Ах, да: ")
        while not name.strip():
            name = input("[Введите ваше имя] ")

        print(f"{name}... Шептала она с любовью, когда вы оставались одни.")
        input("(Нажмите Enter)")

        print(f"{name}!!! Отчаянно кричала она, когда вы не могли ее спасти.")
        input("(Нажмите Enter)")

        print("Теперь это имя — негаснущее эхо в вашей голове. Ваш дом был сожжен, ваш народ убит.")
        input("(Нажмите Enter)")

        print("Лишь ярость и жажда мести движут вами вперед.")
        input("(Нажмите Enter)")

        print("Вы поклялись стереть с лица земли каждое отродье, что повстречается вам на пути. И ваш путь еще не закончен...")
        input("(Нажмите Enter)")

        # После ввода имени и истории только теперь создаем игрока
        self.player = Fighter(name)

        player_survived = True

        while True:
            self.create_monster()
            result = self.battle()

            if not result:
                # Игрок умер
                player_survived = False
                print("\n🎲 Потрачено. Ваш поход за местью завершен.")
                break

            continue_game = self.between_battles_menu()
            if not continue_game:
                break

        if player_survived:
            print("👋 Вы уходите в закат. Может быть, вы найдёте новый путь в жизни...")

def main():
    game = GameManager()
    game.start_game()

if __name__ == "__main__":
    main()