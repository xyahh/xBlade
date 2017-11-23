import pFramework
from pico2d import *

import main_menu
file_name = "StartState"
image = None
background_img = None
logo_time = 0.0
fade_out = False
fade_in = True
alpha = 0.0


def enter():
    global image
    global background_img
    open_canvas(title='X-Blade')
    image = load_image('Logo/Logo.png')
    background_img= load_image('Logo/LogoOr.png')


def exit():
    global image
    del(image)
    close_canvas()


def update(frame_time):
    global logo_time
    global alpha
    global fade_in
    global fade_out
    if logo_time > 1.0 and fade_out:
        logo_time = 0
        pFramework.push_state(main_menu)
    elif logo_time > 2.0:
        fade_out = True
        logo_time = 0
    delay(0.01)
    logo_time += 0.01
    if alpha<1.0 and fade_in:
        alpha += 0.01
    elif alpha>=1.0 and fade_in:
        fade_in = False
        logo_time=0
    elif alpha>=0.0 and fade_out:
        alpha-=0.01


def draw(frame_time):
    clear_canvas()
    background_img.draw(400,300)
    image.opacify(alpha)
    image.draw(400, 300)
    update_canvas()


def handle_events(frame_time):
    global logo_time
    events = get_events()

    for event in events:
        if event.type ==SDL_KEYDOWN or event.type==SDL_MOUSEBUTTONDOWN:
            logo_time = 0
            pFramework.push_state(main_menu)
        elif event.type==SDL_QUIT:
            pFramework.quit()



def pause(): pass


def resume(): pass




