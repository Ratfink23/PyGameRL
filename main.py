# Following the Python Roguelike Tutorial by Terrible Programmer
# using PyGame and libtcod
# YouTube for The Terrible Programmer: https://www.youtube.com/channel/UCYpYQNHs2NN-J-UC7Pn4G5A

import string
import pygame
import random
import math
import pickle
import gzip
import datetime
import os

from typing import Tuple, Type, Any
# Libraries
import tcod as libtcod

# Game files
import constants

# Type checking
PosXY = Tuple[int, int]


#
# STRUCTURES
#

class str_Tile:
    def __init__(self, block_path: bool) -> None:
        self.block_path = block_path
        self.seen = False


class str_Preferences:
    def __init__(self):
        self.vol_sound = .5
        self.vol_music = .5


#
# OBJECTS
#

class obj_Assets:
    def __init__(self) -> None:
        self.load_sprites()
        self.load_audio()
        self.sound_adjust()

    def load_sprites(self):
        # Sprites
        self.reptiles = obj_Spritesheet('data/reptiles.png')
        self.aquatic = obj_Spritesheet('data/aquatic_creatures.png')
        self.wall = obj_Spritesheet('data/Wall.png')
        self.floor = obj_Spritesheet('data/Floor.png')
        self.shield = obj_Spritesheet('data/Shield.png')
        self.medwep = obj_Spritesheet('data/MedWep.png')
        self.scroll = obj_Spritesheet('data/Scroll.png')
        self.flesh = obj_Spritesheet('data/Flesh.png')
        self.tile = obj_Spritesheet('data/Tile.png')
        self.rodents = obj_Spritesheet('data/Rodents.png')
        self.light = obj_Spritesheet('data/Light.png')
        self.doors = obj_Spritesheet('data/Door0.png')

        self.A_PLAYER = self.reptiles.get_Animation(2, 'm', 5, 16, 16, (32, 32))
        self.A_SNAKE_01 = self.reptiles.get_Animation(2, 'e', 5, 16, 16, (32, 32))
        self.A_SNAKE_02 = self.reptiles.get_Animation(2, 'i', 5, 16, 16, (32, 32))
        self.A_SNAKE_03 = self.reptiles.get_Animation(2, 'k', 5, 16, 16, (32, 32))
        self.A_ENEMY = self.aquatic.get_Animation(2, 'k', 1, 16, 16, (32, 32))
        self.A_MOUSE = self.rodents.get_Animation(2, 'a', 2, 16, 16, (32, 32))

        self.S_CORPSE = self.flesh.get_Sprite(3, 0, 16, 16, (32, 32))
        self.S_CORPSE_HP = self.flesh.get_Sprite(1, 1, 16, 16, (32, 32))
        self.S_SWORD = self.medwep.get_Sprite(0, 0, 16, 16, (32, 32))
        self.S_SHIELD = self.shield.get_Sprite(0, 0, 16, 16, (32, 32))
        self.S_SCROLL_01 = self.scroll.get_Sprite(0, 0, 16, 16, (32, 32))
        self.S_SCROLL_02 = self.scroll.get_Sprite(0, 1, 16, 16, (32, 32))
        self.S_SCROLL_03 = self.scroll.get_Sprite(1, 4, 16, 16, (32, 32))
        self.S_LAMP = self.light.get_Sprite(4, 0, 16, 16, (32, 32))

        self.S_WALL = self.wall.get_Sprite(3, 3, 16, 16, (32, 32))[0]
        self.S_WALL_UNSEEN = self.wall.get_Sprite(3, 12, 16, 16, (32, 32))[0]

        self.S_FLOOR = self.floor.get_Sprite(1, 4, 16, 16, (32, 32))[0]
        self.S_FLOOR_UNSEEN = self.floor.get_Sprite(1, 10, 16, 16, (32, 32))[0]
        self.S_STAIRS_DOWN = self.tile.get_Sprite(5, 1, 16, 16, (32, 32))
        self.S_STAIRS_UP = self.tile.get_Sprite(4, 1, 16, 16, (32, 32))
        self.S_PORTAL_CLOSED = self.doors.get_Sprite(2, 5, 16, 16, (32, 32))
        self.S_PORTAL_OPEN = self.doors.get_Sprite(3, 5, 16, 16, (32, 32))
        self.MAIN_MENU_BG = pygame.transform.scale(pygame.image.load('data/main_menu_image.jpg'),
                                                   (constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))

        self.animation_dict = {
            "A_PLAYER": self.A_PLAYER,
            "A_SNAKE_01": self.A_SNAKE_01,
            "A_SNAKE_02": self.A_SNAKE_02,
            "A_SNAKE_03": self.A_SNAKE_03,
            "A_ENEMY": self.A_ENEMY,
            "A_MOUSE": self.A_MOUSE,
            "S_CORPSE": self.S_CORPSE,
            "S_CORPSE_HP": self.S_CORPSE_HP,
            "S_SWORD": self.S_SWORD,
            "S_SHIELD": self.S_SHIELD,
            "S_SCROLL_01": self.S_SCROLL_01,
            "S_SCROLL_02": self.S_SCROLL_02,
            "S_SCROLL_03": self.S_SCROLL_03,
            "S_STAIRS_DOWN": self.S_STAIRS_DOWN,
            "S_STAIRS_UP": self.S_STAIRS_UP,
            "S_LAMP": self.S_LAMP,
            "S_PORTAL_CLOSED": self.S_PORTAL_CLOSED,
            "S_PORTAL_OPEN": self.S_PORTAL_OPEN
        }

    def load_audio(self):
        self.snd_master_list = []

        self.background_music = "data/IntroMusic.wav"
        self.snd_hit1 = self.add_sound("data/Hit_Hurt3.wav")
        self.snd_hit2 = self.add_sound("data/Hit_Hurt4.wav")
        self.snd_hard1 = self.add_sound("data/Hit_Hard1.wav")
        self.snd_hard2 = self.add_sound("data/Hit_Hard2.wav")
        self.snd_list_hit = [self.snd_hit1, self.snd_hit2, self.snd_hard1, self.snd_hard2]

    def add_sound(self, file):
        new_sound = pygame.mixer.Sound(file)
        self.snd_master_list.append(new_sound)

        return new_sound

    def sound_adjust(self):
        for sound in self.snd_master_list:
            sound.set_volume(PREF.vol_sound)

        pygame.mixer.music.set_volume(PREF.vol_music)


class obj_Game:
    def __init__(self) -> None:
        self.current_obj = []
        self.message_log = []
        self.maps_next = []
        self.maps_previous = []
        self.current_map, self.current_rooms = map_create()

    def transition_next(self):
        global FOV_CALCULATE

        FOV_CALCULATE = True

        self.maps_previous.append((PLAYER.x, PLAYER.y, self.current_map, self.current_rooms, self.current_obj))

        if len(self.maps_next) == 0:
            # append
            self.current_obj = [PLAYER]
            self.current_map, self.current_rooms = map_create()
            map_place_objects(self.current_rooms)
        else:
            (PLAYER.x, PLAYER.y, self.current_map, self.current_rooms, self.current_obj) = self.maps_next.pop()

            map_make_fov(self.current_map)

    def transition_previous(self):
        global FOV_CALCULATE

        FOV_CALCULATE = True
        if len(self.maps_previous) != 0:
            # insert current level into next at start of list
            self.maps_next.append((PLAYER.x, PLAYER.y, self.current_map, self.current_rooms, self.current_obj))

            (PLAYER.x, PLAYER.y, self.current_map, self.current_rooms, self.current_obj) = self.maps_previous.pop()

        map_make_fov(self.current_map)


