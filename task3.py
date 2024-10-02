import random
import pickle

class GameObject:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
    
    def update(self):
        pass  # Тут можна оновлювати стан об'єкта

    def render(self):
        print(f"{self.name} знаходиться на позиції ({self.x}, {self.y})")

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

class Player(GameObject):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)

    def handle_input(self, key):
        if key == 'w':
            self.move(0, -1)
        elif key == 's':
            self.move(0, 1)
        elif key == 'a':
            self.move(-1, 0)
        elif key == 'd':
            self.move(1, 0)

class Enemy(GameObject):
    def update(self):
        # Випадковий рух ворога
        self.move(random.choice([-1, 0, 1]), random.choice([-1, 0, 1]))

def save_game(player, enemies, filename="game_state.pkl"):
    with open(filename, 'wb') as f:
        pickle.dump({'player': player, 'enemies': enemies}, f)
    print("Гра збережена!")

def load_game(filename="game_state.pkl"):
    try:
        with open(filename, 'rb') as f:
            data = pickle.load(f)
        print("Гру завантажено!")
        return data['player'], data['enemies']
    except FileNotFoundError:
        print("Файл збереження не знайдено.")
        return None, None

def game_loop(player, enemies):
    while True:
        for enemy in enemies:
            enemy.update()

        player.render()
        for enemy in enemies:
            enemy.render()

        user_input = input("Натисніть w/a/s/d для руху, q щоб вийти, або z щоб зберегти гру: ")
        if user_input == 'q':
            print("Вихід з гри...")
            break
        elif user_input == 'z':
            save_game(player, enemies)
        else:
            player.handle_input(user_input)

player, enemies = load_game()
if not player or not enemies:
    player = Player("Гравець", 0, 0)
    enemies = [Enemy("Ворог1", 5, 5), Enemy("Ворог2", -3, -3)]

game_loop(player, enemies)





