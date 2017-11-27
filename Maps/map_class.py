from pico2d import *
file_name = "MapClass"


class Map:
    def init_map(self, map_name):
        maps_file = open('Maps/maps.txt', 'r')
        map_info = json.load(maps_file)
        maps_file.close()

        self.map = {}

        for name in map_info:
            if name == map_name:
                object_file = open(map_info[name]['objects'], 'r')
                object_info = json.load(object_file)
                object_file.close()

                self.map_objects = []
                for obj_name in object_info:
                    img = None
                    has_img = object_info[obj_name]['has_img']
                    if has_img: img = load_image(object_info[obj_name]['img'])
                    self.map_objects.append({"name": obj_name, "img": img, "has_img": has_img,
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
                                             "has_bbox": object_info[obj_name]['has_bbox'],
                                             "bounding_box": (object_info[obj_name]['bounding_box']['left'],
                                                               object_info[obj_name]['bounding_box']['top'],
                                                               object_info[obj_name]['bounding_box']['right'],
                                                               object_info[obj_name]['bounding_box']['bottom'])
                                             })
                    self.map = {"name": name,
                            "dsp_img": load_image(map_info[name]['dsp_img']),
                            "x": map_info[name]['x'],
                            "y": map_info[name]['y'],
                            "map_img": load_image(map_info[name]['map_img']),
                            "objects": self.map_objects}

    def init_spawn(self, map_name, num_of_players):
        spawn_file = open('Maps/spawn.txt', 'r')
        spawn_info = json.load(spawn_file)
        spawn_file.close()

        self.spawn = []
        
        for name in spawn_info:
            if name == map_name and len(spawn_info[name]) >= num_of_players:
                for i in spawn_info[name]:
                    self.spawn.append({"player_id": int(i),
                                       "x": spawn_info[name][i]['x'],
                                       "y": spawn_info[name][i]['y'],
                                       "state": spawn_info[name][i]['state'],
                                       "action": spawn_info[name][i]['action']})

    def __init__(self, map_name, num_of_players):
        self.init_map(map_name)
        self.init_spawn(map_name, num_of_players)

    def draw(self):
        self.map['map_img'].draw(self.map['x'], self.map['y'])
        for count in range(len(self.map['objects'])):
            if self.map['objects'][count]['has_img']:
                self.map['objects'][count]['img'].draw(self.map['objects'][count]['pos_x'], self.map['objects'][count]['pos_y'])

    def update(self, frame_time):
        for count in range(len(self.map_objects)):
            def reset():
                self.map_objects[count]['pos_x'] = self.map_objects[count]['start_x']
                self.map_objects[count]['pos_y'] = self.map_objects[count]['start_y']

            if self.map_objects[count]['has_img']:
                self.map_objects[count]['pos_x'] += self.map_objects[count]['dir_x']*frame_time
                self.map_objects[count]['pos_y'] += self.map_objects[count]['dir_y']*frame_time

                if (self.map_objects[count]['pos_x'] <= self.map_objects[count]['limit_x1'] and
                            self.map_objects[count]['dir_x'] < 0) or \
                        (self.map_objects[count]['pos_x'] >= self.map_objects[count]['limit_x2'] and
                        self.map_objects[count]['dir_x'] > 0):
                    if self.map_objects[count]['new']: reset()
                    else: self.map_objects[count]['dir_x'] *= self.map_objects[count]['factor_x']

                if (self.map_objects[count]['pos_y'] <= self.map_objects[count]['limit_y1'] and
                        self.map_objects[count]['dir_y'] < 0) \
                        or (self.map_objects[count]['pos_y'] >= self.map_objects[count]['limit_y2'] and
                        self.map_objects[count]['dir_y'] > 0):
                    if self.map_objects[count]['new']: reset()
                    else: self.map_objects[count]['dir_y'] *= self.map_objects[count]['factor_y']

    def get_name(self):
        return self.map[self.id]['name']

    def size(self):
        return len(self.map)


class MapSelect:
    def __init__(self):
        maps_file = open('Maps/maps.txt', 'r')
        map_info = json.load(maps_file)
        maps_file.close()
        self.map = []
        self.id = 0
        for name in map_info:
            self.map.append({"name": name, "dsp_img": load_image(map_info[name]['dsp_img'])})

    def draw(self, x, y):
        self.map[self.id]['dsp_img'].draw(x, y)

    def get_curr_map_name(self):
        return self.map[self.id]['name']

    def handle_events(self, event, left_key, right_key):
        if event.key == left_key:
            if self.id == 0: self.id = len(self.map) -1
            else: self.id -= 1
        if event.key == right_key:
            if self.id == len(self.map)-1: self.id = 0
            else: self.id += 1