class obj_Actor:

    def __init__(self, x: int, y: int, name_object: str, animation_key: str, depth=0,
                 creature: object = None, ai: object = None, container: object = None, item: object = None,
                 equipment: object = None, stairs: object = None, portal: object = None) -> None:
        self.x = x
        self.y = y
        self.name_object = name_object
        self.animation_key = animation_key
        self.depth = depth
        self.animation_speed = 0.5  # TODO change to variable in seconds
        self.animation_cell = 0
        self.state = None

        # animation ticker
        self.flicker = (self.animation_speed / len(ASSETS.animation_dict[self.animation_key]))
        self.flicker_timer = 0

        self.creature = creature
        if creature:
            self.creature.owner = self

        self.ai = ai
        if ai:
            self.ai.owner = self

        self.container = container
        if container:
            self.container.owner = self

        self.item = item
        if item:
            self.item.owner = self

        self.equipment = equipment
        if equipment:
            self.equipment.owner = self
            if not self.item:
                item = com_Item()
                self.item = item
                self.item.owner = self

        self.stairs = stairs
        if stairs:
            self.stairs.owner = self

        self.portal = portal
        if portal:
            self.portal.owner = self

    @property
    def display_name(self) -> str:
        if self.creature:
            return self.creature.name_instance + " " + self.name_object
        elif self.equipment and self.equipment.equipped:
            return self.name_object + " (E)"
        else:
            return self.name_object

    def draw(self) -> None:
        is_visable = libtcod.map_is_in_fov(FOV_MAP, self.x, self.y)
        draw_animation = ASSETS.animation_dict[self.animation_key]
        if is_visable:
            if len(draw_animation) == 1:
                SURFACE_MAP.blit(draw_animation[0], (self.x * constants.CELL_WIDTH, self.y * constants.CELL_HEIGHT))
            elif len(draw_animation) > 1:
                if CLOCK.get_fps() > 0.0:
                    self.flicker_timer += 1 / CLOCK.get_fps()

                if self.flicker_timer >= self.animation_speed:
                    # reset timer
                    self.flicker_timer = 0
                    if self.animation_cell >= len(draw_animation) - 1:
                        # reset animation
                        self.animation_cell = 0
                    else:
                        self.animation_cell += 1

                SURFACE_MAP.blit(draw_animation[self.animation_cell],
                                 (self.x * constants.CELL_WIDTH, self.y * constants.CELL_HEIGHT))

    def distance_to(self, coords: PosXY) -> int:
        ox, oy = coords
        dx = ox - self.x
        dy = oy - self.y

        return int(math.sqrt(dx ** 2 + dy ** 2))

    def move_towards(self, coords: PosXY) -> None:
        ox, oy = coords
        dx = ox - self.x
        dy = oy - self.y

        distance = math.sqrt(dx ** 2 + dy ** 2)
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        self.creature.move(dx, dy)

    def move_away(self, coords: PosXY) -> None:
        ox, oy = coords
        dx = self.x - ox
        dy = self.y - oy

        distance = math.sqrt(dx ** 2 + dy ** 2)
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        self.creature.move(dx, dy)


class obj_Spritesheet:
    """Pull sprite from a sheet"""

    def __init__(self, file_name: str) -> None:
        self.sprite_sheet = pygame.image.load(file_name).convert()
        self.tiledict = {char: index for index, char in enumerate(string.ascii_lowercase, 1)}

    def get_Sprite(self, col: int, row: int, width: int = constants.CELL_WIDTH, height: int = constants.CELL_HEIGHT,
                   scale=None) -> list:
        """ Scale is a Tuple """
        sprite_list = []

        sprite = pygame.Surface([width, height])
        sprite.blit(self.sprite_sheet, (0, 0), [col * width, row * height, width, height])
        sprite.set_colorkey(constants.COLOR_BLACK)

        if scale:
            (new_w, new_h) = scale
            sprite = pygame.transform.scale(sprite, (new_w, new_h))

        sprite_list.append(sprite)

        return sprite_list

    def get_Animation(self, num_sprite: int, col: str, row: int, width: int = constants.CELL_WIDTH,
                      height: int = constants.CELL_HEIGHT, scale: tuple = None) -> list:
        """ Scale is a Tuple """
        sprite_list = []

        for i in range(num_sprite):
            sprite = pygame.Surface([width, height])
            sprite.blit(self.sprite_sheet, (0, 0),
                        [self.tiledict[col] * width + (width * i), row * height, width, height])
            sprite.set_colorkey(constants.COLOR_BLACK)

            if scale:
                (new_w, new_h) = scale
                sprite = pygame.transform.scale(sprite, (new_w, new_h))

            sprite_list.append(sprite)

        return sprite_list


class obj_Room:
    """ Rectangle room lives on the map"""

    def __init__(self, coords: PosXY, size: tuple) -> None:
        self.x1, self.y1 = coords
        self.w, self.h = size

        self.x2 = self.x1 + self.w
        self.y2 = self.y1 + self.h

    @property
    def center(self) -> PosXY:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return (center_x, center_y)

    def intersect(self, other: object) -> bool:
        """ returns true if obj intersects with this one
            Adjusted for the walls """
        object_intersect = (self.x1 <= other.x2 + 1 and self.x2 >= other.x1 - 1 and
                            self.y1 <= other.y2 + 1 and self.y2 >= other.y1 - 1)

        return object_intersect


class obj_Camera:
    def __init__(self):
        self.width = constants.CAMERA_WIDTH
        self.height = constants.CAMERA_HEIGHT
        self.cam_x, self.cam_y = (0, 0)

    def update(self):
        target_x = PLAYER.x * constants.CELL_WIDTH + (constants.CELL_WIDTH / 2)
        target_y = PLAYER.y * constants.CELL_HEIGHT + (constants.CELL_HEIGHT / 2)

        distance_x, distance_y = self.map_dist((target_x, target_y))

        self.cam_x += int(distance_x * .1)
        self.cam_y += int(distance_y * .1)

    def win_to_map(self, coords: PosXY) -> tuple:
        cdx, cdy = self.camera_dist(coords)
        map_p_x = self.cam_x + cdx
        map_p_y = self.cam_y + cdy

        return (map_p_x, map_p_y)

    def map_dist(self, coords: PosXY) -> tuple:
        new_x, new_y = coords
        dx = new_x - self.cam_x
        dy = new_y - self.cam_y

        return (dx, dy)

    def camera_dist(self, coords: PosXY) -> tuple:
        new_x, new_y = coords
        dx = new_x - (self.width / 2)
        dy = new_y - (self.height / 2)

        return (dx, dy)

    @property
    def rectangle(self):
        pos_rect = pygame.Rect((0, 0), (constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))
        pos_rect.center = (self.cam_x, self.cam_y)

        return pos_rect

    @property
    def map_pos(self) -> PosXY:
        map_x = int(self.cam_x / constants.CELL_WIDTH)
        map_y = int(self.cam_y / constants.CELL_HEIGHT)

        return (map_x, map_y)


#
# COMPONENTS
#

