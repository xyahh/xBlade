from pico2d import *

from General import pFramework, key_mapping
from Menu import main_menu

file_name = "CharSelect"

images, arrows = None, None
controls, font = None, None


def init_media():
    global images, arrows, font

    media_file = open('Characters/media.txt', 'r')
    media_info = json.load(media_file)
    media_file.close()

    font = load_font(media_info['font'])

    images = []
    for name in media_info['static']:
        images.append({"img": load_image(media_info['static'][name]['path']),
                       "x": media_info['static'][name]['x'], "y": media_info['static'][name]['y']})
    arrows = []
    for name in media_info['dynamic']:
        if media_info['dynamic'][name]['player_id'] <= main_menu.num_of_players:
            arrows.append({"img": load_image(media_info['dynamic'][name]['path']),
                           "x": media_info['dynamic'][name]['x'], "y": media_info['dynamic'][name]['y'],
                           "player_id": media_info['dynamic'][name]['player_id']})


def init_controls():
    global controls
    control_file = open('General/controls.txt', 'r')
    control_info = json.load(control_file)
    control_file.close()

    controls = []
    for id in control_info:
        controls.append({"player_id":int(id),
                         "up":    key_mapping.map_key(control_info[id]['up']),
                         "down":  key_mapping.map_key(control_info[id]['down']),
                         "left":  key_mapping.map_key(control_info[id]['left']),
                         "right": key_mapping.map_key(control_info[id]['right']),
                         "pause": key_mapping.map_key(control_info[id]['pause']),
                         "submit": key_mapping.map_key(control_info[id]['submit'])})


def enter():
    init_media()
    init_controls()

def exit():
    global images, arrows, font
    del images, arrows, font


def update(frame_time):
    pass


def draw(frame_time):
    clear_canvas()
    #blue_arrow.draw(115+(char1.id%3)*250, 450-int(char1.id/3)*200)
    #p_txt.draw(20, 30, char1.get_name(), (0, 0, 255))
    for i in range(len(images)):
        images[i]['img'].draw(images[i]['x'], images[i]['y'])

    for i in range(len(arrows)):
        arrows[i]['img'].draw( arrows[i]['x'],  arrows[i]['y'])
    update_canvas()

def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN:
            for i in range(len(controls)):
                #Character.handle_events(frame_time, event, controls[i]['player_id'],
                #                        controls[i]['left'], controls[i]['right'], controls[i]['up'])
                if event.key == controls[i]['pause']:
                        pFramework.pop_state()
                        break
        elif event.type == SDL_QUIT:
            pFramework.quit()

def resume():
    pass

def pause():
    pass
