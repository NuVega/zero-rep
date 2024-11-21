import json
import os


class User:
    def __init__(self, user_id, name, access_level='user'):
        self.__user_id = user_id
        self.__name = name
        self.__access_level = access_level

    def get_user_id(self):
        return self.__user_id

    def get_name(self):
        return self.__name

    def get_access_level(self):
        return self.__access_level

    def to_dict(self):
        return {
            "id": self.__user_id,
            "name": self.__name,
            "access_level": self.__access_level
        }

    @staticmethod
    def from_dict(data):
        if data['access_level'] == 'admin':
            return Admin(data['id'], data['name'])
        else:
            return User(data['id'], data['name'])

    def __str__(self):
        return f"ID: {self.__user_id}, Name: {self.__name}, Access Level: {self.__access_level}"


class Admin(User):
    def __init__(self, user_id, name):
        super().__init__(user_id, name, access_level='admin')

    def add_user(self, user_list, user):
        user_list.append(user)
        print(f"User {user.get_name()} added successfully.")

    def remove_user(self, user_list, user_id):
        for user in user_list:
            if user.get_user_id() == user_id:
                if user.get_access_level() == 'admin':
                    print("You cannot remove another admin.")
                    return
                user_list.remove(user)
                print(f"User {user.get_name()} removed successfully.")
                return
        print("User not found.")


class SystemOwner:
    def __init__(self):
        self.user_list = []
        self.next_id = 1
        self.filename = "users.json"
        self.load_users()

    def save_users(self):
        data = [user.to_dict() for user in self.user_list]
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def load_users(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.user_list = [User.from_dict(user) for user in data]
                if self.user_list:
                    self.next_id = max(user.get_user_id() for user in self.user_list) + 1

    def add_user(self):
        name = input("Enter user name: ")
        role = input("Enter role ('user' or 'admin'): ").lower()
        if role == 'admin':
            user = Admin(self.next_id, name)
        elif role == 'user':
            user = User(self.next_id, name)
        else:
            print("Invalid role. User not created.")
            return
        self.user_list.append(user)
        self.next_id += 1
        self.save_users()
        print(f"{role.capitalize()} {name} added successfully.")

    def remove_user(self):
        user_id = int(input("Enter the ID of the user to remove: "))
        for user in self.user_list:
            if user.get_user_id() == user_id:
                if isinstance(user, Admin):
                    print("Only the system owner can remove an admin.")
                    return
                self.user_list.remove(user)
                self.save_users()
                print(f"User {user.get_name()} removed successfully.")
                return
        print("User not found.")

    def show_users(self):
        if not self.user_list:
            print("No users in the system.")
            return
        print("Current users in the system:")
        for user in self.user_list:
            print(user)

    def interactive_menu(self):
        while True:
            print("\n--- System Owner Menu ---")
            print("1. Add user")
            print("2. Remove user")
            print("3. Show users")
            print("4. Exit")
            choice = input("Choose an option: ")
            if choice == '1':
                self.add_user()
            elif choice == '2':
                self.remove_user()
            elif choice == '3':
                self.show_users()
            elif choice == '4':
                print("Exiting system.")
                break
            else:
                print("Invalid option. Please try again.")


class AuthenticationSystem:
    def __init__(self):
        self.credentials_file = "credentials.json"
        self.credentials = self.load_credentials()

    def load_credentials(self):
        if os.path.exists(self.credentials_file):
            with open(self.credentials_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        else:
            return {"owner": "password"}  # Default owner credentials

    def save_credentials(self):
        with open(self.credentials_file, 'w', encoding='utf-8') as file:
            json.dump(self.credentials, file, indent=4, ensure_ascii=False)

    def login(self):
        print("--- Login System ---")
        username = input("Enter username: ")
        password = input("Enter password: ")
        if username in self.credentials and self.credentials[username] == password:
            print("Login successful!")
            return True
        else:
            print("Invalid credentials. Access denied.")
            return False

    def add_credentials(self, username, password):
        self.credentials[username] = password
        self.save_credentials()


# Основная программа
auth_system = AuthenticationSystem()
if auth_system.login():
    owner = SystemOwner()
    owner.interactive_menu()