from pico2d import *

# If a Key is missing, feel free to add it here.
KEY_MAP = \
{
    #alphabet
    "A": SDLK_a, "B": SDLK_b, "C": SDLK_c, "D": SDLK_d, "E": SDLK_e, "F": SDLK_f,
    "G": SDLK_g, "H": SDLK_h, "I": SDLK_i, "J": SDLK_j, "K": SDLK_k, "L": SDLK_l,
    "M": SDLK_m, "N": SDLK_n, "O": SDLK_o, "P": SDLK_p, "Q": SDLK_q, "R": SDLK_r,
    "S": SDLK_s, "T": SDLK_t, "U": SDLK_u, "V": SDLK_v, "W": SDLK_w, "X": SDLK_x,
    "Y": SDLK_y, "Z": SDLK_z,

    #special
    "UP": SDLK_UP,          "DOWN": SDLK_DOWN,      "LEFT": SDLK_LEFT,      "RIGHT": SDLK_RIGHT,
    "ESC": SDLK_ESCAPE,     "DEL": SDLK_DELETE,     "ENTER": SDLK_RETURN,   "SPACE": SDLK_SPACE,
    "BACK": SDLK_BACKSPACE, "TAB": SDLK_TAB,        "LSHIFT": SDLK_LSHIFT,  "RSHIFT" : SDLK_RSHIFT,
    "LCTRL": SDLK_LCTRL,    "RCTRL": SDLK_RCTRL,    "CAPS": SDLK_CAPSLOCK,  "HOME": SDLK_HOME,

    #numbers
    "0": SDLK_0, "F1": SDLK_F1, "F11": SDLK_F11, "F21" :SDLK_F21,
    "1": SDLK_1, "F2": SDLK_F2, "F12": SDLK_F12, "F22" :SDLK_F22,
    "2": SDLK_2, "F3": SDLK_F3, "F13": SDLK_F13, "F23" :SDLK_F23,
    "3": SDLK_3, "F4": SDLK_F4, "F14": SDLK_F14, "F24" :SDLK_F24,
    "4": SDLK_4, "F5": SDLK_F5, "F15": SDLK_F15,
    "5": SDLK_5, "F6": SDLK_F6, "F16": SDLK_F16,
    "6": SDLK_6, "F7": SDLK_F7, "F17": SDLK_F17,
    "7": SDLK_7, "F8": SDLK_F8, "F18": SDLK_F18,
    "8": SDLK_8, "F9": SDLK_F9, "F19": SDLK_F19,
    "9": SDLK_9, "F10": SDLK_F10, "F20": SDLK_F20
}

controls = None

def map_key(string):
    return KEY_MAP[string]


def bind_keys():
    global controls
    control_file = open('General/controls.txt', 'r')
    control_info = json.load(control_file)
    control_file.close()

    controls = []
    for id in control_info:
        controls.append({"player_id": int(id),
                         "up": map_key(control_info[id]['up']),
                         "down": map_key(control_info[id]['down']),
                         "left": map_key(control_info[id]['left']),
                         "right": map_key(control_info[id]['right']),
                         "pause": map_key(control_info[id]['pause']),
                         "submit": map_key(control_info[id]['submit'])})
