from pico2d import *

from General import pFramework
from Menu import main_menu
from Sound import sound_manager as sound
file_name = "StartState"

images = None
logo_time, alpha = 0.0, 0.0
fade_in, fade_out = None, None

win_width, win_height, win_caption = None, None, None

FADE_TIME_CONSTRAINT, LOGO_SHOW_TIME_CONSTRAINT, MAX_ALPHA_VALUE = None, None, None
alpha_change_rate = None


def init_window():
    global win_width, win_height, win_caption

    window_file = open('Logo/window.txt', 'r')
    window_info = json.load(window_file)
    window_file.close()

    win_width = window_info['width']
    win_height = window_info['height']
    win_caption = window_info['title']

    open_canvas(w=win_width, h=win_height, title=win_caption)


def init_media():
    global images

    sound.add("main", "Sound/menu_theme.wav", is_bgm=True)
    sound.add("submit", "Sound/button_submit.wav", is_bgm=False)
    sound.add("change", "Sound/button_change.wav", is_bgm=False)
    sound.add("back", "Sound/button_back.wav", is_bgm=False)

    image_file = open('Logo/image.txt', 'r')
    image_info = json.load(image_file)
    image_file.close()

    images = []
    for name in image_info:
        images.append({"img": load_image(image_info[name]['path']),
                       "x": image_info[name]['x'], "y": image_info[name]['y'],
                       "opacify": image_info[name]['opacify']})


def init_fade():
    global FADE_TIME_CONSTRAINT, LOGO_SHOW_TIME_CONSTRAINT, MAX_ALPHA_VALUE, alpha_change_rate
    global fade_in, fade_out, logo_time, alpha

    fade_file = open('Logo/fade.txt', 'r')
    file_info = json.load(fade_file)
    fade_file.close()

    fade_in, fade_out = True, False
    FADE_TIME_CONSTRAINT = file_info['FADE_TIME_CONSTRAINT']
    LOGO_SHOW_TIME_CONSTRAINT = file_info['LOGO_SHOW_TIME_CONSTRAINT']
    alpha_change_rate = 1.0 / FADE_TIME_CONSTRAINT
    logo_time, alpha = 0.0, 0.0


def enter():
    init_window()
    init_media()
    init_fade()


def exit():
    global images
    del images
    close_canvas()


def update(frame_time):
    global logo_time, alpha, fade_in, fade_out, alpha_change_rate
    logo_time += frame_time
    if fade_in or fade_out:
        alpha += alpha_change_rate*frame_time
    if logo_time > FADE_TIME_CONSTRAINT and fade_out:
        pFramework.push_state(main_menu)
    elif logo_time > FADE_TIME_CONSTRAINT and fade_in:
        logo_time = 0
        fade_in = False
    elif logo_time > LOGO_SHOW_TIME_CONSTRAINT and not (fade_in or fade_out):
        logo_time = 0
        fade_out = True
        alpha_change_rate = -alpha_change_rate


def draw(frame_time):
    clear_canvas()
    for i in range(len(images)):
        if images[i]['opacify']: images[i]['img'].opacify(alpha)
        images[i]['img'].draw(images[i]['x'], images[i]['y'])
    update_canvas()


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN or event.type == SDL_MOUSEBUTTONDOWN:
            pFramework.push_state(main_menu)
        elif event.type == SDL_QUIT:
            pFramework.quit()


def pause(): pass


def resume(): pass




