import pFramework
from pico2d import *

import pyglet #3rd party audio player
from pyglet.media import Player
import char_select

name = "MainMenu"
title_img, border_img, xyah_txt, menu_txt = None, None, None, None
options = []
timer = 0
selected_option = 0
show_menu = False
song = None
player = None

def enter():
    global title_img, side_img, background_img, border_img, song, player
    global xyah_txt, menu_txt
    global options, main_theme
    title_img = load_image('Menu/Title.png')
    border_img = load_image('Menu/border.png')
    background_img = load_image('Menu/menu_back.png')
    xyah_txt, menu_txt = load_image('Menu/xyah_txt.png'), load_font('Menu/lotr_font.ttf', 30)

    options.append("Solo Play")
    options.append("P v P")
    options.append("Exit")

    song = pyglet.media.load('Menu/menu_theme.mp3')
    player = Player()
    player.queue(song)
    player.eos_action = player.EOS_LOOP
    player.play()


def exit():
    global title_img, background_img, border_img, xyah_txt, menu_txt, options
    del(title_img, background_img, border_img, xyah_txt, menu_txt, options)

def update(frame_time):
    global timer
    timer += 1
    delay(0.01)

def drawMenu():
    border_img.draw(400, 110)
    count = 0
    for i in options:
        menu_txt.draw(300, 200 - (count * 70), i)
        count += 1
    draw_rectangle(280, 230 - (selected_option * 70), 525, 170 - (selected_option * 70))

def draw(frame_time):
    clear_canvas()
    background_img.draw(400, 300)
    title_img.draw(400, 400)
    xyah_txt.draw(410, 500)
    if show_menu: drawMenu()
    elif timer%100 > 50: menu_txt.draw(180, 200, 'Press Enter to Start')
    update_canvas()


def handle_events(frame_time):
    global selected_option
    global show_menu
    events = get_events()
    for event in events:
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_w):
            selected_option-=1
            if(selected_option<0): selected_option=2
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_s):
            selected_option += 1
            if (selected_option > 2): selected_option = 0
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RETURN):
            if show_menu:
                if selected_option==0 or selected_option==1:
                    pFramework.push_state(char_select)
                elif selected_option==2:
                    pFramework.quit()
            else: show_menu = True
        elif event.type==SDL_QUIT:
            pFramework.quit()




def pause(): pass


def resume(): pass




