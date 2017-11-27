from pico2d import *
import pyglet  # 3rd party audio player
from pyglet.media import Player
from Characters import char_select
from General import pFramework, key_mapping

file_name = "MainMenu"

RECT_W, RECT_H = None, None
images, font = None, None
song, player = None, None
options, controls = None, None
num_of_players, num_of_players_choices, choice = None, None, None


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


def init_images():
    global images
    image_file = open('Menu/image.txt', 'r')
    image_info = json.load(image_file)
    image_file.close()

    images = []
    for name in image_info:
        images.append({"img": load_image(image_info[name]['path']),
                       "x": image_info[name]['x'], "y": image_info[name]['y']})


def init_pyglet():
    global song, player, main_theme
    song = pyglet.media.load('Menu/menu_theme.mp3')
    player = Player()
    player.queue(song)
    player.eos_action = player.EOS_LOOP
    player.play()


def init_menu():
    global font, options, RECT_H, RECT_W, num_of_players_choices, choice
    menu_file = open('Menu/menu.txt', 'r')
    menu_info = json.load(menu_file)
    menu_file.close()

    font = load_font(menu_info['font']['path'], menu_info['font']['size'])
    RECT_W = menu_info['rect_size']['width']
    RECT_H = menu_info['rect_size']['height']
    num_of_players_choices = []
    options = []

    for name in menu_info['options']:
        y = menu_info['options'][name]['start_y'] + \
            menu_info['options'][name]['diff_y'] * menu_info['options'][name]['priority']
        options.append({"name": name, "x": menu_info['options'][name]['x'], "y": y})
        num_of_players_choices.append(menu_info['options'][name]['num_of_players'])
    choice = len(num_of_players_choices) - 1 # just as a default value


def enter():
    init_images()
    init_menu()
    init_pyglet()
    init_controls()


def exit():
    global images, options
    del images, options


def update(frame_time):
    pass


def draw(frame_time):
    clear_canvas()
    for i in range(len(images)):
        images[i]['img'].draw(images[i]['x'], images[i]['y'])
    for i in options:
        font.draw(i['x'], i['y'], i['name'])
    draw_rectangle(options[choice]['x'], options[choice]['y']-RECT_H/2,
                   options[choice]['x']+RECT_W, options[choice]['y']+RECT_H/2)
    update_canvas()


def handle_events(frame_time):
    global num_of_players, choice
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN:
            for i in range(len(controls)):  # can add the control id check if only one player needs to control menu
                if event.key == controls[i]['up']:
                    choice= (choice + 1) % len(options)
                elif event.key == controls[i]['down']:
                    choice = (choice - 1) % len(options)
                elif event.key == controls[i]['submit']:
                    if choice > 0:
                        num_of_players = num_of_players_choices[choice]
                        pFramework.push_state(char_select)
                    else:
                        pFramework.quit()

        elif event.type==SDL_QUIT:
            pFramework.quit()


def pause(): pass


def resume(): pass




