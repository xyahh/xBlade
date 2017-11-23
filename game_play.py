import pFramework
from pico2d import *

import main_menu
import map_select
import char_select

file_name = "Gameplay"
pause_game = None
p1, p2 = None, None

def enter():
    global pause_game, p1, p2
    p1 = load_image('Characters/p1.png')
    p2 = load_image('Characters/p2.png')
    pause_game = False

def exit(): pass

def update(frame_time):
    char_select.char1.update(frame_time)
    char_select.char2.update(frame_time)
    map_select.maps.update_objects()

def char_draw():
    char_select.char1.draw_sprite()
    p1.draw(char_select.char1.x, char_select.char1.y + char_select.Character.char[char_select.char1.id]
    ['spr'][char_select.char1.sprite_state]['h'])
    if main_menu.selected_option == 1:
        char_select.char2.draw_sprite()
        p2.draw(char_select.char2.x, char_select.char2.y + char_select.Character.char[char_select.char2.id]
        ['spr'][char_select.char2.sprite_state]['h'])

def draw(frame_time):
    clear_canvas()
    map_select.maps.draw(400, 300, 'map_img')
    map_select.maps.draw_objects()
    char_draw()
    update_canvas()

def handle_events(frame_time):
    global pause_game
    events = get_events()
    for event in events:
        char_select.char1.handle_events(frame_time, event, SDLK_a, SDLK_d, SDLK_w)
        if main_menu.selected_option == 1: char_select.char2.handle_events(frame_time, event, SDLK_LEFT, SDLK_RIGHT, SDLK_UP)
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                if pause_game: pause_game = False
                else: pause_game = True
        elif event.type == SDL_QUIT:
            pFramework.quit()

def pause(): pass


def resume(): pass




