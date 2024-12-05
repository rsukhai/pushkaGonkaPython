import time

def event_listener(event):
    def decorator(function):
        if not hasattr(function, 'events'):
            function.events = {}
        function.events[event] = function
        return function
    return decorator

class GameObject():
    def __init__(self, name, health=100):
        self.name = name
        self.health = health

    def update(self):
        print(f"Updated {self.name}")
        pass 

    def render(self):
        print(f"{self.name} - Health: {self.health}")

    def action(self, obj):
        raise NotImplementedError("Every subclass has to have this method!!!")
    
    def save(self, file):
        file.write(f"{self.name},{self.health}\n")

    @classmethod
    def load(cls, line):
        name, health = line.strip().split(',')
        return cls(name, int(health))
    
    def __str__(self):
        return f"{self.name} - Health: {self.health}"
    
class Player(GameObject):
    def __init__(self, name, health=100, armor=100):
        super().__init__(name, health)
        self.armor = armor

    @event_listener('on_collision')
    def on_colision(self, obj):
        print(f"Гравець на ім'я {self.name} спіткнувся об {obj.name}(")

    def action(self, obj):
        if isinstance(obj, Enemy):
            print(f"Гравець на ім'я {self.name} атакує ворога на ім'я {obj.name}")
            self.health -= 25
            self.armor -= 5
            obj.health -= 50
            obj.armor -= 10
        elif isinstance(obj, Item):
            print(f"Гравець на ім'я {self.name} взаємодіє з предметом: {obj.name}")

    def save(self, file):
        file.write(f"{self.name},{self.health},{self.armor}\n")

    @classmethod
    def load(cls, line):
        name, health, armor = line.strip().split(',')
        return cls(name, int(health), int(armor))

class Enemy(GameObject):
    def __init__(self, name, health=100, armor=100):
        super().__init__(name, health)
        self.armor = armor

    @event_listener('on_collision')
    def on_colision(self, obj):
        print(f"Ворог на ім'я {self.name} спіткнувся об {obj.name}(")

    def action(self, obj):
        if isinstance(obj, Player):
            print(f"Ворог на ім'я {self.name} атакує гравця на ім'я {obj.name}")
            self.health -= 25
            self.armor -= 5
            obj.health -= 50
            obj.armor -= 10
        elif isinstance(obj, Item):
            print(f"Ворог на ім'я {self.name} взаємодіє з предметом: {obj.name}")

    def save(self, file):
        file.write(f"{self.name},{self.health},{self.armor}\n")

    @classmethod
    def load(cls, line):
        name, health, armor = line.strip().split(',')
        return cls(name, int(health), int(armor))

class Item(GameObject):
    def __init__(self, name, health=100):
        super().__init__(name, health)
        self.health -= 1

    def action(self, other):
        print(f"{other.name} взаємодіє з {self.name}.")

    def save(self, file):
        file.write(f"{self.name},{self.health}\n")

    @classmethod
    def load(cls, line):
        name, health = line.strip().split(',')
        return cls(name, int(health))

def save_game(player, enemy, item, filename="game_state.txt"):
    with open(filename, 'w') as file:
        player.save(file)
        enemy.save(file)
        item.save(file)
    print("Гру збережено!")

def load_game(filename="game_state.txt"):
    with open(filename, 'r') as file:
        lines = file.readlines()
        player = Player.load(lines[0])
        enemy = Enemy.load(lines[1])
        item = Item.load(lines[2])
    return player, enemy, item

def game_loop():
    if enemy.health > 0:
        enemy.update()
        player.update()
        print('\n')

        print(f"{player.name} атакує {enemy.name}")
        enemy.health -= 10

        print("Стан об'єктів:")
        player.render()
        enemy.render()
        print('\n')
    yield
    time.sleep(1)

    if enemy.health <= 0:
        print(f"{player.name} виграв!")
        return

game = game_loop()

load_or_new = input("Завантажити збережену гру? (y/n): ")
if load_or_new == 'y':
    try:
        player, enemy, item = load_game()
        print("Гру успішно завантажено!")
    except FileNotFoundError:
        print("Файл збереженої гри не знайдено. Створюємо нову гру.")
else:
    player = Player("Roman")
    enemy = Enemy("putin")
    item = Item("pistolet")

game = True

while game:
    command = input("Введіть команду (a - Атака ворога, h - стан гравця, e - взаємодія, q - вихід): ")
    if command == 'a':
        player.action(enemy)  # Атака ворога
        print(enemy.health)
    elif command == 'h':
        print(player)  # Виведення стану гравця
    elif command == 'e':
        player.action(item)  # Гравець взаємодіє з предметом
    elif command == 'q':
        print("Вихід з гри.")  # Завершення гри
        game = False
    else:
        print("Невідома команда!")

    