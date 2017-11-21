import pFramework
from pico2d import *

from map_class import Map

import main_menu
import char_select
import game_play

name = "MapSelect"
back_img, map_sel, border_img = None, None, None
maps = None
gen_txt = None

def enter():
    global back_img, map_sel, gen_txt, maps, border_img
    maps = Map()
    back_img = load_image('Map/sel_back.png')
    border_img = load_image('Map/map_border.png')
    map_sel = load_image('Map/map_sel.png')
    gen_txt = load_font('Menu/lotr_font.ttf')


def exit():
    global back_img, map_sel, gen_txt, maps, border_img
    del(back_img, map_sel, gen_txt, maps, border_img)

def update(frame_time):
    pass

def back_design_draw():
    back_img.draw(400, 300)
    map_sel.draw(400, 550)
    gen_txt.draw(385, 450, 'vs')

def character_info_draw():
    gen_txt.draw(200, 450, char_select.char1.get_name())
    if main_menu.selected_option == 1: gen_txt.draw(450, 450, char_select.char2.get_name())
    else: gen_txt.draw(450, 450, 'CPU')

def map_draw():
    maps.draw(400, 250, 'dsp_img')
    gen_txt.draw(200, 70, maps.get_name(), (255, 255, 255))
    border_img.draw(400, 250)

def draw(frame_time):
    clear_canvas()
    back_design_draw()
    character_info_draw()
    map_draw()
    update_canvas()

def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                pFramework.pop_state()
            elif event.key == SDLK_a:
                if maps.id - 1 < 0:
                    maps.id = maps.size() - 1
                else:
                    maps.id -= 1
            elif event.key == SDLK_d:
                if maps.id + 1 >= maps.size():
                    maps.id = 0
                else:
                    maps.id += 1
            elif event.key == SDLK_RETURN:
                pFramework.push_state(game_play)
        elif event.type == SDL_QUIT:
            pFramework.quit()

def resume():
    pass

def pause():
    pass
