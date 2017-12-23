from sdl2.sdlmixer import *

song_list = {}
CHANNEL_NUMBER = 16
Mix_AllocateChannels(CHANNEL_NUMBER)  # 16 sounds can be played at a time


def add(song_name, path, is_bgm=False):
    data = Mix_LoadWAV(path.encode('UTF-8'))
    if not data:
        print('cannot load %s' % path)
        return
    song_list.update({song_name: {"sound": data, "repeat": is_bgm, "channel": -1}})


def delete(song_name):
    if song_name not in song_list:
        return
    song_list.pop(song_name, None)


def delete_all():
    global song_list
    song_list.clear()
    del song_list


def play(song_name, vol=65):
    if song_name not in song_list:
        return
    repeat = 0
    if song_list[song_name]['repeat']:
        repeat = -1
    i = Mix_PlayChannel(-1, song_list[song_name]['sound'], repeat)
    Mix_Volume(i, vol)
    song_list[song_name]['channel'] = i


def stop(song_name):
    if song_name not in song_list or song_list[song_name]['channel'] == -1:
        return
    Mix_HaltChannel(song_list[song_name]['channel'])
    song_list[song_name]['channel'] = -1


def stop_bgms():
    for name in song_list:
        if song_list[name]['repeat']:
            stop(name)


def stop_all():
    for i in range(CHANNEL_NUMBER):
        if Mix_Playing(i):
            Mix_Pause(i)

