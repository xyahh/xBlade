import pFramework
from pico2d import *

import pyglet #3rd party audio player
from pyglet.media import Player
import char_select

file_name = "MainMenu"

images = None
font = None
menu_txt = None
options = []
timer = 0
num_of_players = 0
show_menu = False
song = None
player = None


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
    global font, options
    menu_file = open('Menu/menu.txt', 'r')
    menu_info = json.load(menu_file)
    menu_file.close()

    font = load_font(menu_info['font']['path'], menu_info['font']['size'])
    for name in menu_info['options']:
        y = menu_info['options'][name]['start_y'] + \
            menu_info['options'][name]['diff_y'] * menu_info['options'][name]['priority']
        options.append({"name": name, "x":menu_info['options'][name]['x'], "y":y})


def enter():
    init_images()
    init_menu()
    init_pyglet()


def exit():
    global menu_txt, options
    del(menu_txt, options)


def update(frame_time):
    global timer
    timer += 1
    delay(0.01)


def draw(frame_time):
    clear_canvas()
    for i in range(len(images)):
        images[i]['img'].draw(images[i]['x'], images[i]['y'])
    for i in options:
        font.draw(i['x'], i['y'], i['name'])

    #draw_rectangle(280, 230 - (selected_option * 70), 525, 170 - (selected_option * 70))
    update_canvas()


def handle_events(frame_time):
    global selected_option
    global show_menu
    events = get_events()
    for event in events:
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_w):
            selected_option-=1
            if(selected_option<0): selected_option=2
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_s):
            selected_option += 1
            if (selected_option > 2): selected_option = 0
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RETURN):
            if show_menu:
                if selected_option==0 or selected_option==1:
                    pFramework.push_state(char_select)
                elif selected_option==2:
                    pFramework.quit()
            else: show_menu = True
        elif event.type==SDL_QUIT:
            pFramework.quit()


def pause(): pass


def resume(): pass




