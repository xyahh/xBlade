from pico2d import *
from Characters import char_select
from General import pFramework
from General import key_mapping as key

file_name = "MainMenu"

num_of_players, num_of_players_choices, choice = None, None, None
options, main_theme = None, None
RECT_W, RECT_H = None, None
images, font = None, None

def init_images():
    global images
    image_file = open('Menu/image.txt', 'r')
    image_info = json.load(image_file)
    image_file.close()

    images = []
    for name in image_info:
        images.append({"img": load_image(image_info[name]['path']),
                       "x": image_info[name]['x'], "y": image_info[name]['y']})


def init_sounds():
    global main_theme
    main_theme = load_music('Menu/menu_theme.mp3')
    main_theme.set_volume(64)
    #main_theme.repeat_play()


def init_menu():
    global font, options, RECT_H, RECT_W, num_of_players_choices, choice
    key.bind_keys()
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
    init_sounds()
    init_images()
    init_menu()


def exit():
    global images, options, main_theme
    del images, options, main_theme


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
            for i in range(len(key.controls)):  # can add the control id check if only one player needs to control menu
                if event.key == key.controls[i]['up']:
                    choice= (choice + 1) % len(options)
                elif event.key == key.controls[i]['down']:
                    choice = (choice - 1) % len(options)
                elif event.key == key.controls[i]['submit']:
                    if choice > 0:
                        num_of_players = num_of_players_choices[choice]
                        pFramework.push_state(char_select)
                    else:
                        pFramework.quit()

        elif event.type==SDL_QUIT:
            pFramework.quit()


def pause(): pass


def resume(): pass




