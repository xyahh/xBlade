import pFramework
from pico2d import *

name = "MainMenu"
title_img = None
background_img = None
side_img = None
border_img = None
xyah_txt = None
options = []
menu_txt = None
main_theme = None
selected_option = 0

def enter():
    global title_img, side_img, background_img, border_img
    global xyah_txt, menu_txt
    global options
    global main_theme
    title_img = load_image('Title.png')
    side_img = load_image('ZXSaber.png')
    background_img = load_image('white_back.png')
    border_img = load_image('border.png')
    xyah_txt = load_font('lotr_font.ttf', 15)
    menu_txt = load_font('lotr_font.ttf', 30)
    main_theme = load_music('theme.mp3')
    #main_theme.play()
    options.append("Solo Play")
    options.append("P v P")
    options.append("Exit")

def exit():
    del(title_img)
    del(side_img)
    del(background_img)
    del(border_img)
    del(xyah_txt)
    del(menu_txt)
    del(options)
    del(main_theme)
    close_canvas()


def update():
    delay(0.01)


def draw():
    clear_canvas()
    background_img.draw(400, 300)
    side_img.draw(700, 200)
    border_img.draw(200, 200)
    title_img.draw(300, 470)
    xyah_txt.draw(70, 560, 'XYAH ENTERTAINMENT PRESENTS')
    count = 0
    for i in options:
        menu_txt.draw(100, 300-(count*100), i)
        count += 1
    draw_rectangle(80, 330-(selected_option*100), 325, 270-(selected_option*100))
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            selected_option-=1
            if(selected_option<0): selected_option=2
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            selected_option += 1
            if (selected_option > 2): selected_option = 0
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RETURN):
            if selected_option==0:
                pass
            elif selected_option==1:
                pass
            elif selected_option==2:
                pFramework.quit()
        elif event.type==SDL_QUIT:
            pFramework.quit()




def pause(): pass


def resume(): pass




