from pico2d import *


class BoundingBox:
    LEFT, TOP, RIGHT, BOTTOM, DAMAGE = range(5)

    def __init__(self, char, map : object):
        global LEFT, TOP, RIGHT, BOTTOM, DAMAGE
        LEFT, TOP, RIGHT, BOTTOM, DAMAGE = range(5)
        self.char = char
        self.map = map
        self.map_object_id = []
        self.char_id = []
        self.map_box = []
        self.char_box = []

    def update_map_box(self):
        self.map_box.clear()
        self.map_object_id.clear()
        objects = self.map.map['objects']
        for i in range(len(objects)):
            obj = objects[i]
            if obj['has_bbox']:
                self.map_object_id.append(i)
                self.map_box.append((obj['pos_x'] + obj['bounding_box'][LEFT],
                                obj['pos_y'] + obj['bounding_box'][TOP],
                                obj['pos_x'] + obj['bounding_box'][RIGHT],
                                obj['pos_y'] + obj['bounding_box'][BOTTOM]))

    def update_char_box(self):
        self.char_box.clear()
        self.char_id.clear()
        for i in range(len(self.char)):
            ch = self.char[i]
            self.char_id.append(ch.player_id)
            bx = ch.bounding_box[ch.action][ch.state]
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

    def collide(self, a, b):
        left_a, bottom_a, right_a, top_a = a[LEFT], a[BOTTOM], a[RIGHT], a[TOP]
        left_b, bottom_b, right_b, top_b = b[LEFT], b[BOTTOM], b[RIGHT], b[TOP]
        if left_a > right_b: return False
        if right_a < left_b: return False
        if top_a < bottom_b: return False
        if bottom_a > top_b: return False
        return True
