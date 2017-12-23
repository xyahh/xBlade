from pico2d import *

from Characters.char_class import Character
from Results import results
from Maps.map_class import Map
from General import pFramework
from Sound import sound_manager as sound
from General import key_mapping as key
from General.bounding_box import BoundingBox
from Maps import map_select
from Menu import main_menu
from Characters import char_select

file_name = "Gameplay"
pause_game = None
char, map = None, None
winner = None
boxes = None
show_boxes = False


def enter():
    global char, map, boxes
    char = []
    map = Map(map_select.map_sel.get_curr_map_name(), main_menu.num_of_players)
    for i in range(main_menu.num_of_players):
        name = char_select.char_sel.chars[char_select.char_sel.player_choice[i]]['name']
        char.append(Character(name, map.spawn[i]['player_id'], map.spawn[i]['x'],
                              map.spawn[i]['y'], map.spawn[i]['state'], map.spawn[i]['action']))

    if main_menu.num_of_players == 1:
        name = char_select.char_sel.chars[char_select.char_sel.player_choice[0]-1]['name']
        char.append(Character(name, 0, map.spawn[1]['x'],
                              map.spawn[1]['y'], map.spawn[1]['state'], map.spawn[1]['action']))
    boxes = BoundingBox(char, map)


def exit():
    pass


def update(frame_time):
    global winner
    map.update(frame_time)
    alive = []
    for i in range(len(char)):
        if not char[i].update(frame_time, boxes):
            alive.append(i)

    boxes.update()

    if len(alive) == 1 and main_menu.num_of_players > 1:
        winner = char[alive[0]]
        pFramework.push_state(results)
        sound.play("victory")
        sound.stop(map_select.map_sel.get_curr_map_theme())


def draw(frame_time):
    clear_canvas()
    map.draw()
    for i in range(len(char)):
        char[-i-1].draw()  # reversed drawing. Player 1 drawn at the top
    if show_boxes:
        boxes.draw()
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
                                      key.controls[i]['ability1'], key.controls[i]['ability2'])
            if event.key == key.controls[i]['pause']:
                sound.play("back")
                sound.stop(map_select.map_sel.get_curr_map_theme())
                pFramework.pop_state()
                sound.play("main")

        if event.key == SDLK_F1 and event.type == SDL_KEYDOWN:
            if show_boxes:
                show_boxes = False
            else:
                show_boxes = True
        if event.type == SDL_QUIT:
            pFramework.quit()


def pause():
    pass


def resume():
    pass




