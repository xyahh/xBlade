import pFramework
from pico2d import *

import map_select

name = "CharSelect"
back_img, char_sel = None, None
char_img = []

def enter():
    global back_img, char_sel, char_img
    back_img = load_image('Map/sel_back.png')
    char_sel = load_image('Characters/char_sel.png')

    if len(char_img) == 0:
        char_img.append(load_image('Characters/athenna_img.png'))
        char_img.append(load_image('Characters/bronker_img.png'))
        char_img.append(load_image('Characters/clyde_img.png'))
        char_img.append(load_image('Characters/xyan_img.png'))
        char_img.append(load_image('Characters/yggdrasil_img.png'))
        char_img.append(load_image('Characters/zero_img.png'))

def exit():
    global back_img, char_sel, char_img
    del(back_img, char_sel, char_img)

def update():
    pass

def draw():
    clear_canvas()
    back_img.draw(400, 300)
    char_sel.draw(400, 550)
    count = 0
    for i in char_img:
        i.draw(145+(count%3)*250, 350-int(count/3)*200)
        count+=1
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            pFramework.pop_state()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RETURN):
            pFramework.push_state(map_select)
        elif event.type == SDL_QUIT:
            pFramework.quit()

def resume():
    pass

def pause():
    pass
