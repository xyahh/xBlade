import pFramework
from pico2d import *

import map_select
import main_menu

name = "CharSelect"
back_img, char_sel, red_arrow, blue_arrow = None, None, None, None
p_txt = None
selected_char, selected_char2 = 0, 0
char_number = 6
chars = []

def enter():
    global back_img, char_sel, chars, blue_arrow, red_arrow
    global p_txt, selected_char, selected_char2
    back_img = load_image('Map/sel_back.png')
    char_sel = load_image('Characters/char_sel.png')
    blue_arrow = load_image('Characters/blue_arrow.png')
    red_arrow = load_image('Characters/red_arrow.png')
    selected_char, selected_char2 = 0, 0
    chars = []
    chars.append({'name': 'Athenna',     'img': load_image('Characters/athenna_img.png')})
    chars.append({'name': 'Bronker',     'img': load_image('Characters/bronker_img.png')})
    chars.append({'name': 'Clyde',       'img': load_image('Characters/clyde_img.png')})
    chars.append({'name': 'Xyan',        'img': load_image('Characters/xyan_img.png')})
    chars.append({'name': 'Yggdrasil',  'img': load_image('Characters/yggdrasil_img.png')})
    chars.append({'name': 'Zero',        'img': load_image('Characters/zero_img.png')})
    p_txt = load_font('Menu/lotr_font.ttf')

def exit():
    global back_img, char_sel, chars, red_arrow, blue_arrow, p_txt
    del(back_img, char_sel, chars, red_arrow, blue_arrow, p_txt)

def update():
    pass

def draw():
    clear_canvas()
    back_img.draw(400, 300)
    char_sel.draw(400, 550)
    count = 0
    for i in chars:
        i['img'].draw(145+(count%3)*250, 350-int(count/3)*200)
        count+=1
    blue_arrow.draw(115+(selected_char%3)*250, 450-int(selected_char/3)*200)
    p_txt.draw(20, 30, chars[selected_char]['name'], (0, 0, 255))
    if(main_menu.selected_option==1):
        red_arrow.draw(175+(selected_char2%3)*250, 450-int(selected_char2/3)*200)
        p_txt.draw(650, 30, chars[selected_char2]['name'], (255, 0, 0))
    update_canvas()

def handle_arrow1(event):
    global selected_char
    if (event.type, event.key) == (SDL_KEYDOWN, SDLK_a):
        if (selected_char % 3 == 0):selected_char += 2
        else: selected_char = (selected_char - 1) % char_number
    elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_d):
        if ((selected_char + 1) % 3 == 0): selected_char -= 2
        else: selected_char = (selected_char + 1) % char_number
    elif event.type == SDL_KEYDOWN and (event.key == SDLK_w or event.key == SDLK_s):
        if (selected_char < 3): selected_char += 3
        else: selected_char -= 3

def handle_arrow2(event):
    global selected_char2
    if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
        if (selected_char2 % 3 == 0):selected_char2 += 2
        else: selected_char2 = (selected_char2 - 1) % char_number
    elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
        if ((selected_char2 + 1) % 3 == 0): selected_char2 -= 2
        else: selected_char2 = (selected_char2 + 1) % char_number
    elif event.type == SDL_KEYDOWN and (event.key == SDLK_UP or event.key == SDLK_DOWN):
        if (selected_char2 < 3): selected_char2 += 3
        else: selected_char2 -= 3

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE: pFramework.pop_state()
            elif event.key == SDLK_RETURN: pFramework.push_state(map_select)
            elif event.key == SDLK_w or event.key == SDLK_s or event.key == SDLK_a or event.key == SDLK_d:
                handle_arrow1(event)
            elif main_menu.selected_option==1 and (event.key == SDLK_UP or event.key==SDLK_DOWN or event.key == SDLK_LEFT or event.key==SDLK_RIGHT):
                handle_arrow2(event)

        elif event.type == SDL_QUIT:
            pFramework.quit()

def resume():
    pass

def pause():
    pass
