import pFramework
from pico2d import *

import game_play

name = "MainMenu"
title_img, border_img, xyah_txt, menu_txt = None, None, None, None
options = []
time = 0
selected_option = 0
show_menu = False

def enter():
    global title_img, side_img, background_img, border_img
    global xyah_txt, menu_txt
    global options, main_theme
    title_img = load_image('Menu/Title.png')
    border_img = load_image('Menu/border.png')
    background_img = load_image('Menu/menu_back.png')
    xyah_txt, menu_txt = load_font('Menu/lotr_font.ttf', 15), load_font('Menu/lotr_font.ttf', 30)
    options.append("Solo Play")
    options.append("P v P")
    options.append("Exit")

def exit():
    del(title_img, background_img, border_img, xyah_txt, menu_txt, options, main_theme)
    close_canvas()

def update():
    global time
    time += 1
    delay(0.01)

def drawMenu():
    border_img.draw(200, 110)
    count = 0
    for i in options:
        menu_txt.draw(100, 200 - (count * 70), i)
        count += 1
    draw_rectangle(80, 230 - (selected_option * 70), 325, 170 - (selected_option * 70))

def draw():
    clear_canvas()
    background_img.draw(400, 300)
    title_img.draw(400, 400)
    xyah_txt.draw(180, 500, 'XYAH ENTERTAINMENT PRESENTS')
    if show_menu: drawMenu()
    elif time%100 > 50: menu_txt.draw(180, 200, 'Press Enter to Start')
    update_canvas()


def handle_events():
    global selected_option
    global show_menu
    events = get_events()
    for event in events:
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            selected_option-=1
            if(selected_option<0): selected_option=2
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            selected_option += 1
            if (selected_option > 2): selected_option = 0
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RETURN):
            if show_menu:
                if selected_option==0:
                    pass
                elif selected_option==1:
                    pass
                elif selected_option==2:
                    pFramework.quit()
            else: show_menu = True
        elif event.type==SDL_QUIT:
            pFramework.quit()




def pause(): pass


def resume(): pass




