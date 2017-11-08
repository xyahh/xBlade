import pFramework
from pico2d import *

import map_select
import main_menu

name = "CharSelect"
back_img, char_sel, arrow, arrow2 = None, None, None, None
selected_char = 0
selected_char2 = 1
char_number = 6
char_img = []

def enter():
    global back_img, char_sel, char_img, arrow, arrow2
    back_img = load_image('Map/sel_back.png')
    char_sel = load_image('Characters/char_sel.png')
    arrow = load_image('Characters/arrow.png')
    arrow2 = load_image('Characters/arrow2.png')
    char_img = []
    char_img.append(load_image('Characters/athenna_img.png'))
    char_img.append(load_image('Characters/bronker_img.png'))
    char_img.append(load_image('Characters/clyde_img.png'))
    char_img.append(load_image('Characters/xyan_img.png'))
    char_img.append(load_image('Characters/yggdrasil_img.png'))
    char_img.append(load_image('Characters/zero_img.png'))

def exit():
    global back_img, char_sel, char_img, arrow, arrow2
    del(back_img, char_sel, char_img, arrow, arrow2)

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
    arrow.draw(145+(selected_char%3)*250, 450-int(selected_char/3)*200)
    if(main_menu.selected_option==1): arrow2.draw(145+(selected_char2%3)*250, 450-int(selected_char2/3)*200)
    update_canvas()

def handle_arrow1(event):
    global selected_char
    if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
        if (selected_char % 3 == 0):selected_char += 2
        else: selected_char = (selected_char - 1) % char_number
    elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
        if ((selected_char + 1) % 3 == 0): selected_char -= 2
        else: selected_char = (selected_char + 1) % char_number
    elif event.type == SDL_KEYDOWN and (event.key == SDLK_UP or event.key == SDLK_DOWN):
        if (selected_char < 3): selected_char += 3
        else: selected_char -= 3

def handle_arrow2(event):
    global selected_char2
    if (event.type, event.key) == (SDL_KEYDOWN, SDLK_a):
        if (selected_char2 % 3 == 0):selected_char2 += 2
        else: selected_char2 = (selected_char2 - 1) % char_number
    elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_d):
        if ((selected_char2 + 1) % 3 == 0): selected_char2 -= 2
        else: selected_char2 = (selected_char2 + 1) % char_number
    elif event.type == SDL_KEYDOWN and (event.key == SDLK_w or event.key == SDLK_s):
        if (selected_char2 < 3): selected_char2 += 3
        else: selected_char2 -= 3

def handle_events():
    events = get_events()
    for event in events:
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            pFramework.pop_state()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RETURN):
            pFramework.push_state(map_select)
        elif (event.type==SDL_KEYDOWN) and (event.key == SDLK_UP or event.key==SDLK_DOWN or event.key == SDLK_LEFT or event.key==SDLK_RIGHT):
            handle_arrow1(event)
        elif (event.type==SDL_KEYDOWN) and (main_menu.selected_option== 1) and (event.key == SDLK_w or event.key==SDLK_s or event.key == SDLK_a or event.key==SDLK_d):
            handle_arrow2(event)
        elif event.type == SDL_QUIT:
            pFramework.quit()

def resume():
    pass

def pause():
    pass
