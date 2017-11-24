from pico2d import *

from Characters import char_select
from General import game_play, pFramework, key_mapping
from Maps.map_class import Map
from Menu import main_menu

file_name = "MapSelect"

controls, images, text = None, None, None
font, choices = None, None


def init_media():
    global images, font, text, choices

    media_file = open('Maps/media.txt', 'r')
    media_info = json.load(media_file)
    media_file.close()

    font = load_font(media_info['font'])
    choices = []

    text = []
    for name in media_info['text']:
        if media_info['text'][name]['player_id'] <= main_menu.num_of_players:
            text.append({"player_id": media_info['text'][name]['player_id'],
                         "x": media_info['text'][name]['x'],
                         "y": media_info['text'][name]['y'],
                         "RGB": (media_info['text'][name]['red'], media_info['text'][name]['green'],
                                 media_info['text'][name]['blue'])})

    images = []
    for name in media_info['images']:
        images.append({"img": load_image(media_info['images'][name]['path']),
                       "x": media_info['images'][name]['x'], "y": media_info['images'][name]['y']})


def init_controls():
    global controls
    control_file = open('General/controls.txt', 'r')
    control_info = json.load(control_file)
    control_file.close()

    controls = []
    for id in control_info:
        controls.append({"player_id":int(id),
                         "left":  key_mapping.map_key(control_info[id]['left']),
                         "right": key_mapping.map_key(control_info[id]['right']),
                         "pause": key_mapping.map_key(control_info[id]['pause']),
                         "submit": key_mapping.map_key(control_info[id]['submit'])})


def enter():
    init_media()
    init_controls()

def exit():
    global controls, images, text, font, choices
    del controls, images, text, font, choices

def update(frame_time):
    pass

def draw(frame_time):
    clear_canvas()
    #back_design_draw()
    #character_info_draw()
    #map_draw()
    update_canvas()

def handle_events(frame_time):
    global maps
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                pFramework.pop_state()
            elif event.key == SDLK_a:
                if maps.id - 1 < 0:
                    maps.id = maps.size() - 1
                else:
                    maps.id -= 1
            elif event.key == SDLK_d:
                if maps.id + 1 >= maps.size():
                    maps.id = 0
                else:
                    maps.id += 1
            elif event.key == SDLK_RETURN:
                pFramework.push_state(game_play)
        elif event.type == SDL_QUIT:
            pFramework.quit()

def resume():
    pass

def pause():
    pass
