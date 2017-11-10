import pFramework
from pico2d import *

import main_menu
import char_select

name = "MapSelect"
back_img, map_sel = None, None
border_img = None
maps = []
selected_map = 0
gen_txt = None

def enter():
    global back_img, map_sel, gen_txt, maps, selected_map, border_img
    selected_map = 0
    maps = []
    back_img = load_image('Map/sel_back.png')
    border_img = load_image('Map/map_border.png')
    map_sel = load_image('Map/map_sel.png')
    gen_txt = load_font('Menu/lotr_font.ttf')
    maps.append({'name': 'Airship Battle', 'img': load_image('Map/airship_battle.png')})
    maps.append({'name': 'The Duel Hall', 'img': load_image('Map/duel_hall.png')})
    maps.append({'name': 'The Mysterious Forest', 'img': load_image('Map/mysterious_forest.png')})
    maps.append({'name': 'Game Center', 'img': load_image('Map/game_center.png')})


def exit():
    global back_img, map_sel, gen_txt, maps, border_img
    del(back_img, map_sel, gen_txt, maps, border_img)

def update():
    pass

def draw():
    clear_canvas()
    back_img.draw(400, 300)
    map_sel.draw(400, 550)
    gen_txt.draw(200, 450, char_select.chars[char_select.selected_char]['name'])
    gen_txt.draw(385, 450, 'vs')
    if main_menu.selected_option==1: gen_txt.draw(450, 450, char_select.chars[char_select.selected_char2]['name'])
    else: gen_txt.draw(450, 450, 'CPU')

    maps[selected_map]['img'].draw(400, 250)
    gen_txt.draw(200, 70, maps[selected_map]['name'], (255, 255, 255))
    border_img.draw(400, 250)
    update_canvas()

def handle_events():
    global selected_map
    events = get_events()
    for event in events:
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            pFramework.pop_state()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_a):
            if selected_map-1 < 0: selected_map = len(maps) - 1
            else: selected_map -=1
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_d):
            if selected_map + 1 >= len(maps): selected_map = 0
            else: selected_map += 1
        elif event.type == SDL_QUIT:
            pFramework.quit()

def resume():
    pass

def pause():
    pass