class com_Creature:
    def __init__(self, name_instance: str, max_hp: int = 10, base_atk: int = 2, base_def: int = 0,
                 death_function: Any = None):
        self.name_instance = name_instance
        self.hp = max_hp
        self.base_atk = base_atk
        self.base_def = base_def
        self.max_hp = max_hp
        self.death_function = death_function

    def move(self, dx: int, dy: int) -> None:
        tile_is_wall = (GAME.current_map[self.owner.x + dx][self.owner.y + dy].block_path == True)
        target = map_check_for_creatures(self.owner.x + dx, self.owner.y + dy, self.owner)

        if target:
            self.attack(target)

        if not tile_is_wall and target == None:
            self.owner.x += dx
            self.owner.y += dy

    def attack(self, target: Type[obj_Actor]) -> None:
        damage = self.power - target.creature.defense
        game_message(
            ('{0} attacks {1} for {2} damage'.format(self.name_instance, target.creature.name_instance, damage)),
            constants.COLOR_WHITE)
        target.creature.take_damage(damage)

        if damage > 0 and self.owner is PLAYER:
            hit_sound = random.choice(ASSETS.snd_list_hit)
            hit_sound.play()

    def take_damage(self, damage: int) -> None:
        self.hp -= damage
        game_message((self.name_instance + "'s hp is " + str(self.hp) + '/' + str(self.max_hp)), constants.COLOR_WHITE)
        if self.hp <= 0:
            if self.death_function is not None:
                self.death_function(self.owner)

    def heal_self(self, val: int) -> None:
        self.hp += val
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        game_message((self.name_instance + "'s hp is " + str(self.hp) + '/' + str(self.max_hp)), constants.COLOR_WHITE)

    @property
    def power(self) -> int:
        total = self.base_atk

        if self.owner.container:
            obj_bonus = [obj.equipment.attack_bonus for obj in self.owner.container.equipped_items]
            for bonus in obj_bonus:
                total += bonus
        return total

    @property
    def defense(self) -> int:
        total = self.base_def

        if self.owner.container:
            obj_bonus = [obj.equipment.defense_bonus for obj in self.owner.container.equipped_items]
            for bonus in obj_bonus:
                total += bonus
        return total


class com_Item:
    def __init__(self, use_function: Any = None, value: Any = 0, weight: float = 0.0, volume: float = 0.0):
        self.weight = weight
        self.volume = volume
        self.use_function = use_function
        self.value = value
        self.container = None

    def pickup(self, actor: Type[obj_Actor]) -> None:
        if actor.container:
            if actor.container.volume + self.volume > actor.container.base_volume:
                # TODO wrong msg if actor is a monster
                game_message('Not enough room to pick up')
            else:
                game_message('Picking up items')
                actor.container.inventory.append(self.owner)
                GAME.current_obj.remove(self.owner)
                self.container = actor.container

    def drop(self, new_x: int, new_y: int) -> None:
        # TODO need to select the item to drop
        GAME.current_obj.append(self.owner)
        self.remove()
        self.owner.x = new_x
        self.owner.y = new_y
        game_message('Item Dropped')

    def use(self) -> None:
        """ Triggers the use of the Item"""

        if self.owner.equipment:
            self.owner.equipment.toggle_equipped()
            return

        if self.use_function:
            result = self.use_function(self.container.owner, self.value)

        if result is None:
            self.remove()

    def remove(self) -> None:
        self.container.inventory.remove(self.owner)
        self.container = None

    ## TODO view item


class com_Container:
    def __init__(self, volume: float = 10.0, inventory: list = []) -> None:
        # List for inventory
        self.inventory = inventory
        self.base_volume = volume

    ## TODO get names from inventory

    @property
    ## TODO get the volume
    def volume(self):
        return 0.0

    ## TODO get weight of items

    @property
    def equipped_items(self) -> list:
        list_equipped = [obj for obj in self.inventory if obj.equipment and obj.equipment.equipped]

        return list_equipped


class com_Equipment:
    def __init__(self, attack_bonus: int = 0, defense_bonus: int = 0, slot: str = None):
        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus
        self.slot = slot
        self.equipped = False

    def toggle_equipped(self) -> None:
        if self.equipped:
            self.unequip()
        else:
            self.equip()

    def equip(self) -> None:
        # check equipment in slot and swap
        equ_items = self.owner.item.container.equipped_items
        for item in equ_items:
            if item.equipment.slot == self.slot:
                item.equipment.unequip()
        self.equipped = True
        game_message('item equipped')

    def unequip(self) -> None:
        self.equipped = False
        game_message('item unequipped')


class com_Stairs:
    def __init__(self, downwards=True):
        self.downwards = downwards

    def use(self):
        if self.downwards:
            GAME.transition_next()
        else:
            GAME.transition_previous()


class com_Portal:
    def __init__(self, key: str):
        self.portalclosed = "S_PORTAL_CLOSED"
        self.portalopen = "S_PORTAL_OPEN"
        self.key = key
        self.open = False
        self.found_key = False

    def update(self):
        for item in PLAYER.container.inventory:
            if self.key == item.item.value:
                self.found_key = True
                break
            else:
                self.found_key = False

        if self.found_key and not self.open:
            self.owner.animation_key = self.portalopen
            self.open = True
        elif not self.found_key and self.open:
            self.open = False
            self.owner.animation_key = self.portalclosed


#
# AI
#

class ai_Confused:
    def __init__(self, old_ai: object, turns: int):
        self.old_ai = old_ai
        self.turns = turns

    def take_turn(self) -> None:
        if self.turns >= 0:
            self.owner.creature.move(libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1))
            self.turns -= self.turns
        else:
            self.owner.ai = self.old_ai
            self.owner.ai.owner = self.owner
            game_message('{0} has recovered'.format(self.owner.name_object), constants.COLOR_RED)


class ai_Chase:
    def take_turn(self) -> None:
        monster = self.owner
        if libtcod.map_is_in_fov(FOV_MAP, monster.x, monster.y):
            if monster.distance_to((PLAYER.x, PLAYER.y)) >= 2:
                monster.move_towards((PLAYER.x, PLAYER.y))
            else:
                monster.creature.attack(PLAYER)


class ai_Flee:
    def take_turn(self) -> None:
        monster = self.owner
        if libtcod.map_is_in_fov(FOV_MAP, monster.x, monster.y):
            monster.move_away((PLAYER.x, PLAYER.y))


#
# DEATH
#

def death_snake(snake: Type[obj_Actor]) -> None:
    game_message(snake.creature.name_instance + ' is dead', constants.COLOR_RED)

    snake.animation_key = "S_CORPSE"
    snake.depth = constants.DEPTH_CORPSE
    snake.creature = None
    snake.ai = None


def death_mouse(mouse: Type[obj_Actor]) -> None:
    game_message(mouse.creature.name_instance + ' is dead. Eat for more health', constants.COLOR_GREEN)
    mouse.animation_key = "S_CORPSE_HP"
    mouse.depth = constants.DEPTH_CORPSE
    mouse.creature = None
    mouse.ai = None


def death_player(player: Type[obj_Actor]) -> None:
    player.state = "STATUS_DEAD"
    SURFACE_MAIN.fill(constants.COLOR_BLACK)
    draw_text(SURFACE_MAIN, "You're Dead", constants.FONT_TITLE,
              (constants.CAMERA_WIDTH / 2, constants.CAMERA_HEIGHT / 2),
              constants.COLOR_RED, center=True)

    filename = ("data\legacy_" + player.name_object + "." + datetime.date.today().strftime("%Y%B%d"))
    legacy_file = open(filename, 'a+')
    for message, color in GAME.message_log:
        legacy_file.write(message + "\n")

    files_delete('data\savegame')

    pygame.display.update()
    pygame.time.wait(2000)


