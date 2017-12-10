from pico2d import *

from General import pFramework
from General import key_mapping as key
from Menu import main_menu
from Characters.char_class import CharacterSelect
from Maps import map_select
file_name = "CharSelect"

images, arrows = None, None
font = None
char_sel, text = None, None
player_colors = None

def init_media():
    global images, arrows, font, char_sel, text, player_colors

    char_sel = CharacterSelect(main_menu.num_of_players)

    media_file = open('Characters/media.txt', 'r')
    media_info = json.load(media_file)
    media_file.close()

    font_path = open('General/font.txt', 'r')
    font_info = json.load(font_path)
    font_path.close()
    font = load_font(font_info['font']['path'], font_info['font']['size'])

    player_colors = {}
    for id in font_info['player_colors']:
        player_colors[int(id)] = (font_info['player_colors'][id]['R'],
                                       font_info['player_colors'][id]['G'],
                                       font_info['player_colors'][id]['B'])

    text = []
    for name in media_info['text']:
        if media_info['text'][name]['player_id'] <= main_menu.num_of_players:
            text.append({"player_id": media_info['text'][name]['player_id'],
                         "x": media_info['text'][name]['x'],
                         "y": media_info['text'][name]['y']})

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

def enter():
    init_media()


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
        id = text[i]['player_id']
        font.draw(text[i]['x'], text[i]['y'], char_sel.chars[char_sel.player_choice[i]]['name'],
                  player_colors[id])


def draw(frame_time):
    clear_canvas()
    draw_media()
    char_sel.draw()
    update_canvas()


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN:
            for i in range(len(key.controls)):
                char_sel.handle_events(frame_time, event, key.controls[i]['player_id'],
                                       key.controls[i]['left'], key.controls[i]['right'],
                                       key.controls[i]['up'], key.controls[i]['down'])
                if event.key == key.controls[i]['pause']:
                    pFramework.pop_state()
                    break
                if event.key == key.controls[i]['submit']:
                    pFramework.push_state(map_select)
        elif event.type == SDL_QUIT:
            pFramework.quit()


def resume():
    pass


def pause():
    pass
