import json


class Animal:
    def __init__(self, name, species, age):
        self.name = name
        self.species = species
        self.age = age

    def make_sound(self):
        return "Some generic sound"

    def eat(self):
        return f"{self.name} the {self.species} is eating"


class Bird(Animal):
    def __init__(self, name, species, age, can_fly=True):
        super().__init__(name, species, age)
        self.can_fly = can_fly

    def make_sound(self):
        return "chirping"

    def fly(self):
        if self.can_fly:
            return f"{self.name} the {self.species} is flying"
        return f"{self.name} the {self.species} cannot fly, so it just stands there, the longing of an unfulfilled dream in its eyes"


class Mammal(Animal):
    def __init__(self, name, species, age, fur_color):
        super().__init__(name, species, age)
        self.fur_color = fur_color

    def make_sound(self):
        return "growling"

    def run(self):
        return f"{self.name} the {self.species} is running"


class Reptile(Animal):
    def __init__(self, name, species, age, is_venomous=False):
        super().__init__(name, species, age)
        self.is_venomous = is_venomous

    def make_sound(self):
        return "hissing"

    def crawl(self):
        return f"{self.name} the {self.species} is crawling"


class Zoo:
    def __init__(self, name):
        self.name = name
        self.animals = []
        self.staff = []

    def add_animal(self, animal):
        self.animals.append(animal)
        print(f"Animal {animal.name} added to the zoo")

    def add_staff(self, staff_member):
        self.staff.append(staff_member)
        print(f"{staff_member.name} is now a part of our team!")

    def save_to_file(self, filename):
        data = {
            "name": self.name,
            "animals": [
                {
                    "type": animal.__class__.__name__,
                    **vars(animal)
                } for animal in self.animals
            ],
            "staff": [
                {
                    "type": staff.__class__.__name__,
                    **vars(staff)
                } for staff in self.staff
            ]
        }
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    def load_from_file(self, filename):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                self.name = data["name"]
                class_map = {
                    'Animal': Animal,
                    'Bird': Bird,
                    'Mammal': Mammal,
                    'Reptile': Reptile,
                    'ZooKeeper': ZooKeeper,
                    'Veterinarian': Veterinarian,
                    'Cashier': Cashier
                }

                try:
                    self.animals = [
                        class_map[animal_data["type"]](
                            **{k: v for k, v in animal_data.items() if k != "type"}
                        )
                        for animal_data in data["animals"]
                    ]
                except KeyError as e:
                    print(f"Unknown animal type in data: {e}")
                    self.animals = []

                try:
                    self.staff = [
                        class_map[staff_data["type"]](
                            **{k: v for k, v in staff_data.items() if k != "type"}
                        )
                        for staff_data in data["staff"]
                    ]
                except KeyError as e:
                    print(f"Unknown staff type in data: {e}")
                    self.staff = []

                print(f"Zoo data loaded from {filename}.")
        except FileNotFoundError:
            print("File not found!")


class ZooKeeper:
    def __init__(self, name, experience_years):
        self.name = name
        self.experience_years = experience_years

    def feed_animal(self, animal):
        print(f"{self.name} is feeding {animal.name}")
        print(animal.eat())


class Veterinarian:
    def __init__(self, name, experience_years):
        self.name = name
        self.experience_years = experience_years

    def heal_animal(self, animal):
        print(f"{self.name} is healing {animal.name}")
        print(f"{animal.name} is now healthy!")


class Cashier:
    def __init__(self, name):
        self.name = name


def animal_sound(animals):
    if not animals:
        print("No animals in the zoo.")
    else:
        print("All animals are making sounds:")
        for animal in animals:
            print(f"{animal.species} is {animal.make_sound()}")