def win_player(player: Type[obj_Actor]) -> None:
    player.state = "STATUS_WIN"
    SURFACE_MAIN.fill(constants.COLOR_BLACK)
    game_message('{0} has escaped the Snake Pit'.format(player.name_object), constants.COLOR_WHITE)
    draw_text(SURFACE_MAIN, "You're Escaped!", constants.FONT_TITLE,
          (constants.CAMERA_WIDTH / 2, constants.CAMERA_HEIGHT / 2),
          constants.COLOR_WHITE, center=True)

    filename = ("data\win_" + player.name_object + "." + datetime.date.today().strftime("%Y%B%d"))
    legacy_file = open(filename, 'a+')
    for message, color in GAME.message_log:
        legacy_file.write(message + "\n")

    files_delete('data\savegame')

    pygame.display.update()
    pygame.time.wait(2000)

#
# MAPPING
#

def map_create():
    new_map = [[str_Tile(True) for y in range(0, constants.MAP_HEIGHT)] for x in range(0, constants.MAP_WIDTH)]

    list_rooms = []
    for i in range(constants.MAP_MAX_ROOMS):
        w = random.randint(constants.ROOM_MIN_WIDTH, constants.ROOM_MAX_WIDTH)
        h = random.randint(constants.ROOM_MIN_HEIGHT, constants.ROOM_MAX_HEIGHT)

        x = random.randint(2, constants.MAP_WIDTH - w - 2)
        y = random.randint(2, constants.MAP_HEIGHT - h - 2)

        new_room = obj_Room((x, y), (w, h))
        intersect_check = False
        for other_room in list_rooms:
            if new_room.intersect(other_room):
                intersect_check = True
                break

        if not intersect_check:
            map_create_room(new_map, new_room)
            center = new_room.center
            if len(list_rooms) != 0:
                prev_center = list_rooms[-1].center
                map_create_tunnels(center, prev_center, new_map)

            list_rooms.append(new_room)

    map_make_fov(new_map)

    return (new_map, list_rooms)


def map_place_objects(room_list: list) -> None:
    top_level = (len(GAME.maps_previous) == 0)

    for room in room_list:
        first_room = (room == room_list[0])
        last_room = (room == room_list[-1])

        if first_room:
            PLAYER.x, PLAYER.y = room.center
            if not top_level:
                gen_Stairs(room.center, downwards=False)
            else:
                gen_Portal(room.center, key='Magic Lamp')

        if last_room:
            if len(GAME.maps_previous) == constants.MAP_MAX_DEPTH-1:
                gen_magic_lamp(room.center, "Magic Lamp")
            else:
                gen_Stairs(room.center, downwards=True)

        item_x = random.randint(room.x1, room.x2)
        item_y = random.randint(room.y1, room.y2)
        gen_item((item_x, item_y))

        mob_x = random.randint(room.x1, room.x2)
        mob_y = random.randint(room.y1, room.y2)
        gen_enemy((mob_x, mob_y))


def map_create_tunnels(coords1: PosXY, coords2: PosXY, new_map: list) -> None:
    x1, y1 = coords1
    x2, y2 = coords2
    coin = (random.randint(0, 1) == 1)

    if coin:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            new_map[x][y1].block_path = False
        for y in range(min(y1, y2), max(y1, y2) + 1):
            new_map[x2][y].block_path = False
    else:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            new_map[x1][y].block_path = False
        for x in range(min(x1, x2), max(x1, x2) + 1):
            new_map[x][y2].block_path = False


def map_create_room(new_map, new_room):
    for x in range(new_room.x1, new_room.x2 + 1):
        for y in range(new_room.y1, new_room.y2 + 1):
            new_map[x][y].block_path = False


def map_obj_at_loc(loc_x, loc_y):
    """ Returns a list of objects at x,y"""

    objects = [obj for obj in GAME.current_obj
               if obj.x == loc_x and obj.y == loc_y]

    return objects


def map_check_for_creatures(x, y, exclude_obj=None):
    target = None
    if exclude_obj:
        # target self
        for obj in GAME.current_obj:
            if (obj is not exclude_obj and obj.x == x and obj.y == y and obj.creature):
                target = obj
    else:
        # Target self and others
        for obj in GAME.current_obj:
            if (obj.x == x and obj.y == y and obj.creature):
                target = obj

    if target:
        return target


def map_make_fov(incoming_map):
    global FOV_MAP

    FOV_MAP = libtcod.map_new(constants.MAP_WIDTH, constants.MAP_HEIGHT)
    for y in range(constants.MAP_HEIGHT):
        for x in range(constants.MAP_WIDTH):
            libtcod.map_set_properties(FOV_MAP, x, y,
                                       not incoming_map[x][y].block_path, not incoming_map[x][y].block_path)


def map_calculate_fov():
    global FOV_CALCULATE

    if FOV_CALCULATE:
        FOV_CALCULATE = False
        libtcod.map_compute_fov(FOV_MAP, PLAYER.x, PLAYER.y, constants.TORCH_RAD, constants.FOV_LIGHT_WALLS,
                                constants.FOV_ALGO)


def map_find_line(coords1, coords2):
    x1, y1 = coords1
    x2, y2 = coords2
    libtcod.line_init(x1, y1, x2, y2)
    line_x, line_y = libtcod.line_step()
    coord_list = []

    if x1 == x2 and y1 == y2:
        return [(x1, y1)]

    while line_x is not None:
        coord_list.append((line_x, line_y))
        # Step Step
        line_x, line_y = libtcod.line_step()

    return coord_list


def map_find_radius(coords, radius):
    # Simple radius not trimming edges
    center_x, center_y = coords
    cell_list = []

    for x in range((center_x - radius), (center_x + radius + 1)):
        for y in range((center_y - radius), (center_y + radius + 1)):
            cell_list.append((x, y))

    return cell_list


#
#   DRAWING
#

def draw_game():
    global SURFACE_MAIN

    # clear the surface
    SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)
    SURFACE_MAP.fill(constants.COLOR_BLACK)

    CAMERA.update()

    # draw the map
    draw_map(GAME.current_map)

    # draw character
    for obj in sorted(GAME.current_obj, key=lambda obj: obj.depth, reverse=True):
        obj.draw()

    SURFACE_MAIN.blit(SURFACE_MAP, (0, 0), CAMERA.rectangle)

    draw_debug()
    draw_message()

    # update the display
    pygame.display.flip()


def draw_map(map_to_draw):
    cam_x, cam_y = CAMERA.map_pos
    display_map_w = constants.CAMERA_WIDTH / constants.CELL_WIDTH
    display_map_h = constants.CAMERA_WIDTH / constants.CELL_HEIGHT

    render_w_min = int(cam_x - (display_map_w / 2))
    render_h_min = int(cam_y - (display_map_h / 2))
    render_w_max = int(cam_x + (display_map_w / 2))
    render_h_max = int(cam_y + (display_map_h / 2))

    if render_w_min < 0: render_w_min = 0
    if render_h_min < 0: render_h_min = 0
    if render_w_max > constants.MAP_WIDTH: render_w_max = constants.MAP_WIDTH
    if render_h_max > constants.MAP_HEIGHT: render_h_max = constants.MAP_HEIGHT

    for x in range(render_w_min, render_w_max):
        for y in range(render_h_min, render_h_max):

            is_visible = libtcod.map_is_in_fov(FOV_MAP, x, y)

            if is_visible:
                map_to_draw[x][y].seen = True
                if map_to_draw[x][y].block_path:
                    # draw wall
                    SURFACE_MAP.blit(ASSETS.S_WALL, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))
                else:
                    # draw floor
                    SURFACE_MAP.blit(ASSETS.S_FLOOR, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))
            elif map_to_draw[x][y].seen:
                if map_to_draw[x][y].block_path:
                    # draw wall
                    SURFACE_MAP.blit(ASSETS.S_WALL_UNSEEN, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))
                else:
                    # draw floor
                    SURFACE_MAP.blit(ASSETS.S_FLOOR_UNSEEN, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))


