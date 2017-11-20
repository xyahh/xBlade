from pico2d import *
name = "MapClass"

class Map:
    def __init__(self):
        self.id = 0
        maps_file = open('Map/maps.txt', 'r')
        map_info= json.load(maps_file)
        maps_file.close()
        self.map = []
        for name in map_info:
            self.map.append({"name": name, "dsp_img": load_image(map_info[name]['dsp_img']), "map_img": load_image(map_info[name]['map_img'])})

    def draw(self, x, y, string):
        self.map[self.id][string].draw(x, y)

    def getName(self):
        return self.map[self.id]['name']

    def size(self):
        return len(self.map)