def get_choice(prompt, options):
    print(f"\n{prompt}")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    while True:
        try:
            choice = int(input("Choose an option: "))
            if 1 <= choice <= len(options):
                return choice
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def add_animal_to_zoo(zoo):
    print("\nAdding a new animal:")

    # Выбор типа животного
    animal_types = ["Bird", "Mammal", "Reptile"]
    animal_type_choice = get_choice("Select type of animal:", animal_types)
    animal_type = animal_types[animal_type_choice - 1]

    species = input("Enter animal species: ")
    name = input("Enter animal name: ")

    # Проверка корректного ввода возраста
    while True:
        age_input = input("Animal age: ").replace(',', '.')
        try:
            age = float(age_input)
            if age < 0:
                raise ValueError("Age cannot be negative.")
            break
        except ValueError:
            print("Invalid age format. Please enter a positive number.")

    if animal_type == "Bird":
        while True:
            can_fly_input = input("Can it fly? (yes/no): ").lower()
            if can_fly_input in ["yes", "no"]:
                can_fly = can_fly_input == "yes"
                animal = Bird(name, species, age, can_fly)
                break
            else:
                print("Invalid input. Please type 'yes' or 'no'.")
    elif animal_type == "Mammal":
        fur_color = input("Enter fur color: ")
        animal = Mammal(name, species, age, fur_color)
    elif animal_type == "Reptile":
        while True:
            is_venomous_input = input("Is it venomous? (yes/no): ").lower()
            if is_venomous_input in ["yes", "no"]:
                is_venomous = is_venomous_input == "yes"
                animal = Reptile(name, species, age, is_venomous)
                break
            else:
                print("Invalid input. Please type 'yes' or 'no'.")

    zoo.add_animal(animal)
    print(f"{name} the {species} has been added to the zoo!")


def add_staff_to_zoo(zoo):
    print("\nAdding a new staff member:")

    # Выбор роли сотрудника
    staff_roles = ["ZooKeeper", "Veterinarian", "Cashier"]
    role_choice = get_choice("Select role:", staff_roles)
    role = staff_roles[role_choice - 1]

    name = input("Enter staff name: ")

    if role in ["ZooKeeper", "Veterinarian"]:
        # Проверка корректного ввода стажа
        while True:
            exp_input = input("Enter years of experience: ").replace(',', '.')
            try:
                experience_years = float(exp_input)
                if experience_years < 0:
                    raise ValueError("Experience cannot be negative.")
                break
            except ValueError:
                print("Invalid format. Please enter a positive number.")
        if role == "ZooKeeper":
            staff = ZooKeeper(name, experience_years)
        else:
            staff = Veterinarian(name, experience_years)
    elif role == "Cashier":
        staff = Cashier(name)

    zoo.add_staff(staff)
    print(f"{name} has been added as a {role}.")


def view_animals(zoo):
    if not zoo.animals:
        print("No animals in the zoo.")
    else:
        print("Animals in the zoo:")
        for i, animal in enumerate(zoo.animals, 1):
            print(f"{i}. {animal.name} ({animal.species}) - {animal.__class__.__name__}, Age: {animal.age}")
        # Спрашиваем, хочет ли пользователь повзаимодействовать с животным
        interact = input("Do you want to observe one of the animals? (yes/no): ").lower()
        if interact == "yes":
            while True:
                try:
                    choice = int(input("Select an animal by number: ")) - 1
                    if 0 <= choice < len(zoo.animals):
                        animal = zoo.animals[choice]
                        if isinstance(animal, Bird):
                            print(animal.fly())
                        elif isinstance(animal, Mammal):
                            print(animal.run())
                        elif isinstance(animal, Reptile):
                            print(animal.crawl())
                        print(f"{animal.name} is {animal.make_sound()}")
                        break
                    else:
                        print("Invalid choice.")
                except ValueError:
                    print("Please enter a valid number.")


def view_staff(zoo):
    if not zoo.staff:
        print("No staff members in the zoo.")
    else:
        print("Staff members in the zoo:")
        for i, staff in enumerate(zoo.staff, 1):
            if isinstance(staff, ZooKeeper):
                role = "ZooKeeper"
                extra_info = f"\nExperience Years: {staff.experience_years}"
            elif isinstance(staff, Veterinarian):
                role = "Veterinarian"
                extra_info = f"\nExperience Years: {staff.experience_years}"
            elif isinstance(staff, Cashier):
                role = "Cashier"
                extra_info = ""
            else:
                role = "Unknown"
                extra_info = ""
            print(f"{i}. {staff.name} - {role} {extra_info}")