def draw_debug():
    draw_text(SURFACE_MAIN,
              "FPS: " + str(int(CLOCK.get_fps())),
              constants.FONT_DEBUG,
              (0, 0),
              constants.COLOR_RED,
              constants.COLOR_BLACK)


def draw_text(display_surface, text, font, coords: PosXY, text_color, back_color=None, center=False):
    text_surf, text_rect = helper_text_object(text, font, text_color, back_color)
    if not center:
        text_rect.topleft = coords
    else:
        text_rect.center = coords

    display_surface.blit(text_surf, text_rect)


def draw_message():
    """ Draw Message Logger Text showing only the MESSAGE_LOG_NUM amount of messages"""
    if len(GAME.message_log) <= constants.MESSAGE_LOG_NUM:
        to_draw = GAME.message_log
    else:
        to_draw = GAME.message_log[-constants.MESSAGE_LOG_NUM:]
    text_height = helper_text_height(constants.FONT_MESSAGE)
    start_y = (constants.CAMERA_HEIGHT - (constants.MESSAGE_LOG_NUM * text_height)) - 5

    i = 0
    for message, color in to_draw:
        draw_text(SURFACE_MAIN, message, constants.FONT_MESSAGE, (0, start_y + (i * text_height)), color)
        i += 1


def draw_tile_rect(coords: PosXY, color=constants.COLOR_WHITE, marker=None):
    """ Draws a Cell rect on the MAP surface """
    new_surface = pygame.Surface((constants.CELL_WIDTH, constants.CELL_HEIGHT))
    new_surface.fill(color)
    new_surface.set_alpha(100)
    draw_text(new_surface, marker, constants.FONT_CURSOR_TEXT,
              coords=(constants.CELL_WIDTH / 2, constants.CELL_HEIGHT / 2),
              text_color=constants.COLOR_BLACK, center=True)
    SURFACE_MAP.blit(new_surface, coords)


#
# HELPERS
#

def helper_text_object(text, font, color, bg_color):
    if bg_color:
        text_surface = font.render(text, False, color, bg_color)
    else:
        text_surface = font.render(text, False, color)

    return text_surface, text_surface.get_rect()


def helper_text_height(font):
    font_rect = font.render('a', False, (0, 0, 0)).get_rect()

    return font_rect.height


def helper_text_width(font, text):
    font_rect = font.render(text, False, (0, 0, 0)).get_rect()

    return font_rect.width


def screen_mid_offset(width, height):
    """ Determines the middle point offset for a screen or text """

    return (constants.CAMERA_WIDTH - width) / 2, (constants.CAMERA_HEIGHT - height) / 2


#
# MAGIC
#

def cast_heal(caster, val):
    if caster.creature.hp == caster.creature.max_hp:
        game_message('{0} already at full health'.format(caster.name_object), constants.COLOR_WHITE)
        return 'cancelled'
    else:
        game_message('{0} healed for {1}'.format(caster.name_object, val), constants.COLOR_LIME)
        caster.creature.heal_self(val)

    return None


def cast_key(caster, key):
    for obj in map_obj_at_loc(caster.x, caster.y):
        if obj.portal and obj.portal.key == key:
            win_player(caster)
            return 'cancelled'

    game_message('This is a key to a portal. Stand on the portal and try again', constants.COLOR_WHITE)
    return 'cancelled'


def cast_lightning(caster, damage_range=(5, 5)):
    cast_damage, cast_range = damage_range
    caster_pos = (caster.x, caster.y)
    end_point = menu_tile_select(caster_pos, cast_range)
    if end_point:
        spell_path = map_find_line(caster_pos, end_point)
    else:
        return 'cancelled'

    for i, (tile_x, tile_y) in enumerate(spell_path):
        target = map_check_for_creatures(tile_x, tile_y)
        # draw the lighting bolt!! Zappy Zap Zap
        draw_tile_rect((tile_x * constants.CELL_WIDTH, tile_y * constants.CELL_HEIGHT), constants.COLOR_YELLOW)
        pygame.display.flip()
        CLOCK.tick(constants.MAX_FPS)
        if target and i != 0:
            target.creature.take_damage(cast_damage)
    return


def cast_fireball(caster, damage_range_radius=(5, 5, 1)):
    cast_damage, cast_range, cast_radius = damage_range_radius
    caster_pos = (caster.x, caster.y)
    target_select = menu_tile_select(caster_pos, cast_range, wall_blocking=False, enemy_blocking=True,
                                     radius=cast_radius)
    if target_select:
        cells_to_damage = map_find_radius(target_select, cast_radius)
    else:
        return 'cancelled'

    for tile_x, tile_y in cells_to_damage:
        target = map_check_for_creatures(tile_x, tile_y)
        # draw the fireball!! Burn Baby Burn
        draw_tile_rect((tile_x * constants.CELL_WIDTH, tile_y * constants.CELL_HEIGHT), constants.COLOR_RED)
        pygame.display.flip()
        CLOCK.tick(constants.MAX_FPS * 2 * cast_radius)
        if target:
            target.creature.take_damage(cast_damage)
    return


def cast_confusion(caster, turns_range=(3, 5)):
    cast_turns, cast_range = turns_range
    caster_pos = (caster.x, caster.y)
    end_point = menu_tile_select(caster_pos, cast_range, enemy_blocking=False, wall_blocking=True)
    if end_point:
        tile_x, tile_y = end_point
        target = map_check_for_creatures(tile_x, tile_y, PLAYER)
        if target:
            target_ai = target.ai
            confused_ai = ai_Confused(target_ai, cast_turns)
            target.ai = confused_ai
            target.ai.owner = target
            game_message('{0} has been confused'.format(target.name_object), constants.COLOR_GREEN)
        return
    else:
        return 'cancelled'


#
# IU
#

class ui_button:
    def __init__(self, surface, button_text, size, center_coords,
                 color_box_mouseover=constants.COLOR_RED,
                 color_box_default=constants.COLOR_GREEN,
                 color_text_mouseover=constants.COLOR_GREY,
                 color_text_default=constants.COLOR_GREY):

        self.surface = surface
        self.button_text = button_text
        self.size = size
        self.center_coords = center_coords

        self.c_box_mo = color_box_mouseover
        self.c_box_default = color_box_default
        self.c_text_mo = color_text_mouseover
        self.c_text_default = color_text_default
        self.current_c_box = color_box_default
        self.current_c_text = color_text_default

        self.rect = pygame.Rect((0, 0), size)
        self.rect.center = center_coords

    def update(self, player_input):
        mouse_click = False

        local_events, local_mousexy = player_input
        mouse_x, mouse_y = local_mousexy

        mouse_over = (self.rect.left <= mouse_x <= self.rect.right
                      and self.rect.bottom >= mouse_y >= self.rect.top)

        for event in local_events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: mouse_click = True

        if mouse_over and mouse_click:
            return True

        if mouse_over:
            self.current_c_box = self.c_box_mo
            self.current_c_text = self.c_text_mo
        else:
            self.current_c_box = self.c_box_default
            self.current_c_text = self.c_text_default

    def draw(self):
        pygame.draw.rect(self.surface, self.current_c_box, self.rect)
        draw_text(self.surface, self.button_text, constants.FONT_DEBUG, self.center_coords,
                  self.current_c_text, self.current_c_box, center=True)


