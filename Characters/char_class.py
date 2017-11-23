from pico2d import *
file_name = "CharacterClass"


class Character:
    # CONSTANTS
    PIXEL_PER_METER, GRAVITY_M2PS, GRAVITY_P2PS = None, None, None
    RUN_SPEED_KMPH, RUN_SPEED_MPS, RUN_SPEED_PPS = None, None, None
    JUMP_SPEED_KMPH, JUMP_SPEED_MPS, JUMP_SPEED_PPS = None, None, None
    TIME_PER_ACTION, ACTION_PER_TIME = None, None

    STAND_R, STAND_L, RUN_R = None, None, None
    RUN_L, JUMP_R, JUMP_L = None, None, None

    MOVE, ATTACK1 = None, None

    NUMBER_OF_CHARACTERS = None
    CHAR_SCALE = None
    # END CONSTANTS

    def init_const(self):
        global PIXEL_PER_METER, GRAVITY_M2PS, GRAVITY_P2PS
        global RUN_SPEED_KMPH, RUN_SPEED_MPS, RUN_SPEED_PPS
        global JUMP_SPEED_KMPH, JUMP_SPEED_MPS, JUMP_SPEED_PPS
        global TIME_PER_ACTION, ACTION_PER_TIME
        global STAND_R, STAND_L, RUN_R, RUN_L, JUMP_R, JUMP_L
        global MOVE, ATTACK1, CHAR_SCALE

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

    def init_vars(self, id):
        self.id, = id
        self.jump_start_time
        self.jump_start_y, self.jump_curr_time = 0, 0
        self.jump_key_down, self.left_key_down, self.right_key_down = False, False, False
        self.frame, self.state = 0, Character.STAND_R
        self.sprite_state = Character.MOVE
        self.x, self.y = 100, 100
        self.total_frames = 0.0

    def init_chars(self, char_name):
        global NUMBER_OF_CHARACTERS
        NUMBER_OF_CHARACTERS = 0
        self.sprite = {}
        self.chars = {}
        chars_file = open('Characters/characters.txt', 'r')
        char_info = json.load(chars_file)
        chars_file.close()

        for name in char_info:
            NUMBER_OF_CHARACTERS += 1
            if name == char_name:
                sprite_file = open(char_info[name]['sprite'], 'r')
                sprite_info = json.load(sprite_file)
                sprite_file.close()
                for action in sprite_info:
                    self.sprite = { "action": action,
                                    "img": load_image(sprite_info[action]['path']),
                                    "SFrames": sprite_info[action]['SFrames'],
                                    "RFrames": sprite_info[action]['RFrames'],
                                    "JFrames": sprite_info[action]['JFrames'],
                                    "w": sprite_info[action]["w"],
                                    "h": sprite_info[action]["h"] }
                self.char = {"name": name, "img": load_image(char_info[name]['img']), "sprite": self.sprite }
                break

    def __init__(self, char_name, id : int):
        self.init_const()
        self.init_vars(id)
        self.init_chars(char_name)

    def draw_img(self, x, y):
        self.char['img'].draw(x, y)

    def draw_sprite(self):
        h = self.char['sprite'][self.sprite_state]['h']
        w = self.char['sprite'][self.sprite_state]['w']
        self.char['sprite'][self.sprite_state]['img'].clip_draw(self.frame*w, self.state*h,
                                                                           w, h, self.x, self.y, w*CHAR_SCALE,
                                                                                                 h*CHAR_SCALE)

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def update(self, frame_time):
        self.update_frames(frame_time)
        self.move(frame_time)

    def update_frames(self, frame_time):
        state_frames = None
        if self.state in (Character().STAND_R, Character().STAND_L):
            state_frames = 'SFrames'
        elif self.state in (Character().RUN_R, Character().RUN_L):
            state_frames = 'RFrames'
        elif self.state in (Character().JUMP_R, Character().JUMP_L):
            state_frames = 'JFrames'
        self.total_frames += self.char['sprite'][self.sprite_state][state_frames] \
                             * Character.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % self.char['sprite'][self.sprite_state][state_frames]

    def move(self, frame_time):
        def clamp(minimum, x, maximum):
            return max(minimum, min(x, maximum))

        distance = Character.RUN_SPEED_PPS * frame_time

        if self.jump_key_down:
            self.jump_time += frame_time
            dt = self.jump_time - self.jump_start_time
            self.y = self.jump_start_y + Character.JUMP_SPEED_PPS * dt - Character.GRAVITY_P2PS * dt * dt
            # change to collision boxes after
            if self.y <= self.jump_start_y:
                self.y = self.jump_start_y
                self.jump_key_down = False

        if self.left_key_down:
            self.x -= distance

        if self.right_key_down:
            self.x += distance

        self.x = clamp(0, self.x, 800)

        if not self.right and not self.left and not self.jmp:
            if self.state == Character.RUN_R or self.state== Character.JUMP_R:
                self.state = Character.STAND_R
            elif self.state == Character.RUN_L or self.state== Character.JUMP_L:
                self.state = Character.STAND_L

    def get_name(self):
        return self.char['name']

    def num_of_chars(self):
        return Character.NUMBER_OF_CHARACTERS

    def draw_all_chars(self):
        # count = 0
        #  while count < len(Character.char):
        #    Character.char[count]['img'].draw(145 + (count % 3) * 250, 350 - int(count / 3) * 200)
        #    count += 1
        pass

    def handle_events(self, frame_time, event, player_id, left_key, right_key, jump_key):
        if player_id == self.id:
            if event.key == left_key:
                self.left_key_down = event.type == SDL_KEYDOWN
            if event.key == right_key:
                self.right_key_down = event.type == SDL_KEYDOWN
            if event.key == jump_key and not self.jump_key_down:
                self.jump_key_down = True
                self.jump_start_time = frame_time
                self.jump_time = frame_time
                self.jump_start_y = self.y
                self.frame = 0
                if self.state in (Character().STAND_R, Character().RUN_R):
                    self.state = Character.JUMP_R
                elif self.state in (Character().STAND_L, Character().RUN_L):
                    self.state = Character.JUMP_L