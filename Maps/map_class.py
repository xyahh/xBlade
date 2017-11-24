from pico2d import *
file_name = "MapClass"


class Map:
    def __init__(self):
        self.id = 0
        maps_file = open('Maps/maps.txt', 'r')
        map_info= json.load(maps_file)
        maps_file.close()
        self.map = []
        self.objects = []
        for name in map_info:
            self.map.append({"name": name, "dsp_img": load_image(map_info[name]['dsp_img']),
                             "map_img": load_image(map_info[name]['map_img'])})
            object_file = open(map_info[name]['objects'], 'r')
            object_info = json.load(object_file)
            object_file.close()
            for obj_name in object_info:
                self.objects.append({"name": obj_name, "img": load_image(object_info[obj_name]['img']),
                                     "start_x": object_info[obj_name]['start_x'],
                                     "start_y": object_info[obj_name]['start_y'],
                                     "pos_x": object_info[obj_name]['start_x'],
                                     "pos_y": object_info[obj_name]['start_y'],
                                     "dir_x": object_info[obj_name]['dir_x'],
                                     "dir_y": object_info[obj_name]['dir_y'],
                                     "limit_x1": object_info[obj_name]['limit_x1'],
                                     "limit_y1": object_info[obj_name]['limit_y1'],
                                     "limit_x2": object_info[obj_name]['limit_x2'],
                                     "limit_y2": object_info[obj_name]['limit_y2'],
                                     "new": object_info[obj_name]['new'],
                                     "factor_x": object_info[obj_name]['factor_x'],
                                     "factor_y": object_info[obj_name]['factor_y'],
                                     })

    def draw(self, x, y, string):
        self.map[self.id][string].draw(x, y)
        for count in range(len(self.objects)):
            self.objects[count]['img'].draw(self.objects[count]['pos_x'], self.objects[count]['pos_y'])

    def update(self):
        for count in range(len(self.objects)):
            def reset():
                self.objects[count]['pos_x'] = self.objects[count]['start_x']
                self.objects[count]['pos_y'] = self.objects[count]['start_y']

            self.objects[count]['pos_x'] += self.objects[count]['dir_x']
            self.objects[count]['pos_y'] += self.objects[count]['dir_y']

            if self.objects[count]['pos_x'] <= self.objects[count]['limit_x1'] or self.objects[count]['pos_x'] >= self.objects[count]['limit_x2']:
                if self.objects[count]['new']: reset()
                else: self.objects[count]['dir_x'] *= self.objects[count]['factor_x']

            if self.objects[count]['pos_y'] <= self.objects[count]['limit_y1'] or self.objects[count]['pos_y'] >= self.objects[count]['limit_y2']:
                if self.objects[count]['new']: reset()
                else: self.objects[count]['dir_y'] *= self.objects[count]['factor_y']

    def get_name(self):
        return self.map[self.id]['name']

    def size(self):
        return len(self.map)