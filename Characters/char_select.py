from pico2d import *

from General import pFramework, key_mapping
from Menu import main_menu
from Characters.char_class import CharacterSelect
from Maps import map_select
file_name = "CharSelect"

images, arrows = None, None
controls, font = None, None
char_sel, text = None, None


def init_media():
    global images, arrows, font, char_sel, text

    char_sel = CharacterSelect(main_menu.num_of_players)

    media_file = open('Characters/media.txt', 'r')
    media_info = json.load(media_file)
    media_file.close()

    font = load_font(media_info['font'])

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
    arrows = []
    for name in media_info['arrows']:
        if media_info['arrows'][name]['player_id'] <= main_menu.num_of_players:
            arrows.append({"img": load_image(media_info['arrows'][name]['path']),
                           "player_id": media_info['arrows'][name]['player_id'],
                           "x_offset": media_info['arrows'][name]['x_offset'],
                           "y_offset" : media_info['arrows'][name]['y_offset']})


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
    global images, arrows, font, char_sel, text
    del images, arrows, font, char_sel, text


def update(frame_time):
    pass


def draw_media():
    for i in range(len(images)):
        images[i]['img'].draw(images[i]['x'], images[i]['y'])

    for i in range(len(arrows)):
        if i < main_menu.num_of_players:
            arrows[i]['img'].draw((char_sel.player_choice[i] % char_sel.chars_per_row) * char_sel.col_dist_diff
                                  + char_sel.start_x + arrows[i]['x_offset'],
                                  int(char_sel.player_choice[i] / char_sel.chars_per_row) * char_sel.row_dist_diff
                                  + char_sel.start_y + arrows[i]['y_offset'])
    for i in range(main_menu.num_of_players):
        font.draw(text[i]['x'], text[i]['y'], char_sel.chars[char_sel.player_choice[i]]['name'], text[i]['RGB'])


def draw(frame_time):
    clear_canvas()
    draw_media()
    char_sel.draw()
    update_canvas()


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN:
            for i in range(len(controls)):
                char_sel.handle_events(frame_time, event, controls[i]['player_id'],
                                       controls[i]['left'], controls[i]['right'],
                                       controls[i]['up'], controls[i]['down'])
                if event.key == controls[i]['pause']:
                    pFramework.pop_state()
                    break
                if event.key == controls[i]['submit']:
                    pFramework.push_state(map_select)
        elif event.type == SDL_QUIT:
            pFramework.quit()


def resume():
    pass


def pause():
    pass
