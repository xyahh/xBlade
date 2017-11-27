from pico2d import *

from Characters.char_class import Character
from Maps.map_class import Map
from General import pFramework, key_mapping
from General.bounding_box import  BoundingBox
from Maps import map_select
from Menu import main_menu
from Characters import char_select

file_name = "Gameplay"
pause_game, controls = None, None
char, map = None, None
boxes = None

def init_controls():
    global controls
    control_file = open('General/controls.txt', 'r')
    control_info = json.load(control_file)
    control_file.close()

    controls = []
    for id in control_info:
        if int(id) <= main_menu.num_of_players:
            controls.append({"player_id":int(id),
                             "left":  key_mapping.map_key(control_info[id]['left']),
                             "right": key_mapping.map_key(control_info[id]['right']),
                             "up": key_mapping.map_key(control_info[id]['up']),
                             "pause": key_mapping.map_key(control_info[id]['pause']),
                             "submit": key_mapping.map_key(control_info[id]['submit'])})


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
   init_controls()


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
    update_canvas()


def handle_events(frame_time):
    events = get_events()
    for event in events:
        for i in range(len(controls)):
            char[i].handle_events(frame_time, event, controls[i]['player_id'],
                                  controls[i]['left'], controls[i]['right'], controls[i]['up'])
        if event.type == SDL_QUIT:
            pFramework.quit()


def pause(): pass


def resume(): pass




