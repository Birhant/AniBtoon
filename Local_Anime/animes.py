import os
import re

def dict_to_list(dict_file):
    list_file = []
    keys = list(dict_file.keys())
    for key in keys:
        value = dict_file[key]
        list_file.append((key, value))
    return list_file

def order(key):
    key_list = list(key)
    numbers = ''
    start = False
    for i in reversed(key_list):
        if i=='.':
            start = True
        else:
            if start:
                if i.isdigit():
                    numbers = i+numbers
                else:
                    break
    numbers = int(numbers)
    return numbers

class Anime_files:
    def __init__(self, path):
        self.anime_tree = {}
        self.get_episodes(path)
        self.anime = {}
        self.catalogue()
        self.anime_list = dict_to_list(self.anime)

    def get_episodes(self, path):
        dirs = os.listdir(path)
        series = []
        for dir in dirs:
            path_dir = os.path.join(path, dir)
            if os.path.isdir(path_dir):
                self.get_episodes(path_dir)
            if os.path.isfile(path_dir):
                if self.valid_episode(dir):
                    series.append(dir)
        series.sort(key = order)
        _, dir_name = os.path.split(path)
        if len(series)>0:
            info = (path, series)
            self.anime_tree[dir_name] = info

    def valid_episode(self, episode_name):
        match = re.match('.*\.(mp4|ts|mkv)', episode_name)
        if match is not None:
            status = True
        else:
            status = False
        return status

    def append_to_anime(self, key, value):
        if key in list(self.anime.keys()):
            self.anime[key].append(value)
        else:
            self.anime[key] = [value]

    def catalogue(self):
        for key in list(self.anime_tree.keys()):
            value = self.anime_tree[key]
            match = re.match("Season ?(\d+)", key)
            if match is not None:
                base, _ = os.path.split(value[0])
                _, parent_name = os.path.split(base)
                self.append_to_anime(parent_name, value)
            else:
                self.append_to_anime(key, value)

