from pico2d import *

from Characters.char_class import Character
from Maps.map_class import Map
from General import pFramework
from General import key_mapping as key
from General.bounding_box import  BoundingBox
from Maps import map_select
from Menu import main_menu
from Characters import char_select

file_name = "Gameplay"
pause_game = None
char, map = None, None
boxes = None
show_boxes = False


def init_map_and_chars():
    global char, map, boxes
    char = []
    map = Map(map_select.map_sel.get_curr_map_name(), main_menu.num_of_players)
    for i in range(main_menu.num_of_players):
        name = char_select.char_sel.chars[char_select.char_sel.player_choice[i]]['name']
        char.append(Character(name, map.spawn[i]['player_id'], map.spawn[i]['x'],
                              map.spawn[i]['y'], map.spawn[i]['state'], map.spawn[i]['action']))
    boxes = BoundingBox(char, map)


def enter():
   init_map_and_chars()

def exit(): pass


def update(frame_time):
    map.update(frame_time)
    for i in range(len(char)):
        char[i].update(frame_time, boxes)
    boxes.update()


def draw(frame_time):
    clear_canvas()
    map.draw()
    for i in range(len(char)):
        char[len(char)-i-1].draw()  # reversed drawing. Player 1 drawn at the top
    if show_boxes: boxes.draw()
    #boxes.draw()
    update_canvas()


def handle_events(frame_time):
    global show_boxes
    events = get_events()
    for event in events:
        for i in range(len(key.controls)):
            if i < main_menu.num_of_players:
                char[i].handle_events(frame_time, event, key.controls[i]['player_id'],
                                      key.controls[i]['left'], key.controls[i]['right'],
                                      key.controls[i]['up'], key.controls[i]['down'],
                                      key.controls[i]['attack1'])
            if event.key == key.controls[i]['pause']:
                pFramework.pop_state()

        if event.key == SDLK_F1 and event.type == SDL_KEYDOWN:
            if show_boxes: show_boxes = False
            else: show_boxes = True
        if event.type == SDL_QUIT:
            pFramework.quit()


def pause(): pass


def resume(): pass