class ui_slider:
    def __init__(self, surface, size, center_coords, bg_color, fg_color, value):
        self.surface = surface
        self.size = size
        self.center_coords = center_coords

        self.rect = pygame.Rect((0, 0), size)
        self.rect.center = center_coords

        self.bg_color = bg_color
        self.fg_color = fg_color
        self.value = value

        self.slider_rect = pygame.Rect((0, 0), size)
        self.slider_rect.width = self.rect.width * self.value
        self.slider_rect.topleft = self.rect.topleft

    def update(self, player_input):
        mouse_down = pygame.mouse.get_pressed()[0]

        local_events, local_mousexy = player_input
        mouse_x, mouse_y = local_mousexy

        mouse_over = (self.rect.left <= mouse_x <= self.rect.right
                      and self.rect.bottom >= mouse_y >= self.rect.top)

        if mouse_down and mouse_over:
            self.value = (mouse_x - self.rect.left) / self.rect.width
            self.slider_rect.width = self.rect.width * self.value

    def draw(self):
        pygame.draw.rect(self.surface, self.bg_color, self.rect)
        pygame.draw.rect(self.surface, self.fg_color, self.slider_rect)


#
# MENU
#

def menu_main():
    game_init()
    menu_running = True

    title_y = constants.CAMERA_HEIGHT / 2 - 40
    title_x = constants.CAMERA_WIDTH / 2
    title_text = "Python RL"

    # Button Alignment
    button_offset = 40

    # draw menu
    menu_build = True

    start_button = ui_button(SURFACE_MAIN, 'New Game', (160, 30), (title_x, title_y + button_offset))
    continue_button = ui_button(SURFACE_MAIN, 'Continue Game', (160, 30), (title_x, title_y + (button_offset * 2)))
    options_button = ui_button(SURFACE_MAIN, 'Options', (160, 30), (title_x, title_y + (button_offset * 3)))
    quit_button = ui_button(SURFACE_MAIN, 'Quit Game', (160, 30), (title_x, title_y + (button_offset * 4)))

    # music
    pygame.mixer.music.load(ASSETS.background_music)
    pygame.mixer.music.play(-1)

    while menu_running:
        mouse_pos = pygame.mouse.get_pos()
        list_events = pygame.event.get()

        game_input = (list_events, mouse_pos)

        if menu_build:
            SURFACE_MAIN.blit(ASSETS.MAIN_MENU_BG, (0, 0))
            draw_text(SURFACE_MAIN, title_text, constants.FONT_TITLE, (title_x, title_y),
                      constants.COLOR_BLACK, back_color=constants.COLOR_WHITE, center=True)
            menu_build = False

        for event in list_events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # button updates
        if continue_button.update(game_input):
            pygame.mixer.music.stop()
            try:
                game_load()
            except:
                game_new()

            game_main_loop()
            menu_build = True

        if start_button.update(game_input):
            pygame.mixer.music.stop()
            game_new()
            game_main_loop()
            menu_build = True

        if options_button.update(game_input):
            menu_options()
            menu_build = True

        if quit_button.update(game_input):
            pygame.mixer.music.stop()
            game_exit()

        continue_button.draw()
        start_button.draw()
        options_button.draw()
        quit_button.draw()

        # update surface
        pygame.display.update()


def menu_options():
    option_menu_width = 200
    option_menu_height = 200

    option_menu_center = (constants.CAMERA_WIDTH / 2, constants.CAMERA_HEIGHT / 2)

    option_menu_surface = pygame.Surface((option_menu_width, option_menu_height))
    option_menu_rect = pygame.Rect(0, 0, option_menu_width, option_menu_height)
    option_menu_rect.center = option_menu_center

    # sliders
    slider_x = constants.CAMERA_WIDTH / 2
    slider_y = constants.CAMERA_HEIGHT / 2 - 50

    menu_close = False
    option_menu_surface.fill(constants.COLOR_GREY)
    SURFACE_MAIN.blit(option_menu_surface, option_menu_rect.topleft)

    # Menu Header
    draw_text(SURFACE_MAIN, "OPTIONS", constants.FONT_DEBUG, (slider_x, slider_y - 30),
              constants.COLOR_WHITE, center=True)

    sound_effect_slider = ui_slider(SURFACE_MAIN, (175, 10), (slider_x, slider_y + 20),
                                    constants.COLOR_BLACK, constants.COLOR_WHITE, PREF.vol_sound)

    music_effect_slider = ui_slider(SURFACE_MAIN, (175, 10), (slider_x, slider_y + 70),
                                    constants.COLOR_BLACK, constants.COLOR_WHITE, PREF.vol_music)

    # Slider Text
    draw_text(SURFACE_MAIN, "Sounds Volume", constants.FONT_MESSAGE, (slider_x, slider_y),
              constants.COLOR_WHITE, center=True)
    draw_text(SURFACE_MAIN, "Music Volume", constants.FONT_MESSAGE, (slider_x, slider_y + 50),
              constants.COLOR_WHITE, center=True)

    # Save Button
    save_button = ui_button(SURFACE_MAIN, 'Save', (160, 30), (slider_x, slider_y + 120))

    while not menu_close:
        mouse_pos = pygame.mouse.get_pos()
        list_events = pygame.event.get()
        game_input = (list_events, mouse_pos)

        for event in list_events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                menu_close = True

        if PREF.vol_sound is not sound_effect_slider.value:
            PREF.vol_sound = sound_effect_slider.value
            ASSETS.sound_adjust()

        if PREF.vol_music is not music_effect_slider.value:
            PREF.vol_music = music_effect_slider.value
            ASSETS.sound_adjust()

        sound_effect_slider.update(game_input)
        music_effect_slider.update(game_input)

        if save_button.update(game_input):
            pref_save()
            menu_close = True

        sound_effect_slider.draw()
        music_effect_slider.draw()
        save_button.draw()
        pygame.display.update()


def menu_pause():
    menu_close = False

    menu_text = "PAUSED"
    menu_font = constants.FONT_DEBUG

    text_height = helper_text_height(menu_font)
    text_width = helper_text_width(menu_font, menu_text)

    menu_x, menu_y = screen_mid_offset(text_width, text_height)

    while not menu_close:
        event_list = pygame.event.get()

        for event in event_list:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                menu_close = True

        draw_text(SURFACE_MAIN, menu_text, menu_font, (menu_x, menu_y), constants.COLOR_WHITE,
                  back_color=constants.COLOR_BLACK)
        pygame.display.flip()

        # Tick the clock. Stop speed animation on unpause
        CLOCK.tick(constants.MAX_FPS)

    return


