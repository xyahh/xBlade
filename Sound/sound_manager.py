from sdl2.sdlmixer import *

song_list = {}
CHANNEL_NUMBER = 16
Mix_AllocateChannels(CHANNEL_NUMBER)  # 16 sounds can be played at a time


def add(song_name, path, is_bgm=False):
    data = Mix_LoadWAV(path.encode('UTF-8'))
    if not data:
        print('cannot load %s' % path)
        return
    song_list.update({song_name: {"sound": data, "repeat": is_bgm}})


def delete(song_name):
    if song_name not in song_list:
        return
    song_list.pop(song_name, None)


def play(song_name, vol=70):
    if song_name not in song_list:
        return
    repeat = 0
    if song_list[song_name]['repeat']:
        repeat = -1
    for i in range(CHANNEL_NUMBER):
        if not Mix_Playing(i):
            Mix_Volume(i, vol)
            Mix_PlayChannel(i, song_list[song_name]['sound'], repeat)
            return