def staff_actions(zoo):
    if not zoo.staff:
        print("No staff available.")
        return
    print("\nStaff Members:")
    for i, staff in enumerate(zoo.staff, 1):
        print(f"{i}. {staff.name} ({staff.__class__.__name__})")
    while True:
        try:
            choice = int(input("Select staff member: ")) - 1
            if 0 <= choice < len(zoo.staff):
                staff_member = zoo.staff[choice]
                break
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a valid number.")

    if isinstance(staff_member, (ZooKeeper, Veterinarian)):
        if not zoo.animals:
            print("No animals in the zoo.")
            return
        print("\nAnimals in the zoo:")
        for i, animal in enumerate(zoo.animals, 1):
            print(f"{i}. {animal.name} ({animal.species})")
        while True:
            try:
                animal_choice = int(input("Select an animal to interact with: ")) - 1
                if 0 <= animal_choice < len(zoo.animals):
                    animal = zoo.animals[animal_choice]
                    break
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Please enter a valid number.")

        if isinstance(staff_member, ZooKeeper):
            staff_member.feed_animal(animal)
        elif isinstance(staff_member, Veterinarian):
            staff_member.heal_animal(animal)
    else:
        print(f"{staff_member.name} doesn't have any actions at the moment.")


def zoo_management_system():
    # Проверка наличия сохраненных данных
    zoo = None
    try:
        with open("zoo_data.json", "r") as file:
            data = json.load(file)
            zoo_name = data.get("name", "")
            if zoo_name:
                zoo = Zoo(zoo_name)
                zoo.load_from_file("zoo_data.json")
                print(f"Loaded zoo: {zoo.name}")
    except FileNotFoundError:
        pass

    if not zoo:
        print("No zoo found. Let's create a new one!")
        while True:
            zoo_name = input("Enter the name of the new zoo: ").strip()
            if zoo_name:
                zoo = Zoo(zoo_name)
                break
            else:
                print("Zoo name cannot be empty. Please enter a valid name.")

    while True:
        print(f"\nWelcome to {zoo.name} Management System")
        print("1. Add Data")
        print("2. Edit Data")
        print("3. Delete Data")
        print("4. View Animals")
        print("5. View Staff")
        print("6. Staff Actions")
        print("7. THE SOUNDS OF THE ZOO!")
        print("8. Save and Exit")
        choice = input("Enter your choice: ")

        if choice == "1":  # Add Data
            print("\nAdd Data Menu")
            print("1. Add Animal")
            print("2. Add Staff")
            print("3. Back to Main Menu")
            sub_choice = input("Enter your choice: ")

            if sub_choice == "1":
                add_animal_to_zoo(zoo)
            elif sub_choice == "2":
                add_staff_to_zoo(zoo)
            elif sub_choice == "3":
                continue
            else:
                print("Invalid choice.")

        elif choice == "2":  # Edit Data
            print("\nEdit Data Menu")
            print("1. Edit Zoo Name")
            print("2. Edit Animal Data")
            print("3. Edit Staff Data")
            print("4. Back to Main Menu")
            sub_choice = input("Enter your choice: ")

            if sub_choice == "1":
                new_name = input("Enter new zoo name: ")
                if new_name.strip():
                    zoo.name = new_name
                    print(f"Zoo renamed to {zoo.name}.")
                else:
                    print("Zoo name cannot be empty.")
            elif sub_choice == "2":
                if not zoo.animals:
                    print("No animals to edit.")
                    continue
                print("Select an animal to edit:")
                for i, animal in enumerate(zoo.animals):
                    print(f"{i + 1}. {animal.name}")
                try:
                    animal_choice = int(input("Enter choice: ")) - 1
                    if 0 <= animal_choice < len(zoo.animals):
                        animal = zoo.animals[animal_choice]
                        new_name = input(
                            f"Enter new name for {animal.name} (leave blank to keep current): ") or animal.name
                        animal.name = new_name
                        new_species = input(
                            f"Enter new species for {animal.species} (leave blank to keep current): ") or animal.species
                        animal.species = new_species
                        try:
                            age_input = input(
                                f"Enter new age for {animal.age} (leave blank to keep current): ").replace(',', '.')
                            if age_input:
                                animal.age = float(age_input)
                        except ValueError:
                            print("Invalid age entered.")
                    else:
                        print("Invalid choice.")
                except (IndexError, ValueError):
                    print("Invalid choice.")

            elif sub_choice == "3":
                if not zoo.staff:
                    print("No staff to edit.")
                    continue
                print("Select a staff member to edit:")
                for i, staff in enumerate(zoo.staff):
                    print(f"{i + 1}. {staff.name}")
                try:
                    staff_choice = int(input("Enter choice: ")) - 1
                    if 0 <= staff_choice < len(zoo.staff):
                        staff = zoo.staff[staff_choice]
                        new_name = input(
                            f"Enter new name for {staff.name} (leave blank to keep current): ") or staff.name
                        staff.name = new_name
                        if isinstance(staff, (ZooKeeper, Veterinarian)):
                            try:
                                exp_input = input(
                                    f"Enter new experience years for {staff.experience_years} (leave blank to keep current): ").replace(',', '.')
                                if exp_input:
                                    staff.experience_years = float(exp_input)
                            except ValueError:
                                print("Invalid number of years.")
                    else:
                        print("Invalid choice.")
                except (IndexError, ValueError):
                    print("Invalid choice.")

            elif sub_choice == "4":
                continue
            else:
                print("Invalid choice.")

        elif choice == "3":  # Delete Data
            print("\nDelete Data Menu")
            print("1. Delete Animal")
            print("2. Delete Staff")
            print("3. Back to Main Menu")
            sub_choice = input("Enter your choice: ")

            if sub_choice == "1":
                if not zoo.animals:
                    print("No animals to delete.")
                    continue
                print("Select an animal to delete:")
                for i, animal in enumerate(zoo.animals):
                    print(f"{i + 1}. {animal.name}")
                try:
                    animal_choice = int(input("Enter choice: ")) - 1
                    if 0 <= animal_choice < len(zoo.animals):
                        animal = zoo.animals.pop(animal_choice)
                        print(f"Animal {animal.name} removed from the zoo.")
                    else:
                        print("Invalid choice.")
                except (IndexError, ValueError):
                    print("Invalid choice.")

            elif sub_choice == "2":
                if not zoo.staff:
                    print("No staff to delete.")
                    continue
                print("Select a staff member to delete:")
                for i, staff in enumerate(zoo.staff):
                    print(f"{i + 1}. {staff.name}")
                try:
                    staff_choice = int(input("Enter choice: ")) - 1
                    if 0 <= staff_choice < len(zoo.staff):
                        staff = zoo.staff.pop(staff_choice)
                        print(f"Staff member {staff.name} removed from the zoo.")
                    else:
                        print("Invalid choice.")
                except (IndexError, ValueError):
                    print("Invalid choice.")

            elif sub_choice == "3":
                continue
            else:
                print("Invalid choice.")

        elif choice == "4":  # View Animals
            view_animals(zoo)

        elif choice == "5":  # View Staff
            view_staff(zoo)

        elif choice == "6":  # Staff Actions
            staff_actions(zoo)

        elif choice == "7":
            animal_sound(zoo.animals)

        elif choice == "8":  # Save and Exit
            zoo.save_to_file("zoo_data.json")
            print("Zoo data saved. Exiting.")
            break

        else:
            print("Invalid choice. Please select from the menu options.")


if __name__ == "__main__":
    zoo_management_system()