from pico2d import *
from General import pFramework
from Sound import sound_manager as sound
from General import key_mapping as key
from General import game_play

file_name = "Results"
images, font = None, None


def enter():
    global images, font

    media_file = open('Results/media.txt', 'r')
    media_info = json.load(media_file)
    media_file.close()

    font = load_font(media_info['font']['path'], media_info['font']['size'])

    images = []
    for name in media_info['images']:
        images.append({"img": load_image(media_info['images'][name]['path']),
                       "x": media_info['images'][name]['x'], "y": media_info['images'][name]['y']})


def exit():
    pass


def update(frame_time):
    pass


def draw(frame_time):
    clear_canvas()
    for i in range(len(images)):
        images[i]['img'].draw(images[i]['x'], images[i]['y'])
    game_play.winner.draw(images[i]['x'], images[i]['y'])
    update_canvas()


def handle_events(frame_time):
    events = get_events()
    for event in events:
        for i in range(len(key.controls)):
            if event.key in (key.controls[i]['pause'], key.controls[i]['submit']):
                sound.play("submit")
                sound.stop("victory")
                for j in range(4):
                    pFramework.pop_state()
                sound.play("main")
                break
        if event.type == SDL_QUIT:
            pFramework.quit()


def pause(): pass


def resume(): pass