def menu_inventory():
    """ Creates a Inventory list centered to the screen """

    menu_close = False

    menu_width = 200
    menu_height = 200

    menu_text_font = constants.FONT_MESSAGE
    menu_text_color = constants.COLOR_WHITE
    menu_text_height = helper_text_height(menu_text_font)

    menu_x, menu_y = screen_mid_offset(menu_width, menu_height)

    inventory_menu = pygame.Surface((menu_width, menu_height))

    while not menu_close:
        inventory_menu.fill(constants.COLOR_BLACK)

        # Inventory List
        inv_list = [obj.display_name for obj in PLAYER.container.inventory]

        event_list = pygame.event.get()

        # Mouse controls
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x_rel = mouse_x - menu_x
        mouse_y_rel = mouse_y - menu_y

        mouse_in_window = (0 < mouse_x_rel < menu_width and 0 < mouse_y_rel < menu_height)

        mouse_line_selection = int(mouse_y_rel / menu_text_height)

        for event in event_list:
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_i or event.key == pygame.K_ESCAPE):
                menu_close = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Left-click Use
                    if mouse_in_window and mouse_line_selection <= len(inv_list) - 1:
                        PLAYER.container.inventory[mouse_line_selection].item.use()
                        menu_close = True
                if event.button == 3:
                    # Right-click Drop
                    if mouse_in_window and mouse_line_selection <= len(inv_list) - 1:
                        PLAYER.container.inventory[mouse_line_selection].item.drop(PLAYER.x, PLAYER.y)
                        menu_close = True

        for line, (name) in enumerate(inv_list):
            if line == mouse_line_selection and mouse_in_window:
                # TODO I'm sure this could be done better ( rect.collidepoint - as per youtube Part 20)
                # TODO add more than just the name to the inv list
                draw_text(inventory_menu,
                          name,
                          menu_text_font,
                          (0, 0 + (line * menu_text_height)),
                          menu_text_color, constants.COLOR_GREY)
            else:
                draw_text(inventory_menu,
                          name,
                          menu_text_font,
                          (0, 0 + (line * menu_text_height)),
                          menu_text_color)

        SURFACE_MAIN.blit(inventory_menu, (menu_x, menu_y))
        pygame.display.flip()
        CLOCK.tick(constants.MAX_FPS)


def menu_tile_select(start_origin=None, tile_range=None, wall_blocking=True, enemy_blocking=False, radius=None):
    """ This menu allows the player to select a tile.
    """
    # TODO range does not measure diag cost of 1.41
    menu_close = False

    while not menu_close:
        event_list = pygame.event.get()
        mouse_x, mouse_y = pygame.mouse.get_pos()

        mapx_pix, mapy_pix = CAMERA.win_to_map((mouse_x, mouse_y))

        map_pos_x = int(mapx_pix / constants.CELL_WIDTH)
        map_pos_y = int(mapy_pix / constants.CELL_HEIGHT)

        valid_path = []

        if start_origin:
            full_list_of_cells = map_find_line(start_origin, (map_pos_x, map_pos_y))
            for i, (x, y) in enumerate(full_list_of_cells):
                valid_path.append((x, y))
                if tile_range and len(valid_path) >= tile_range:
                    break
                if not wall_blocking and GAME.current_map[x][y].block_path:
                    break
                if enemy_blocking and map_check_for_creatures(x, y):
                    break
        else:
            valid_path = [(map_pos_x, map_pos_y)]

        # get mouse_clicks
        for event in event_list:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                menu_close = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    return valid_path[-1]

        SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)
        SURFACE_MAP.fill(constants.COLOR_BLACK)

        CAMERA.update()
        draw_game()

        # draw_rec at mouse_pos
        for tile_x, tile_y in valid_path:
            if (tile_x, tile_y) == valid_path[-1]:
                draw_tile_rect((tile_x * constants.CELL_WIDTH, tile_y * constants.CELL_HEIGHT), marker='X')
            else:
                draw_tile_rect((tile_x * constants.CELL_WIDTH, tile_y * constants.CELL_HEIGHT))
        if radius:
            tile_area = map_find_radius(valid_path[-1], radius)
            for (tile_x, tile_y) in tile_area:
                draw_tile_rect((tile_x * constants.CELL_WIDTH, tile_y * constants.CELL_HEIGHT), marker="X")

        SURFACE_MAIN.blit(SURFACE_MAP, (0, 0), CAMERA.rectangle)

        draw_debug()
        draw_message()

        pygame.display.flip()
        CLOCK.tick(constants.MAX_FPS)

    return None


#
# GENERATORS
#

def gen_item(coords: PosXY) -> None:
    ran_num = random.randint(1, 5)
    if ran_num == 1:
        new_item = gen_scroll_ligthning(coords)
    elif ran_num == 2:
        new_item = gen_scroll_fireball(coords)
    elif ran_num == 3:
        new_item = gen_scroll_confusion(coords)
    elif ran_num == 4:
        new_item = gen_weapon_sword(coords)
    elif ran_num == 5:
        new_item = gen_armour_shield(coords)

    GAME.current_obj.append(new_item)


def gen_scroll_ligthning(coords: PosXY):
    x, y = coords
    item_use_dam = random.randint(5, 7)
    item_use_range = random.randint(5, 8)
    scroll_item = com_Item(use_function=cast_lightning, value=(item_use_dam, item_use_range))
    scroll = obj_Actor(x, y, "Lightning Scroll", "S_SCROLL_01", depth=constants.DEPTH_ITEM, item=scroll_item)

    return scroll


def gen_scroll_fireball(coords: PosXY):
    x, y = coords
    item_use_dam = random.randint(3, 5)
    item_use_range = random.randint(6, 9)
    item_use_radius = random.randint(1, 3)
    scroll_item = com_Item(use_function=cast_fireball, value=(item_use_dam, item_use_range, item_use_radius))
    scroll = obj_Actor(x, y, "Fireball Scroll", "S_SCROLL_02", depth=constants.DEPTH_ITEM, item=scroll_item)

    return scroll


def gen_scroll_confusion(coords: PosXY):
    x, y = coords
    item_use_range = random.randint(5, 7)
    item_use_turns = random.randint(3, 5)
    scroll_item = com_Item(use_function=cast_confusion, value=(item_use_turns, item_use_range))
    scroll = obj_Actor(x, y, "Confusion Scroll", animation_key="S_SCROLL_03", depth=constants.DEPTH_ITEM,
                       item=scroll_item)

    return scroll


def gen_weapon_sword(coords: PosXY):
    x, y = coords
    bonus = random.randint(1, 2)
    equipment_com = com_Equipment(attack_bonus=bonus, slot="MAIN")
    weapon = obj_Actor(x, y, "Sword", animation_key="S_SWORD", depth=constants.DEPTH_ITEM, equipment=equipment_com)

    return weapon


def gen_armour_shield(coords: PosXY):
    x, y = coords
    bonus = random.randint(1, 2)
    equipment_com = com_Equipment(defense_bonus=bonus, slot="OFFHAND")
    weapon = obj_Actor(x, y, "Shield", animation_key="S_SHIELD", depth=constants.DEPTH_ITEM, equipment=equipment_com)

    return weapon


def gen_snake_anaconda(coords: PosXY):
    x, y = coords
    max_health = random.randint(5, 10)
    max_attack = random.randint(1, 2)
    creature_com = com_Creature("Anaconda", death_function=death_snake, max_hp=max_health, base_atk=max_attack)
    ai_com = ai_Chase()
    snake = obj_Actor(x, y, "Snake", "A_SNAKE_01", depth=constants.DEPTH_CREATURE, creature=creature_com, ai=ai_com)

    return snake


