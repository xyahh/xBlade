from Characters.char_class import Character
from Maps.map_class import Map
from pico2d import *


class BoundingBox:
    LEFT = TOP = RIGHT = BOTTOM = None

    def __init__(self, char, map : object):
        global LEFT, TOP, RIGHT, BOTTOM
        LEFT, TOP, RIGHT, BOTTOM = range(4)
        self.char = char
        self.map = map
        self.map_box = []
        self.char_box = []

    def update_map_box(self):
        self.map_box.clear()
        objects = self.map.map['objects']
        for i in range(len(objects)):
            obj = objects[i]
            if obj['has_bbox']:
                self.map_box.append((obj['pos_x'] + obj['bounding_box'][LEFT],
                                obj['pos_y'] + obj['bounding_box'][TOP],
                                obj['pos_x'] + obj['bounding_box'][RIGHT],
                                obj['pos_y'] + obj['bounding_box'][BOTTOM]))

    def update_char_box(self):
        self.char_box.clear()
        for i in range(len(self.char)):
            ch = self.char[i]
            bx = ch.bounding_box[ch.action]
            self.char_box.append((ch.x + bx[LEFT],
                   ch.y + bx[TOP],
                   ch.x + bx[RIGHT],
                   ch.y + bx[BOTTOM]))

    def update(self):
        self.update_map_box()
        self.update_char_box()

    def draw(self):
        for i in range(len(self.map_box)):
            draw_rectangle(self.map_box[i][LEFT],
                           self.map_box[i][TOP],
                           self.map_box[i][RIGHT],
                           self.map_box[i][BOTTOM])

        for i in range(len(self.char_box)):
            draw_rectangle(self.char_box[i][LEFT],
                           self.char_box[i][TOP],
                           self.char_box[i][RIGHT],
                           self.char_box[i][BOTTOM])
