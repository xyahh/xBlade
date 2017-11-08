import pFramework
from pico2d import *

name = "MapSelect"
back_img, map_sel = None, None

def enter():
    global back_img, map_sel
    back_img = load_image('Map/sel_back.png')
    map_sel = load_image('Map/map_sel.png')

def exit():
    global back_img, map_sel
    del(back_img, map_sel)

def update():
    pass

def draw():
    clear_canvas()
    back_img.draw(400, 300)
    map_sel.draw(400, 550)
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            pFramework.pop_state()
        elif event.type == SDL_QUIT:
            pFramework.quit()

def resume():
    pass

def pause():
    pass
