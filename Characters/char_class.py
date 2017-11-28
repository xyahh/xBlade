from pico2d import *
from General.bounding_box import BoundingBox
from Logo import logo
file_name = "CharacterClass"


def clamp(minimum, value, maximum):
    return max(minimum, min(value, maximum))

class Character:
    # CONSTANTS
    PIXEL_PER_METER, GRAVITY_M2PS, GRAVITY_P2PS = None, None, None
    RUN_SPEED_KMPH, RUN_SPEED_MPS, RUN_SPEED_PPS = None, None, None
    JUMP_SPEED_KMPH, JUMP_SPEED_MPS, JUMP_SPEED_PPS = None, None, None
    TIME_PER_ACTION, ACTION_PER_TIME = None, None

    STAND_R, STAND_L, RUN_R = None, None, None
    RUN_L, JUMP_R, JUMP_L = None, None, None

    CHAR_SCALE = None
    # END CONSTANTS

    def init_const(self):
        # all constants named global
        global PIXEL_PER_METER, GRAVITY_M2PS, GRAVITY_P2PS, RUN_SPEED_KMPH, RUN_SPEED_MPS, RUN_SPEED_PPS
        global JUMP_SPEED_KMPH, JUMP_SPEED_MPS, JUMP_SPEED_PPS, TIME_PER_ACTION, ACTION_PER_TIME
        global STAND_R, STAND_L, RUN_R, RUN_L, JUMP_R, JUMP_L, MOVE, ATTACK1, CHAR_SCALE

        constants_file = open('Characters/constants.txt', 'r')
        constants = json.load(constants_file)
        constants_file.close()

        PIXEL_PER_METER = constants['Physics']['PIXEL_PER_METER']

        RUN_SPEED_KMPH = constants['Physics']['RUN_SPEED_KMPH']
        RUN_SPEED_MPS = RUN_SPEED_KMPH * 1000.0 / 3600.0  # convert km/h to m/s
        RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

        GRAVITY_M2PS = constants['Physics']['GRAVITY_M2PS']
        GRAVITY_P2PS = GRAVITY_M2PS * PIXEL_PER_METER * PIXEL_PER_METER

        JUMP_SPEED_KMPH = constants['Physics']['JUMP_SPEED_KMPH']
        JUMP_SPEED_MPS = JUMP_SPEED_KMPH * 1000.0 / 3600.0
        JUMP_SPEED_PPS = JUMP_SPEED_MPS * PIXEL_PER_METER

        TIME_PER_ACTION = constants['Events']['TIME_PER_ACTION']
        ACTION_PER_TIME = 1 / TIME_PER_ACTION

        STAND_R = constants['States']['STAND_R']
        STAND_L = constants['States']['STAND_L']
        RUN_R = constants['States']['RUN_R']
        RUN_L = constants['States']['RUN_L']
        JUMP_R = constants['States']['JUMP_R']
        JUMP_L = constants['States']['JUMP_L']

        MOVE = constants['Actions']['MOVE']
        ATTACK1 = constants['Actions']['ATTACK1']

        CHAR_SCALE = constants['Char_Scale']

    def init_vars(self, player_id, spawn_x, spawn_y, spawn_state, spawn_action):
        self.jump_key_down = self.left_key_down = self.right_key_down = False
        self.frame = self.total_frames = self.last_key = self.accel = 0
        self.last_x, self.last_y = (spawn_x, spawn_y)
        self.curr_time = self.start_time = 0
        self.x, self.y = (spawn_x, spawn_y)
        self.action = spawn_action
        self.player_id = player_id
        self.state = spawn_state

    def init_chars(self, char_name):
        self.char = {}
        self.sprite = {}
        chars_file = open('Characters/characters.txt', 'r')
        char_info = json.load(chars_file)
        chars_file.close()

        for name in char_info:
            if name == char_name:
                sprite_file = open(char_info[name]['sprite'], 'r')
                sprite_info = json.load(sprite_file)
                sprite_file.close()
                for action in sprite_info:
                    self.sprite[action] = {"img": load_image(sprite_info[action]['path']),
                                           "SFrames": sprite_info[action]['SFrames'],
                                           "RFrames": sprite_info[action]['RFrames'],
                                           "JFrames": sprite_info[action]['JFrames'],
                                           "w": sprite_info[action]['w'],
                                           "h": sprite_info[action]['h']}
                self.char = {"name": name, "sprite": self.sprite,
                             "bounding_boxes": char_info[name]['bounding_boxes'],
                             "hp": {"bar":load_image(char_info[name]['hp']['bar']),
                                    "red": load_image(char_info[name]['hp']['red']),
                                    "dx": char_info[name]['hp']['dx'],
                                    "dy": char_info[name]['hp']['dy']}}
                self.max_hp = self.hp = char_info[name]['hp']['hp']

    def init_font(self):
        font_path = open('General/font.txt', 'r')
        font_info = json.load(font_path)
        font_path.close()
        self.font = load_font(font_info['font']['path'], font_info['font']['size'])
        self.player_colors = {}
        for id in font_info['player_colors']:
            self.player_colors[int(id)] = (font_info['player_colors'][id]['R'],
                                      font_info['player_colors'][id]['G'],
                                      font_info['player_colors'][id]['B'])

    def init_bounding_boxes(self):
        self.bounding_box = {}

        bboxes_file = open(self.char['bounding_boxes'], 'r')
        bboxes_info = json.load(bboxes_file)
        bboxes_file.close()

        for action in bboxes_info:
            self.bounding_box[action] = (bboxes_info[action]['left'],
                                  bboxes_info[action]['top'],
                                  bboxes_info[action]['right'],
                                  bboxes_info[action]['bottom'])

    def __init__(self, char_name, player_id: int, spawn_x: int, spawn_y: int, spawn_state: int, spawn_action):
        self.init_const()
        self.init_vars(player_id, spawn_x, spawn_y, spawn_state, spawn_action)
        self.init_chars(char_name)
        self.init_font()
        self.init_bounding_boxes()

    def draw(self):
        h = self.char['sprite'][self.action]['h']
        w = self.char['sprite'][self.action]['w']
        self.char['sprite'][self.action]['img'].clip_draw(self.frame * w, self.state * h,
                                                          w, h, self.x, self.y, w * CHAR_SCALE,
                                                          h * CHAR_SCALE)
        x = self.char['hp']['dx'] + self.x
        y = self.char['hp']['dy'] + self.y
        self.char['hp']['bar'].draw(x, y)
        h_ = self.char['hp']['bar'].h
        w_ = self.char['hp']['bar'].w
        dw = w_*(self.hp / self.max_hp)
        self.char['hp']['red'].draw(x, y, dw, h_)
        self.font.draw(x-w_, y+h_, str(self.player_id),
                       color=self.player_colors[self.player_id])

    def update(self, frame_time, boxes):
        self.update_frames(frame_time)
        self.move(frame_time,boxes)
        self.update_state()

    def update_frames(self, frame_time):
        state_frames = None
        if self.state in (STAND_R, STAND_L):
            state_frames = 'SFrames'
        elif self.state in (RUN_R, RUN_L):
            state_frames = 'RFrames'
        elif self.state in (JUMP_R, JUMP_L):
            state_frames = 'JFrames'
        self.total_frames += self.char['sprite'][self.action][state_frames] * ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % self.char['sprite'][self.action][state_frames]

    def move(self, frame_time, boxes):
        self.curr_time += frame_time
        dt = self.curr_time - self.start_time
        self.y = self.last_y - GRAVITY_P2PS * dt*dt # there's always a force!

        if self.jump_key_down:
            self.y += JUMP_SPEED_PPS * dt # only had initial speed if it has jumped
            self.accel = JUMP_SPEED_PPS - 2*GRAVITY_P2PS*dt # derivative of speed*t - at^2

        sd = BoundingBox
        for i in range(len(boxes.map_box)):
            # check if it collides and if it is NOT on the first part of a jump (when going up)
            if sd.collide(sd, boxes.char_box[self.player_id-1], boxes.map_box[i]) and self.accel <= 0:
               if self.y +self.bounding_box[self.action][sd.BOTTOM] >= boxes.map_box[i][sd.BOTTOM]\
                       and self.y >= boxes.map_box[i][sd.TOP]: # check if the center is above the platform level and feet are above the lower level
                self.y = boxes.map_box[i][sd.TOP] - self.bounding_box[self.action][sd.BOTTOM] # update based on feet
                self.start_time = self.curr_time # update the starting time for the next jump / fall
                self.last_y = self.y # update position for the next jump / fall
                self.x += boxes.map.map['objects'][boxes.map_object_id[i]]['dir_x']*frame_time # update direction
                self.accel = 0
                self.jump_key_down = False
               break


        distance = RUN_SPEED_PPS * frame_time
        if self.left_key_down and not self.right_key_down or self.last_key == RUN_L:
            self.x -= distance

        if self.right_key_down and not self.left_key_down or self.last_key == RUN_R:
            self.x += distance

        self.x = clamp(0, self.x, logo.win_width)

    def get_name(self):
        return self.char['name']

    def handle_moves(self, frame_time, event, left_key, right_key, jump_key, down_key):
        if event.key == left_key:
            self.left_key_down = event.type == SDL_KEYDOWN
            if self.left_key_down: self.last_key = RUN_L
            else: self.last_key = STAND_L
        if event.key == right_key:
            self.right_key_down = event.type == SDL_KEYDOWN
            if self.right_key_down: self.last_key = RUN_R
            else: self.last_key = STAND_R
        if event.key == jump_key and event.type == SDL_KEYDOWN and not self.jump_key_down:
            self.start_time = self.curr_time =  self.total_frames = 0
            self.jump_key_down = True
            self.last_y = self.y

    def update_state(self):
        if self.jump_key_down:
            if self.state in (RUN_L, STAND_L) or (self.left_key_down and not self.right_key_down):
                self.state = JUMP_L
            elif self.state in (RUN_R, STAND_R) or (self.right_key_down and not self.left_key_down):
                self.state = JUMP_R
        else:
            if self.left_key_down and not self.right_key_down:
                self.state = RUN_L
            elif self.right_key_down and not self.left_key_down:
                self.state = RUN_R
            elif self.right_key_down and self.left_key_down:
                self.state = self.last_key
            else:
                if self.state in (RUN_L, STAND_L, JUMP_L):
                    self.state = STAND_L
                elif self.state in (RUN_R, STAND_R, JUMP_R):
                    self.state = STAND_R

    def handle_events(self, frame_time, event, player_id, left_key, right_key, jump_key, down_key):
        if player_id == self.player_id:
            self.handle_moves(frame_time, event, left_key, right_key, jump_key, down_key)


