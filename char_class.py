from pico2d import *
file_name = "CharacterClass"


class Character:
    # CONSTANTS
    PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
    RUN_SPEED_KMPH = 40.0  # Km / Hour
    RUN_SPEED_MPS = (RUN_SPEED_KMPH * 1000.0 / 3600.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    GRAVITY_M2PS = 1.2
    GRAVITY_P2PS = GRAVITY_M2PS * PIXEL_PER_METER * PIXEL_PER_METER

    JUMP_SPEED_KMPH = 100.0
    JUMP_SPEED_MPS = (JUMP_SPEED_KMPH *1000.0 / 3600.0)
    JUMP_SPEED_PPS = (JUMP_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

    STAND_R, STAND_L, RUN_R, RUN_L, JUMP_R, JUMP_L = 0, 1, 2, 3, 4, 5
    MOVE, ATTACK1 = 0, 1
    # END CONSTANTS

    char = []

    def __init__(self):
        self.jump_start_time, self.jump_start_y, self.jump_time = 0.0, 0.0, 0.0
        self.id = 0
        self.sprite = []
        #state hard-coded for now. Will add the Starting state later through JSON
        self.frame, self.state = 0, Character.STAND_R
        self.jmp, self.left, self.right = False, False, False
        # Coordinates are hard-coded for now. Will add the Starting Spawn Coordinates through JSON
        self.x, self.y = 100, 100
        self.sprite_state = Character.MOVE
        self.total_frames = 0.0
        if len(Character.char)==0:
            chars_file = open('Characters/characters.txt', 'r')
            char_info= json.load(chars_file)
            chars_file.close()
            for name in char_info:
                if len(self.sprite) == 0:
                    sprite_file = open(char_info[name]['sprite'], 'r')
                    sprite_info = json.load(sprite_file)
                    sprite_file.close()
                    for _type in sprite_info:
                        self.sprite.append({"anim": _type, "img": load_image(sprite_info[_type]['path']),
                                            "SFrames": sprite_info[_type]['SFrames'],
                                            "RFrames": sprite_info[_type]['RFrames'],
                                            "JFrames": sprite_info[_type]['JFrames'],
                                            "w":sprite_info[_type]["x"], "h":sprite_info[_type]["y"]})
                Character.char.append({"name": name, "img": load_image(char_info[name]['img']), "spr": self.sprite})

    def draw_img(self, x, y):
        Character.char[self.id]['img'].draw(x, y)

    def draw_sprite(self):
        h = Character.char[self.id]['spr'][self.sprite_state]['h']
        w = Character.char[self.id]['spr'][self.sprite_state]['w']
        Character.char[self.id]['spr'][self.sprite_state]['img'].clip_draw(self.frame*w, self.state*h,
                                                                           w, h, self.x, self.y, w*2, h*2)

    def update(self, frame_time):
        state_frames = None
        def clamp(minimum, x, maximum):
            return max(minimum, min(x, maximum))

        if self.state == Character.STAND_R or self.state == Character.STAND_L:
            state_frames = 'SFrames'
        elif self.state == Character.RUN_R or self.state == Character.RUN_L:
            state_frames = 'RFrames'
        elif self.state == Character.JUMP_R or self.state == Character.JUMP_L:
            state_frames = 'JFrames'
        self.total_frames += Character.char[self.id]['spr'][self.sprite_state][state_frames] \
                             * Character.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % Character.char[self.id]['spr'][self.sprite_state][state_frames]
        self.move(frame_time)
        self.x = clamp(0, self.x, 800)

    def move(self, frame_time):
        distance = Character.RUN_SPEED_PPS * frame_time

        if self.jmp:
            self.jump_time += frame_time
            t = self.jump_time - self.jump_start_time
            self.y = self.jump_start_y + Character.JUMP_SPEED_PPS*t - Character.GRAVITY_P2PS*t*t
            if self.y <= self.jump_start_y: # change to collision boxes after
                self.y = self.jump_start_y
                self.jmp = False

        if self.left:
            self.x -= distance
            if self.jmp: self.state = Character.JUMP_L
            else: self.state = Character.RUN_L
        if self.right:
            self.x += distance
            if self.jmp: self.state = Character.JUMP_R
            else: self.state = Character.RUN_R

        if not self.right and not self.left and not self.jmp:
            if self.state == Character.RUN_R or self.state== Character.JUMP_R: self.state = Character.STAND_R
            elif self.state == Character.RUN_L or self.state== Character.JUMP_L: self.state = Character.STAND_L

    def get_name(self):
        return Character.char[self.id]['name']

    def size(self):
        return len(Character.char)

    def draw_all_chars(self):
        count = 0
        while count < len(Character.char):
            Character.char[count]['img'].draw(145 + (count % 3) * 250, 350 - int(count / 3) * 200)
            count += 1

    def handle_events(self, frame_time, event, key_left, key_right, key_jump):
        if event.key == key_left:
            self.left = event.type == SDL_KEYDOWN
        if event.key == key_right:
            self.right = event.type == SDL_KEYDOWN
        if event.key == key_jump and not self.jmp:
            self.jump_start_time = frame_time
            self.jump_time = frame_time
            self.jump_start_y = self.y
            self.frame = 0
            self.jmp = True
            if not self.right and not self.left:
                if self.state == Character.STAND_R: self.state = Character.JUMP_R
                elif self.state == Character.STAND_L: self.state = Character.JUMP_L