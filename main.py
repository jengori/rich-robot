# Rich Robot
# Use the arrow keys to collect coins and avoid monsters
# New level (and increased difficulty) every 10 coins
# Game Over if 3 lives lost

import pygame
from random import randint, choice

images = {"robot": "robot.png",
          "monster": "monster.png",
          "coin": "coin.png",
          }

screen_width = 480
screen_height = 480

starting_lives = 3


class Robot:

    def __init__(self, x: int, y: int, speed: int, lives: int):

        self.robot_image = images["robot"]

        self.x = x
        self.y = y

        self.speed = speed
        self.lives = lives

        self.width = pygame.image.load(self.robot_image).get_width()
        self.height = pygame.image.load(self.robot_image).get_height()

        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False

    def move_left(self):
        self.x -= 1 * self.speed

    def move_right(self):
        self.x += 1 * self.speed

    def move_up(self):
        self.y -= 1 * self.speed

    def move_down(self):
        self.y += 1 * self.speed

    def lose_life(self):
        self.lives -= 1

    def coin_collected(self, coin):
        if coin.x - self.width <= self.x <= coin.x + coin.width and coin.y - self.height <= self.y <= coin.y + coin.height:
            return True

    def collide_with_monster(self, monster):
        if monster.x - self.width <= self.x <= monster.x + monster.width and monster.y - self.height <= self.y <= monster.y + monster.height:
            return True


class Coin:

    def __init__(self, x: int, y: int):
        self.coin_image = images["coin"]
        self.x = x
        self.y = y
        self.width = pygame.image.load(self.coin_image).get_width()
        self.height = pygame.image.load(self.coin_image).get_height()

    def move_coin(self, x: int, y: int):
        self.x = x
        self.y = y


class Monster:

    def __init__(self, x: int, y: int, speed: int, direction: str):
        self.monster_image = images["monster"]
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction
        self.width = pygame.image.load(self.monster_image).get_width()
        self.height = pygame.image.load(self.monster_image).get_height()

    def move(self):
        if self.direction == "RIGHT":
            self.x += 1 * self.speed
        elif self.direction == "LEFT":
            self.x -= 1 * self.speed
        elif self.direction == "UP":
            self.y -= 1 * self.speed
        elif self.direction == "DOWN":
            self.y += 1 * self.speed


class RichRobot:

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Rich Robot")

        self.level = 1
        self.score = 0

        self.robot = Robot(0, 50, 2, 3)
        self.robot.x = (screen_width / 2) - (self.robot.width / 2)
        self.robot.y = (screen_height / 2) - (self.robot.height / 2)

        self.coin = Coin(0, 0)
        self.coin.x = randint(int(screen_width/2), screen_width - self.coin.width)
        self.coin.y = randint(int(screen_height/2), screen_height - self.coin.height)

        self.monsters = []

        self.clock = pygame.time.Clock()

        self.main_loop()

    def main_loop(self):
        counter = 0

        while True:
            counter += 1

            self.check_events()
            self.move_robot()
            for monster in self.monsters:
                monster.move()

            if self.robot.coin_collected(self.coin):
                self.score += 1
                self.move_coin()

            for monster in self.monsters:
                if self.robot.collide_with_monster(monster):
                    self.robot.lose_life()
                    self.robot.x = (screen_width/2) - (self.robot.width/2)
                    self.robot.y = (screen_height/2) - (self.robot.height/2)
                    self.monsters.clear()

            if counter == 200:
                if self.level in [1, 2, 3, 4]:
                    self.generate_monster()
                else:
                    for n in range(self.level - 3):
                        self.generate_monster()
                counter = 0

            self.delete_off_screen_monsters()
            self.set_level()

            self.draw_window()
            self.clock.tick(60)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.robot.moving_left = True
                if event.key == pygame.K_RIGHT:
                    self.robot.moving_right = True
                if event.key == pygame.K_UP:
                    self.robot.moving_up = True
                if event.key == pygame.K_DOWN:
                    self.robot.moving_down = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.robot.moving_left = False
                if event.key == pygame.K_RIGHT:
                    self.robot.moving_right = False
                if event.key == pygame.K_UP:
                    self.robot.moving_up = False
                if event.key == pygame.K_DOWN:
                    self.robot.moving_down = False

    def move_robot(self):
        if self.robot.moving_right and self.robot.x <= screen_width - self.robot.width:
            self.robot.move_right()
        if self.robot.moving_left and self.robot.x >= 0:
            self.robot.move_left()
        if self.robot.moving_up and self.robot.y >= 50:
            self.robot.move_up()
        if self.robot.moving_down and self.robot.y <= screen_height - self.robot.height:
            self.robot.move_down()

    def draw_window(self):
        self.window.fill((23, 89, 74))
        self.window.blit(pygame.image.load(self.robot.robot_image), (self.robot.x, self.robot.y))
        self.window.blit(pygame.image.load(self.coin.coin_image), (self.coin.x, self.coin.y))

        for monster in self.monsters:
            self.window.blit(pygame.image.load(monster.monster_image), (monster.x, monster.y))

        pygame.draw.rect(self.window, (0, 0, 0), (0, 0, 480, 40))
        game_font = pygame.font.SysFont("Courier", 24)
        text = game_font.render("Level: " + str(self.level) + "   Lives: " + str(self.robot.lives) + "   Score: " + str(self.score), True, (255, 255, 255))
        self.window.blit(text, (20, 10))

        if self.game_over():
            self.monsters.clear()
            self.coin.x = 0 - self.coin.width
            self.coin.y = 0
            self.robot.x = -1000
            self.robot.y = -1000
            self.robot.moving_left = False
            self.robot.moving_right = False
            self.robot.moving_up = False
            self.robot.moving_down = False
            game_font_2 = pygame.font.SysFont("Courier", 40)
            game_over_text = game_font_2.render("GAME OVER", True, (255, 255, 255))
            self.window.blit(game_over_text, (130, 220))
        pygame.display.flip()

    def move_coin(self):
        while True:
            self.coin.move_coin(randint(0, screen_width - self.coin.width), randint(50, screen_height - self.coin.height))
            if abs(self.coin.x - self.robot.x) > 50 and abs(self.coin.y - self.robot.y) > 50:
                break

    def generate_monster(self):
        if self.level == 1:
            direction = choice(["RIGHT"])
        elif self.level == 2:
            direction = choice(["LEFT", "RIGHT"])
        elif self.level == 3:
            direction = choice(["LEFT", "RIGHT", "DOWN"])
        else:
            direction = choice(["LEFT", "RIGHT", "UP", "DOWN"])

        new_monster = Monster(0, 0, 1, direction)
        if direction == "LEFT":
            new_monster.x = screen_width + new_monster.width
            new_monster.y = randint(50, screen_height - new_monster.height)
        elif direction == "RIGHT":
            new_monster.x = 0 - new_monster.width
            new_monster.y = randint(50, screen_height - new_monster.height)
        elif direction == "UP":
            new_monster.x = randint(0, screen_width - new_monster.width)
            new_monster.y = screen_height + new_monster.height
        else:
            new_monster.x = randint(0, screen_width - new_monster.width)
            new_monster.y = 0 - new_monster.height

        self.monsters.append(new_monster)

    def delete_off_screen_monsters(self):
        for monster in self.monsters:
            if monster.x < 0 - monster.width or monster.x > screen_width + monster.width or monster.y < 0 - monster.height or monster.y > screen_height + monster.height:
                self.monsters.remove(monster)

    def set_level(self):
        self.level = self.score // 10 + 1

    def game_over(self):
        if self.robot.lives == 0:
            return True


RichRobot()