class CharacterSelect:

    def init_chars(self):
        self.chars = []
        chars_file = open('Characters/characters.txt', 'r')
        char_info = json.load(chars_file)
        chars_file.close()
        for name in char_info:
            self.chars .append({"name": name, "img": load_image(char_info[name]['img'])})

    def init_selection_format(self):
        selection_file = open('Characters/selection_format.txt', 'r')
        selection_info = json.load(selection_file)
        selection_file.close()

        self.chars_per_row = selection_info['chars_per_row']
        self.col_dist_diff = selection_info['col_dist_diff']
        self.row_dist_diff = selection_info['row_dist_diff']
        self.start_x = selection_info['start_x']
        self.start_y = selection_info['start_y']

    def init_players(self, player_num):
        self.player_choice = []
        if len(self.player_choice) > 0: del self.player_choice
        for i in range(player_num):
            self.player_choice.append(0)

    def __init__(self, player_num):
        self.init_chars()
        self.init_selection_format()
        self.init_players(player_num)

    def size(self):
        return len(self.chars)

    def draw(self):
        for i in range(self.size()):
            self.chars[i]['img'].draw(self.start_x+(i%self.chars_per_row)*self.col_dist_diff,
                                        self.start_y+int(i/self.chars_per_row)*self.row_dist_diff)

    def handle_events(self, frame_time, event, player_id, left_key, right_key, up_key, down_key):
        if player_id <= len(self.player_choice):
            i = player_id - 1
            if event.key == left_key:
                if self.player_choice[i] > 0:
                    self.player_choice[i] -= 1
            if event.key == right_key:
                if self.player_choice[i] < self.size() - 1:
                    self.player_choice[i] += 1
            if event.key == down_key:
                if self.player_choice[i] < self.size() - self.chars_per_row:
                    self.player_choice[i] += self.chars_per_row
            if event.key == up_key:
                if self.player_choice[i] > self.chars_per_row - 1:
                    self.player_choice[i] -= self.chars_per_row
