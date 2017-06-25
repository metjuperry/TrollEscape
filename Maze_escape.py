#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import randint
import numpy
from heapq import *


# ------------------------------------- Map declarations -------------------------------------

MAP = """###################################X#
# #       #       #     #         # #
# # ##### # ### ##### ### ### ### # #
#       #   # #     #     # # #   # #
##### # ##### ##### ### # # # ##### #
#   # #       #     # # # # #     # #
# # ####### # # ##### ### # ##### # #
# #       # # #   #     #     #   # #
# ####### ### ### # ### ##### # ### #
#     #   # #   # #   #     # #     #
# ### ### # ### # ##### # # # ##### #
#   #   # # #   #   #   # # #   #   #
####### # # # ##### # ### # ### ### #
#     # #     #   # #   # #   #     #
# ### # ##### ### # ### ### ####### #
# #   #     #     #   # # #       # #
# # ##### # ### ##### # # ####### # #
# #     # # # # #     #       # #   #
# ##### # # # ### ##### ##### # #####
# #   # # #     #     # #   #       #
# # ### ### ### ##### ### # ##### # #
# #         #     #       #       # #
#X###################################"""

walls = {0b1010: "┘",
         0b0110: "┐",
         0b0101: "┌",
         0b1001: "└",
         0b1111: "┼",
         0b0011: "─",
         0b1101: "├",
         0b1110: "┤",
         0b1011: "┴",
         0b0111: "┬",
         0b1100: "│",
         0b1000: "│",
         0b0100: "│",
         0b0010: "─",
         0b0001: "─"}


# ------------------------------------- Class declarations -------------------------------------


class Map:
    def __init__(self, layout):
        self.layout = layout
        self.dungeon = [list(line) for line in layout.split('\n')]
        self.bin_dungeon = self.make_binary_dungeon()
        self.width = len(self.dungeon) - 1
        self.height = len(self.dungeon[0]) - 1
        self.obstacles = ["#", "X", "T"]
        for new_wall in walls:
            self.obstacles.append(walls[new_wall])

    def print_map(self):
        for row in self.dungeon:
            print " ".join(row)

    def update_map(self, player, npc):
        self.dungeon = [list(line) for line in self.layout.split('\n')]
        self.dungeon = self.improve_map()
        self.add_map_packs()
        self.dungeon[player.x_coords][player.y_coords] = color_hero(player.char)
        self.dungeon[npc.x_coords][npc.y_coords] = color_enemy(enemy.char)
        player.line_of_sight(self)
        player.vision_cone()
        if player.has_map != 2:
            self.print_visible(player)
        else:
            self.print_map()

    map_packs_coords = []

    def add_map_pack_coords(self, (x, y)):
        self.map_packs_coords.append([x, y])

    def add_map_packs(self):
        for map_pack in self.map_packs_coords:
            self.dungeon[map_pack[0]][map_pack[1]] = "m"

    def get_neighbours(self, piece):
        neighbours = [0, 0, 0, 0]
        # Up, Down, Left, Right

        if self.dungeon[piece[0]][piece[1]] != "#":
            return neighbours

        try:  # Up
            if self.dungeon[piece[0] - 1][piece[1]] == "#":
                if piece[0] - 1 >= 0:
                    neighbours[0] = 1
        except IndexError:
            pass

        try:  # Down
            if self.dungeon[piece[0] + 1][piece[1]] == "#":
                if piece[0] + 1 >= 0:
                    neighbours[1] = 1
        except IndexError:
            pass

        try:  # Left
            if self.dungeon[piece[0]][piece[1] - 1] == "#":
                if piece[1] - 1 >= 0:
                    neighbours[2] = 1
        except IndexError:
            pass

        try:  # Right
            if self.dungeon[piece[0]][piece[1] + 1] == "#":
                if piece[1] + 1 >= 0:
                    neighbours[3] = 1
        except IndexError:
            pass

        return neighbours

    def improve_map(self):
        new_dungeon = []

        for x, row in enumerate(self.dungeon):
            new_dungeon.append([])
            for y, column in enumerate(row):
                if self.dungeon[x][y] == "#":
                    new_dungeon[x].append(walls[int(list_to_bin(self.get_neighbours([x, y])), 2)])
                else:
                    new_dungeon[x].append(self.dungeon[x][y])
        return new_dungeon

    def make_binary_dungeon(self):
        binary_dungeon = []

        for current_row, row in enumerate(self.dungeon):
            binary_dungeon.append([])
            for tile in row:
                if tile == "#" or tile == "X":
                    binary_dungeon[current_row].append(1)
                else:
                    binary_dungeon[current_row].append(0)
        return numpy.array(binary_dungeon)

    def print_visible(self, player):
        for x, row in enumerate(self.dungeon):
            for y, column in enumerate(row):
                if [x, y] not in player.cone:
                    self.dungeon[x][y] = " "
        self.print_map()


