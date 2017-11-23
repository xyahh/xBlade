import pFramework
from pico2d import *

import map_select
import main_menu
from char_class import Character
file_name = "CharSelect"
back_img, char_sel, red_arrow, blue_arrow = None, None, None, None
p_txt = None
char1, char2 = None, None


def enter():
    global back_img, char_sel, char1, char2, blue_arrow, red_arrow
    global p_txt
    back_img = load_image('Map/sel_back.png')
    char_sel = load_image('Characters/char_sel.png')
    blue_arrow = load_image('Characters/blue_arrow.png')
    red_arrow = load_image('Characters/red_arrow.png')
    p_txt = load_font('Menu/lotr_font.ttf')
    char1 = Character()
    char2 = Character()

def exit():
    global back_img, char_sel, red_arrow, blue_arrow, p_txt, char1, char2
    del(back_img, char_sel, red_arrow, blue_arrow, p_txt, char1, char2)

def update(frame_time):
    pass

def back_design_draw():
    back_img.draw(400, 300)
    char_sel.draw(400, 550)

def draw(frame_time):
    clear_canvas()
    back_design_draw()
    char1.draw_all_chars()
    blue_arrow.draw(115+(char1.id%3)*250, 450-int(char1.id/3)*200)
    p_txt.draw(20, 30, char1.get_name(), (0, 0, 255))
    if(main_menu.selected_option==1):
        red_arrow.draw(175+(char2.id%3)*250, 450-int(char2.id/3)*200)
        p_txt.draw(650, 30,  char2.get_name(), (255, 0, 0))
    update_canvas()

def handle_arrow1(event):
    global char1
    if (event.type, event.key) == (SDL_KEYDOWN, SDLK_a):
        if (char1.id  % 3 == 0):char1.id  += 2
        else: char1.id  = (char1.id - 1) % char1.num_of_chars()
    elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_d):
        if ((char1.id  + 1) % 3 == 0): char1.id -= 2
        else: char1.id  = (char1.id  + 1) % char1.num_of_chars()
    elif event.type == SDL_KEYDOWN and (event.key == SDLK_w or event.key == SDLK_s):
        if (char1.id < 3): char1.id  += 3
        else: char1.id  -= 3

def handle_arrow2(event):
    global char2
    if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
        if (char2.id  % 3 == 0): char2.id  += 2
        else: char2.id  = (char2.id - 1) % char2.size()
    elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
        if ((char2.id  + 1) % 3 == 0): char2.id  -= 2
        else: char2.id  = (char2.id  + 1) % char2.size()
    elif event.type == SDL_KEYDOWN and (event.key == SDLK_UP or event.key == SDLK_DOWN):
        if (char2.id < 3): char2.id  += 3
        else: char2.id  -= 3

def handle_events(frame_time):
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
