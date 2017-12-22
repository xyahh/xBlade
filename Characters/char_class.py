from pico2d import *
from General.bounding_box import BoundingBox
from Sound import sound_manager as sound
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
    LIVES_PER_CHAR = None
    DEPTH_SIZE = None
    STATES = {}
    ACTIONS = {}
    CHAR_SCALE = None
    # END CONSTANTS

    heart = None

    @staticmethod
    def init_const():
        # all constants named global
        global PIXEL_PER_METER, GRAVITY_M2PS, GRAVITY_P2PS, RUN_SPEED_KMPH, RUN_SPEED_MPS, RUN_SPEED_PPS
        global JUMP_SPEED_KMPH, JUMP_SPEED_MPS, JUMP_SPEED_PPS, TIME_PER_ACTION, ACTION_PER_TIME
        global CHAR_SCALE, STATES, ACTIONS, LIVES_PER_CHAR, DEPTH_SIZE

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

        DEPTH_SIZE = constants['Physics']['DEPTH_SIZE']

        TIME_PER_ACTION = constants['Events']['TIME_PER_ACTION']
        ACTION_PER_TIME = 1 / TIME_PER_ACTION

        STATES = {}
        for i in constants['States']:
            STATES.update({i: constants['States'][i], constants['States'][i]: constants['StateMap'][i]})

        ACTIONS = {}
        for i in constants['Actions']:
            ACTIONS.update({i: constants['Actions'][i]['name'],
                            constants['Actions'][i]['name']: {'is_attack': constants['Actions'][i]['is_attack']}
                            })

        CHAR_SCALE = constants['Char_Scale']
        LIVES_PER_CHAR = constants['Char_Lives']

    def init_vars(self, player_id, spawn_x, spawn_y, spawn_state, spawn_action):
        self.jump_key_down = self.left_key_down = self.right_key_down = False
        self.frame = self.total_frames = self.last_key = self.accel = 0
        self.last_x, self.last_y = (spawn_x, spawn_y)
        self.spawn_x, self.spawn_y = (spawn_x, spawn_y)
        self.x, self.y = (spawn_x, spawn_y)
        self.curr_time = self.start_time = 0
        self.i_hit, self.im_hit, self.extra_jump = False, False, False
        self.action = spawn_action
        self.player_id = player_id
        self.lives = LIVES_PER_CHAR
        self.state = STATES[spawn_state]

    def init_chars(self, char_name):
        sprite = {}
        chars_file = open('Characters/characters.txt', 'r')
        char_info = json.load(chars_file)
        chars_file.close()

        for name in char_info:
            if name == char_name:
                sprite_file = open(char_info[name]['sprite'], 'r')
                sprite_info = json.load(sprite_file)
                sprite_file.close()
                for action in sprite_info:
                    sprite[action] = sprite_info[action]
                    sprite[action].update({"img": load_image(sprite[action]['path'])})

                self.char = char_info[name]
                self.char.update({"name": name, "sprite": sprite})
                self.char['hp'].update({"bar": load_image(self.char['hp']['bar']),
                                        "red": load_image(self.char['hp']['red'])})
                self.max_hp = self.hp = self.char['hp']['hp']

    def init_other_media(self):
        font_path = open('General/font.txt', 'r')
        font_info = json.load(font_path)
        font_path.close()
        self.font = load_font(font_info['font']['path'], font_info['font']['size'])
        self.player_colors = {}
        for id in font_info['player_colors']:
            self.player_colors[int(id)] = (font_info['player_colors'][id]['R'],
                                           font_info['player_colors'][id]['G'],
                                           font_info['player_colors'][id]['B'])

        media_path = open('Characters/media.txt', 'r')
        media_info = json.load(media_path)
        media_path.close()
        if Character.heart is None:
            Character.heart = media_info['heart']
            Character.heart.update({'img': load_image(Character.heart['img'])})

    def init_bounding_boxes(self):
        self.bounding_box = {}
        bboxes_file = open(self.char['bounding_boxes'], 'r')
        bboxes_info = json.load(bboxes_file)
        bboxes_file.close()

        for action in bboxes_info:
            bb_states = {}
            for state in bboxes_info[action]:
                bb_states.update({STATES[state]: (bboxes_info[action][state]['left'],
                                                  bboxes_info[action][state]['top'],
                                                  bboxes_info[action][state]['right'],
                                                  bboxes_info[action][state]['bottom'],
                                                  bboxes_info[action][state]['damage'],
                                                  bboxes_info[action][state]['heal'])})
            self.bounding_box.update({action: bb_states})

    def __init__(self, char_name, player_id: int, spawn_x: int, spawn_y: int, spawn_state: int, spawn_action):
        self.init_const()
        self.init_vars(player_id, spawn_x, spawn_y, spawn_state, spawn_action)
        self.init_chars(char_name)
        self.init_other_media()
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
        self.char['hp']['red'].draw(x-0.5*w_+0.5*dw, y, dw, h_)
        self.font.draw(x-w_, y+h_, str(self.player_id),
                       color=self.player_colors[self.player_id])
        heart = Character.heart
        for i in range(self.lives):
            heart['img'].draw(x-w_*0.5+i*heart['w']*2, y+h_+heart['h']*0.5, heart['w'], heart['h'])

    def check_hp(self):
        if self.hp < 0 or self.y < -self.char['sprite'][self.action]['h']*CHAR_SCALE-DEPTH_SIZE:
            if self.lives == 0:
                return True
            self.lives -= 1
            self.hp = self.max_hp
            self.x, self.y = (self.spawn_x, self.spawn_y)
            self.action = ACTIONS['MOVE']
            if self.im_hit:
                self.im_hit = False
            return False

    def update(self, frame_time, boxes):
        game_end = self.check_hp()
        self.update_frames(frame_time)
        self.update_attack(frame_time, boxes)
        self.move(frame_time, boxes)
        self.update_state()
        return game_end

    def update_attack(self, frame_time, boxes):
        if ACTIONS[self.action]['is_attack']:
            sd = BoundingBox
            for i in range(len(boxes.char_box)):
                is_there_collision = sd.collide(sd, boxes.char_box[self.player_id - 1], boxes.char_box[i])
                if is_there_collision and boxes.char_id[i] != self.player_id \
                        and not self.i_hit and not boxes.char[i].im_hit:
                            dmg = self.bounding_box[self.action][self.state][sd.DAMAGE]
                            if dmg > 0:
                                boxes.char[i].hp -= dmg
                                boxes.char[i].im_hit = True
                                boxes.char[i].action = ACTIONS['IM_HIT']
                                boxes.char[i].total_frames = 0.0
                            self.hp += self.bounding_box[self.action][self.state][sd.HEAL]
                            if self.hp > self.max_hp:
                                self.hp = self.max_hp
                            self.i_hit = True

    def update_frames(self, frame_time):
        state_frames = STATES[self.state]
        self.total_frames += self.char['sprite'][self.action][state_frames]['frames'] * ACTION_PER_TIME * \
                             frame_time * self.char['sprite'][self.action][state_frames]['action_time_ratio']
        self.frame = int(self.total_frames) % self.char['sprite'][self.action][state_frames]['frames']
        if self.action != ACTIONS['MOVE'] \
                and self.total_frames > self.char['sprite'][self.action][state_frames]['frames']\
                and not self.char['sprite'][self.action][state_frames]['loop']:
            self.action = ACTIONS['MOVE']
            if self.im_hit:
                self.im_hit = False

    def move(self, frame_time, boxes):
        self.curr_time += frame_time
        dt = self.curr_time - self.start_time

        temp_y = self.y

        self.y = self.last_y - GRAVITY_P2PS * dt*dt # there's always a force!

        if self.jump_key_down:
            self.y += JUMP_SPEED_PPS * dt # only had initial speed if it has jumped
            self.accel = JUMP_SPEED_PPS - 2*GRAVITY_P2PS*dt  # derivative of speed*t - at^2

        sd = BoundingBox

        for i in range(len(boxes.map_box)):
            is_there_collision = sd.collide(sd, boxes.char_box[self.player_id-1], boxes.map_box[i]) and self.accel <= 0
            is_above_level = self.y + self.bounding_box[self.action][self.state][sd.BOTTOM] >= \
                boxes.map_box[i][sd.BOTTOM] and self.y >= boxes.map_box[i][sd.TOP]
            time_delay_condition = boxes.map_box[i][sd.LEFT] <= self.x <= boxes.map_box[i][sd.RIGHT] and \
                                   self.y < boxes.map_box[i][sd.TOP] and temp_y >= boxes.map_box[i][sd.TOP]

            if (is_there_collision and is_above_level) or time_delay_condition:
                # update based on feet
                self.y = boxes.map_box[i][sd.TOP] - self.bounding_box[self.action][self.state][sd.BOTTOM]
                self.start_time = self.curr_time  # update the starting time for the next jump / fall
                self.last_y = self.y  # update position for the next jump / fall
                self.x += boxes.map.map['objects'][boxes.map_object_id[i]]['dir_x'] * frame_time  # update direction
                self.accel = 0
                self.jump_key_down, self.extra_jump = False, False
                break

        distance = RUN_SPEED_PPS * frame_time
        if self.left_key_down and not self.right_key_down or self.last_key == STATES['RUN_L']:
            self.x -= distance

        if self.right_key_down and not self.left_key_down or self.last_key == STATES['RUN_R']:
            self.x += distance

        self.x = clamp(0, self.x, logo.win_width)

    def get_name(self):
        return self.char['name']

    def process_action(self, ACTION_NAME):
        self.action = ACTIONS[ACTION_NAME]
        if self.char['sprite'][self.action]['has_sound']:
            sound.play(self.char['sprite'][self.action]['sound'])
        self.i_hit = False
        self.total_frames = 0.0
        if self.char['sprite'][self.action][STATES[self.state]]['extra_jump'] and not self.extra_jump:
            self.extra_jump, self.jump_key_down = True, True
            self.start_time = self.curr_time = 0.0
            self.last_y = self.y

    def handle_actions(self, frame_time, event, ability1_key, ability2_key):
        ability_list = (ACTIONS['ABILITY1'], ACTIONS['ABILITY2'])
        if event.key == ability1_key and event.type == SDL_KEYDOWN and self.action not in ability_list:
            self.process_action('ABILITY1')
        if event.key == ability2_key and event.type == SDL_KEYDOWN and self.action not in ability_list:
            self.process_action('ABILITY2')

    def handle_moves(self, frame_time, event, left_key, right_key, jump_key):
        if event.key == left_key:
            self.left_key_down = event.type == SDL_KEYDOWN and not self.im_hit
            if self.left_key_down:
                self.last_key = STATES['RUN_L']
            else:
                self.last_key = STATES['STAND_L']
        if event.key == right_key:
            self.right_key_down = event.type == SDL_KEYDOWN and not self.im_hit
            if self.right_key_down:
                self.last_key = STATES['RUN_R']
            else:
                self.last_key = STATES['STAND_R']
        if event.key == jump_key and event.type == SDL_KEYDOWN and not self.jump_key_down and not self.im_hit:
            self.start_time = self.curr_time =  self.total_frames = 0
            self.jump_key_down = True
            self.last_y = self.y

    def update_state(self):
        if self.jump_key_down:
            if self.state in (STATES['RUN_L'], STATES['STAND_L']) or (self.left_key_down and not self.right_key_down):
                self.state = STATES['JUMP_L']
            elif self.state in (STATES['RUN_R'], STATES['STAND_R']) or (self.right_key_down and not self.left_key_down):
                self.state = STATES['JUMP_R']
        else:
            if self.left_key_down and not self.right_key_down:
                self.state = STATES['RUN_L']
            elif self.right_key_down and not self.left_key_down:
                self.state = STATES['RUN_R']
            elif self.right_key_down and self.left_key_down:
                self.state = self.last_key
            else:
                if self.state in (STATES['RUN_L'], STATES['STAND_L'], STATES['JUMP_L']):
                    self.state = STATES['STAND_L']
                elif self.state in (STATES['RUN_R'], STATES['STAND_R'], STATES['JUMP_R']):
                    self.state = STATES['STAND_R']

    def handle_events(self, frame_time, event, player_id,
                      left_key, right_key, jump_key, down_key, ability1_key, ability2_key):
        if player_id == self.player_id:
            self.handle_moves(frame_time, event, left_key, right_key, jump_key)
            self.handle_actions(frame_time, event, ability1_key, ability2_key)


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
        self.__dict__.update(selection_info)

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
                    sound.play("change")
                    self.player_choice[i] -= 1
            if event.key == right_key:
                if self.player_choice[i] < self.size() - 1:
                    sound.play("change")
                    self.player_choice[i] += 1
            if event.key == down_key:
                if self.player_choice[i] < self.size() - self.chars_per_row:
                    sound.play("change")
                    self.player_choice[i] += self.chars_per_row
            if event.key == up_key:
                if self.player_choice[i] > self.chars_per_row - 1:
                    sound.play("change")
                    self.player_choice[i] -= self.chars_per_row
