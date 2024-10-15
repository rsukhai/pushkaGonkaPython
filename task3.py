import time

def event_listener(event):
    def decorator(function):
        if not hasattr(function, 'events'):
            function.events = {}
        function.events[event] = function
        print('function.event ', function.events)
        return function
    return decorator

class GameObject():
    def __init__(self, name, health = 100):
        self.name = name
        self.health = health

    def update(self):
        print(f"Updated {self.name}")
        pass 

    def render(self):
        print(f"{self.name} - Health: {self.health}")

    def action (self, obj):
        raise NotImplementedError("Every subclass has to have this methd!!!")
    
    
    def save(self, file):
        file.write(f"{self.name},{self.health}\n")

    def load(cls, line):
        name, health = line.strip().split(',')
        return cls(name, int(health))
    
    def __str__(self):
        return f"{self.name} - Health: {self.health}"
    
class Player(GameObject):
    def __init__(self, name, health = 100, armor = 100):
        super().__init__(name, health)
        self.armor = armor

    @event_listener('on_collision')
    def on_colision(self, obj):
        print(f"Гравець на імя {self.name} спіткнувся об {obj.name}(")

    def action(self, obj):
        if isinstance(obj, Enemy):
            print(f"Гравець на імя {self.name} атакує ворога на імя {obj.name}")
            self.health -= 25
            self.armor -= 5
            obj.health -=50
            obj.armor -=10
        elif isinstance(obj, Item):
            print(f"Гравець на імя {self.name} хоче взяємодіяти з предметом: {obj.name}")

    def save(self, file):
        file.write(f"{self.name},{self.health},{self.armor}\n")

    def load(cls, line):
        name, health, armor = line.strip().split(',')
        return cls(name, int(health), int(armor))

class Enemy(GameObject):
    def __init__(self, name, health = 100, armor = 100):
        super().__init__(name, health)
        self.armor = armor

    @event_listener('on_collision')
    def on_colision(self, obj):
        print(f"Ворог на імя {self.name} спіткнувся об {obj.name}(")

    def action(self, obj):
        if isinstance(obj, Player):
            print(f"Ворог на імя {self.name} атакує гравця на імя {obj.name}")
            self.health -= 25
            self.armor -= 5
            obj.health -= 50
            obj.armor -= 10
        elif isinstance(obj, Item):
            print(f"Ворог на імя {self.name} хоче взяємодіяти з предметом: {obj.name}")

    def save(self, file):
        file.write(f"{self.name},{self.health},{self.armor}\n")

    def load(cls, line):
        name, health, armor = line.strip().split(',')
        return cls(name, int(health), int(armor))
class Item(GameObject):
    def __init__(self, name, health = 100):
        super().__init__(name, health)
        self.health -= 1

    def action(self, other):
        print(f"{other.name} взаємодіє з {self.name}.")

    def save(self, file):
        file.write(f"{self.name},{self.health}\n")

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
    n = 0
    with open(filename, 'r') as file:
        lines = file.readlines()
        player = Player.load(lines[n])
        enemy = Enemy.load(lines[n + 1])
        item = Item.load(lines[n + 1])
    return player, enemy, item

player = Player("Roman")
print(player)
print('\n')

enemy = Enemy("putin")
print(enemy)
print('\n')

item = Item("pistolet")
print(item)
print('\n')

item.action(player)
print(item)
print('\n')

player.action(enemy)
print(enemy)
print(player)
print('\n')

player.on_colision(item)
print('\n')

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
for i in game:
    pass

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

HwomToPlay = input("Виберіть персонажа (player, enemy, item): ")

if HwomToPlay == 'player': 
    command = input("Введіть команду (a - атака на ворога, h - стан гравця, e - взаємодія, q - вихід): ")
    if command == 'a':
        player.action(enemy)  # Атака ворога
    elif command == 'h':
        print(player)  # Виведення стану гравця
    elif command == 'e':
        player.action(item)  # Ворог атакує гравця
    elif command == 'q':
        print("Вихід з гри.")  # Завершення гри
    else:
        print("Невідома команда!")
elif HwomToPlay == 'enemy':
    command = input("Введіть команду (a - атака на персонажа, h - стан ворога, e - взаємодія, q - вихід): ")
    if command == 'a':
        enemy.action(player)  # Атака ворога
    elif command == 'h':
        print(enemy)  # Виведення стану гравця
    elif command == 'e':
        enemy.action(item)  # Ворог атакує гравця
    elif command == 'q':
        print("Вихід з гри.")  # Завершення гри
    else:
        print("Невідома команда!")
else:
    print("Невідома команда!")