class Player:
    def __init__(self, coords, direction):
        self.has_map = 0
        self.x_coords = coords[0]
        self.y_coords = coords[1]
        self.direction = direction.upper()
        self.vision = []
        self.cone = []
        self.char = self.sprite[self.direction]
        self.obstacles = []
        for new_wall in walls:
            self.obstacles.append(walls[new_wall])

    sprite = {'DOWN': 'V', 'LEFT': '<', 'UP': '^', 'RIGHT': '>'}

    def turn(self, direction):
        direction = direction.upper()
        if self.char != self.sprite[direction]:
            self.char = self.sprite[direction]
            self.direction = direction
        else:
            return self.char

    def is_facing_wall(self, layout):
        if self.direction == "UP":
            if layout.dungeon[self.x_coords - 1][self.y_coords] in self.obstacles:
                return True

        elif self.direction == "DOWN":
            if layout.dungeon[self.x_coords + 1][self.y_coords] in self.obstacles:
                return True

        elif self.direction == "LEFT":
            if layout.dungeon[self.x_coords][self.y_coords - 1] in self.obstacles:
                return True

        elif self.direction == "RIGHT":
            if layout.dungeon[self.x_coords][self.y_coords + 1] in self.obstacles:
                return True
        return False

    def is_at_exit(self, layout):
        if layout.dungeon[self.x_coords][self.y_coords] == "X":
            return True
        return False

    def is_at_map(self, layout):
        if layout.dungeon[self.x_coords][self.y_coords] == "m":
            if self.has_map != 2:
                self.has_map += 1
            return True
        return False

    def move(self, layout):
        if not self.is_facing_wall(layout):
            if self.direction == "UP":
                self.x_coords -= 1

            elif self.direction == "DOWN":
                self.x_coords += 1

            elif self.direction == "LEFT":
                self.y_coords -= 1

            elif self.direction == "RIGHT":
                self.y_coords += 1
            return True
        return False

    # TODO: Learn to run

    def input(self, order, layout):
        if self.direction != order.upper():
            self.turn(order)
        else:
            self.move(layout)

    def line_of_sight(self, layout):
        self.obstacles.append("X")
        self.vision = []

        if self.direction == "UP":
            next_x = self.x_coords - 1
            while layout.dungeon[next_x][self.y_coords] not in self.obstacles:
                self.vision.append([next_x, self.y_coords])
                next_x -= 1

        elif self.direction == "DOWN":
            next_x = self.x_coords + 1
            while layout.dungeon[next_x][self.y_coords] not in self.obstacles:
                self.vision.append([next_x, self.y_coords])
                next_x += 1

        elif self.direction == "RIGHT":
            next_y = self.y_coords + 1
            while layout.dungeon[self.x_coords][next_y] not in self.obstacles:
                self.vision.append([self.x_coords, next_y])
                next_y += 1

        elif self.direction == "LEFT":
            next_y = self.y_coords - 1
            while layout.dungeon[self.x_coords][next_y] not in self.obstacles:
                self.vision.append([self.x_coords, next_y])
                next_y -= 1

        self.obstacles.remove("X")

    def vision_cone(self):

        if self.has_map == 0:
            self.cone = []
        try:
            final = self.vision[len(self.vision) - 1]
        except IndexError:
            final = [self.x_coords, self.y_coords]
        if self.direction == "UP" or self.direction == "DOWN":
            for visible in self.vision:
                self.cone.append([visible[0], visible[1] - 1])
                self.cone.append(visible)
                self.cone.append([visible[0], visible[1] + 1])
            if self.direction == "UP":
                self.cone.append([final[0] - 1, final[1]])
            elif self.direction == "DOWN":
                self.cone.append([final[0] + 1, final[1]])

            self.cone.append([self.x_coords, self.y_coords - 1])
            self.cone.append([self.x_coords, self.y_coords])
            self.cone.append([self.x_coords, self.y_coords + 1])

        elif self.direction == "RIGHT" or self.direction == "LEFT":
            for visible in self.vision:
                self.cone.append([visible[0] - 1, visible[1]])
                self.cone.append(visible)
                self.cone.append([visible[0] + 1, visible[1]])
            if self.direction == "RIGHT":
                self.cone.append([final[0], final[1] + 1])
            elif self.direction == "LEFT":
                self.cone.append([final[0], final[1] - 1])

            self.cone.append([self.x_coords - 1, self.y_coords])
            self.cone.append([self.x_coords, self.y_coords])
            self.cone.append([self.x_coords + 1, self.y_coords])


