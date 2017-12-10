from pico2d import *

from General import game_play, pFramework
from General import key_mapping as key
from Maps.map_class import MapSelect
from Characters import char_select
from Menu import main_menu

file_name = "MapSelect"

images, map_text = None, None
player_text, custom_text = None, None
font, choices, map_sel = None, None, None
player_colors = None


def init_media():
    global images, choices, map_sel

    map_sel = MapSelect()

    media_file = open('Maps/media.txt', 'r')
    media_info = json.load(media_file)
    media_file.close()

    choices = []
    images = []
    for name in media_info['images']:
        images.append({"img": load_image(media_info['images'][name]['path']),
                       "is_map_border": media_info['images'][name]['is_map_border'],
                       "x": media_info['images'][name]['x'],
                       "y": media_info['images'][name]['y']})


def init_text():
    global font, map_text, player_text, custom_text, player_colors

    text_file = open('Maps/text.txt', 'r')
    text_info = json.load(text_file)
    text_file.close()

    font_path = open('General/font.txt', 'r')
    font_info = json.load(font_path)
    font_path.close()
    font = load_font(font_info['font']['path'], font_info['font']['size'])

    player_text = []
    custom_text = []
    map_text = {}

    player_colors = {}
    for id in font_info['player_colors']:
        player_colors[int(id)] = (font_info['player_colors'][id]['R'],
                                  font_info['player_colors'][id]['G'],
                                  font_info['player_colors'][id]['B'])

    for name in text_info['player_text']:
        player_text.append({"player_id": text_info['player_text'][name]['player_id'],
                            "x": text_info['player_text'][name]['x'],
                            "y": text_info['player_text'][name]['y']})

    for name in text_info['custom_text']:
        custom_text.append({"string": text_info['custom_text'][name]['string'],
                            "x": text_info['custom_text'][name]['x'],
                            "y": text_info['custom_text'][name]['y'],
                            "RGB": (text_info['custom_text'][name]['red'],
                                    text_info['custom_text'][name]['green'],
                                    text_info['custom_text'][name]['blue'])})

    map_text = {"x": text_info['map_text']['map_name']['x'],
                "y": text_info['map_text']['map_name']['y'],
                "RGB": (text_info['map_text']['map_name']['red'],
                         text_info['map_text']['map_name']['green'],
                         text_info['map_text']['map_name']['blue'])}


def enter():
    init_media()
    init_text()


def exit():
    global images, custom_text, font, choices, map_text, player_text
    del images, custom_text, font, choices, map_text, player_text


def update(frame_time):
    pass


def draw(frame_time):
    clear_canvas()
    for i in range(len(images)):
        if images[i]['is_map_border']:
            map_sel.draw(images[i]['x'], images[i]['y'])
        images[i]['img'].draw(images[i]['x'], images[i]['y'])

    for i in range(len(custom_text)):
        font.draw(custom_text[i]['x'], custom_text[i]['y'], custom_text[i]['string'], custom_text[i]['RGB'])

    for i in range(len(player_text)):
        if i < main_menu.num_of_players:
            id = player_text[i]['player_id']
            char_name = char_select.char_sel.chars[char_select.char_sel.player_choice[i]]['name']
            font.draw(player_text[i]['x'], player_text[i]['y'], char_name, player_colors[id])

    font.draw(map_text['x'], map_text['y'], map_sel.get_curr_map_name(), map_text['RGB'])
    update_canvas()


def handle_events(frame_time):
    global maps
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN:
            for i in range(len(key.controls)):
                map_sel.handle_events(event, key.controls[i]['left'], key.controls[i]['right'])
                if event.key == key.controls[i]['pause']:
                    pFramework.pop_state()
                    break
                if event.key == key.controls[i]['submit']:
                    pFramework.push_state(game_play)
        elif event.type == SDL_QUIT:
            pFramework.quit()


def resume():
    pass


def pause():
    pass