def gen_snake_cobra(coords: PosXY):
    x, y = coords
    max_health = random.randint(15, 20)
    max_attack = random.randint(3, 6)
    creature_com = com_Creature("Cobra", death_function=death_snake, max_hp=max_health, base_atk=max_attack)
    ai_com = ai_Chase()
    snake = obj_Actor(x, y, "Snake", "A_SNAKE_03", depth=constants.DEPTH_CREATURE, creature=creature_com, ai=ai_com)

    return snake


def gen_enemy(coords: PosXY):
    x, y = coords
    ran_num = random.randint(1, 100)
    if ran_num <= 15:
        new_snake = gen_snake_cobra((x, y))
    elif ran_num <= 65:
        new_snake = gen_snake_anaconda((x, y))
    else:
        new_snake = gen_mouse((x, y))

    GAME.current_obj.append(new_snake)


def gen_mouse(coords: PosXY):
    x, y = coords
    max_health = random.randint(1, 5)
    max_attack = random.randint(1, 1)
    creature_com = com_Creature("Mouse", death_function=death_mouse, max_hp=max_health, base_atk=max_attack)
    ai_com = ai_Flee()
    item_com = com_Item(use_function=cast_heal, value=2)
    mouse = obj_Actor(x, y, "mouse", "A_MOUSE", depth=constants.DEPTH_CREATURE, item=item_com,
                      creature=creature_com, ai=ai_com)

    return mouse


def gen_player(coords: PosXY):
    global PLAYER
    x, y = coords
    container_com = com_Container()
    creature_com = com_Creature("Player", base_atk=4, max_hp=20, death_function=death_player)
    PLAYER = obj_Actor(x, y, "Python", animation_key="A_PLAYER", depth=constants.DEPTH_PLAYER, creature=creature_com,
                       container=container_com)

    GAME.current_obj.append(PLAYER)


def gen_Stairs(coords: PosXY, downwards):
    x, y = coords
    stairs_com = com_Stairs(downwards)

    if downwards:
        stairs = obj_Actor(x, y, "Stairs", depth=constants.DEPTH_BKGD, animation_key="S_STAIRS_DOWN", stairs=stairs_com)
    else:
        stairs = obj_Actor(x, y, "Stairs", depth=constants.DEPTH_BKGD, animation_key="S_STAIRS_UP", stairs=stairs_com)

    GAME.current_obj.append(stairs)


def gen_Portal(coords: PosXY, key: str):
    x, y = coords
    portal_com = com_Portal(key)
    portal = obj_Actor(x, y, "Exit Portal", depth=constants.DEPTH_BKGD, animation_key="S_PORTAL_CLOSED",
                       portal=portal_com)

    GAME.current_obj.append(portal)


def gen_magic_lamp(coords: PosXY, key: str):
    x, y = coords
    lamp_item = com_Item(use_function=cast_key, value=key)
    lamp = obj_Actor(x, y, "Magic Lamp", animation_key="S_LAMP", depth=constants.DEPTH_ITEM, item=lamp_item)

    GAME.current_obj.append(lamp)


#
# MAIN GAME LOOP
#

def game_main_loop():
    global FOV_CALCULATE

    FOV_CALCULATE = True
    game_quit = False
    player_action = 'no-action'

    while not game_quit:
        player_action = game_handle_keys()
        if player_action == 'player-move':
            # recal FOV on player move
            FOV_CALCULATE = True

        map_calculate_fov()

        if player_action == 'QUIT':
            game_save()
            menu_main()

        if PLAYER.state == "STATUS_DEAD" or PLAYER.state == "STATUS_WIN":
            game_quit = True

        for obj in GAME.current_obj:
            if obj.ai:
                if player_action != 'no-action':
                    obj.ai.take_turn()
            if obj.portal:
                obj.portal.update()

        # draw the game
        draw_game()

        CLOCK.tick(constants.MAX_FPS)


def game_message(msg, msg_color=constants.COLOR_WHITE):
    GAME.message_log.append((msg, msg_color))


def game_handle_keys():
    event_list = pygame.event.get()
    key_list = pygame.key.get_pressed()

    MOD_KEY = key_list[pygame.K_RSHIFT] or key_list[pygame.K_LSHIFT]

    for event in event_list:
        if event.type == pygame.QUIT:
            return "QUIT"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_KP8:
                PLAYER.creature.move(0, -1)
                return "player-move"
            if event.key == pygame.K_DOWN or event.key == pygame.K_KP2:
                PLAYER.creature.move(0, 1)
                return "player-move"
            if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                PLAYER.creature.move(-1, 0)
                return "player-move"
            if event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                PLAYER.creature.move(1, 0)
                return "player-move"
            if event.key == pygame.K_KP7:
                PLAYER.creature.move(-1, -1)
                return "player-move"
            if event.key == pygame.K_KP9:
                PLAYER.creature.move(1, -1)
                return "player-move"
            if event.key == pygame.K_KP1:
                PLAYER.creature.move(-1, 1)
                return "player-move"
            if event.key == pygame.K_KP3:
                PLAYER.creature.move(1, 1)
                return "player-move"
            if event.key == pygame.K_g:
                objects = map_obj_at_loc(PLAYER.x, PLAYER.y)
                for obj in objects:
                    if obj.item:
                        obj.item.pickup(PLAYER)
            if event.key == pygame.K_p:
                menu_pause()

            if event.key == pygame.K_i:
                menu_inventory()

            if event.key == pygame.K_COMMA and MOD_KEY:
                objects = map_obj_at_loc(PLAYER.x, PLAYER.y)
                for obj in objects:
                    if obj.stairs:
                        obj.stairs.use()

            if event.key == pygame.K_l:
                menu_tile_select()

            if event.key == pygame.K_d:
                if len(PLAYER.container.inventory) > 0:
                    PLAYER.container.inventory[-1].item.drop(PLAYER.x, PLAYER.y)

    return "no-action"


def game_init():
    """Setup the main window and pygame"""

    global SURFACE_MAIN, SURFACE_MAP, CLOCK, FOV_CALCULATE, ASSETS, CAMERA, PREF
    # startup pygame
    pygame.init()

    # Repeating the key input
    pygame.key.set_repeat(200, 50)

    try:
        pref_load()
    except:
        PREF = str_Preferences()

    # Create the Main Image Surface
    SURFACE_MAIN = pygame.display.set_mode((constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))

    SURFACE_MAP = pygame.Surface((constants.MAP_WIDTH * constants.CELL_WIDTH,
                                  constants.MAP_HEIGHT * constants.CELL_HEIGHT))

    ASSETS = obj_Assets()
    CAMERA = obj_Camera()

    CLOCK = pygame.time.Clock()

    FOV_CALCULATE = True


def game_new():
    global GAME

    GAME = obj_Game()
    gen_player((0, 0))
    map_place_objects(GAME.current_rooms)


def game_load():
    global GAME, PLAYER

    with gzip.open('data/savegame', 'rb') as file:
        GAME, PLAYER = pickle.load(file)

    map_make_fov(GAME.current_map)


def game_save():
    with gzip.open('data/savegame', 'wb') as file:
        pickle.dump([GAME, PLAYER], file)


def pref_load():
    global PREF

    with gzip.open('data/pref', 'rb') as file:
        PREF = pickle.load(file)


def pref_save():
    with gzip.open('data/pref', 'wb') as file:
        pickle.dump(PREF, file)


def files_delete(file):
    save_found = os.path.isfile(file)
    if save_found: os.remove(file)


def game_exit():
    pygame.quit()
    exit()


if __name__ == '__main__':
    menu_main()