class Enemy(Player):
    def is_at_player(self, player):
        if self.x_coords == player.x_coords and self.y_coords == player.y_coords:
            return True
        return False

    def is_at_map(self, layout):
        pass

    def is_at_exit(self, layout):
        pass

    def pace(self):
        pass

    def move_to(self, layout, target):
        if (self.y_coords, self.y_coords) == (target.x_coords, target.y_coords):
            return True

        movements = {(1, 0): "up",
                     (-1, 0): "down",
                     (0, 1): "left",
                     (0, -1): "right"}

        list_of_coords = (astar(layout.bin_dungeon,
                                (self.x_coords, self.y_coords),
                                (target.x_coords, target.y_coords)))

        direction_to_move = (self.x_coords - list_of_coords[0][0],
                             self.y_coords - list_of_coords[0][1])

        self.input(movements[direction_to_move], layout)


# ------------------------------------- Public functions -------------------------------------

# \033[93m = yellow
# \033[031m = red

def color_hero(char):
    return "\033[093m" + char + "\033[0m"


def color_enemy(char):
    return "\033[031m" + char + "\033[0m"


def heuristic(a, b):
    return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2


def astar(layout, start, goal):
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []

    heappush(oheap, (fscore[start], start))

    while oheap:

        current = heappop(oheap)[1]

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data[::-1]

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor[0] < layout.shape[0]:
                if 0 <= neighbor[1] < layout.shape[1]:
                    if layout[neighbor[0]][neighbor[1]] == 1:
                        continue
                else:
                    # layout.dungeon bound y walls
                    continue
            else:
                # layout.dungeon bound x walls
                continue

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue

            if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heappush(oheap, (fscore[neighbor], neighbor))

    return False


def get_starting_position(dungeon, width, height):
    x = randint(1, width)
    y = randint(1, height)
    obstacles = ['#', 'X', 'm', 'V', '<', '>', '^']

    if dungeon[x][y] in obstacles:
        return get_starting_position(dungeon, width, height)
    return x, y


def get_random_direction():
    wasd = randint(0, 3)

    possibilities = {
        0: "up",
        1: "right",
        2: "left",
        3: "right"
    }

    return possibilities[wasd]


def list_to_bin(given_list):
    result = ""

    for bit in given_list:
        result = str(result) + str(bit)

    return result


def brake():
    print "-------------------------------------------------------------------------"


# ------------------------------------- Object declarations -------------------------------------

# get_starting_position(labyrinth.dungeon, labyrinth.width, labyrinth.height)

labyrinth = Map(MAP)
hero = Player(get_starting_position(labyrinth.dungeon, labyrinth.width, labyrinth.height), get_random_direction())

labyrinth.add_map_pack_coords(get_starting_position(labyrinth.dungeon, labyrinth.width, labyrinth.height))

labyrinth.add_map_pack_coords(get_starting_position(labyrinth.dungeon, labyrinth.width, labyrinth.height))

labyrinth.add_map_pack_coords(get_starting_position(labyrinth.dungeon, labyrinth.width, labyrinth.height))

enemy = Enemy(get_starting_position(labyrinth.dungeon, labyrinth.width, labyrinth.height), get_random_direction())

possible_inputs = {
    "up": "UP",
    "w": "UP",

    "down": "DOWN",
    "s": "DOWN",

    "right": "RIGHT",
    "d": "RIGHT",

    "left": "LEFT",
    "a": "LEFT"
}


# ------------------------------------- Game loop -------------------------------------


def game_loop():
    won = True
    while not hero.is_at_exit(labyrinth):
        labyrinth.update_map(hero, enemy)

        next_step = raw_input("What do you want to do? Up, Down, Left, Right (or WASD) \n").strip()
        while next_step not in possible_inputs:
            print "Wrong input, try again: "
            next_step = raw_input("What do you want to do? Up, Down, Left, Right (or WASD) \n").strip()
        next_step = possible_inputs[next_step.lower()]

        hero.input(next_step, labyrinth)
        if enemy.is_at_player(hero):
            won = False
            break
        elif hero.is_at_exit(labyrinth):
            break
        enemy.move_to(labyrinth, hero)
        if enemy.is_at_player(hero):
            won = False
            break

        if hero.is_at_map(labyrinth):
            if hero.has_map == 1:
                print color_hero("You got map!")
            else:
                print color_hero("Map upgraded!")
            labyrinth.map_packs_coords.remove([hero.x_coords, hero.y_coords])
        brake()

    if won:
        print color_hero("You win!")
    else:
        print color_enemy("You Died!")

if __name__ == "__main__":
    game_loop()
