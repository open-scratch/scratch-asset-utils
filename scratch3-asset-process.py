# -*- coding: utf-8 -*-

import hashlib
import os
import wave
import contextlib
import shutil
import json

# scratch根目录 ， 一般只需要配置该路径
PRE = ""
# 资源路径
PATH_ASSET = PRE + "hemacode\\internalapi\\asset\\"
# 索引库目录
PRE_LIB = PRE + "hemacode\\json_index\\"
# 背景索引
LIB_BACKDROP = PRE_LIB + "backdrops.json"
# 造型索引
LIB_COSTUME = PRE_LIB + "costumes.json"
# 声音索引
LIB_SOUND = PRE_LIB + "sounds.json"
# 角色索引
LIB_SPRITE = PRE_LIB + "sprite.json"

if not os.path.exists(PATH_ASSET):
    print("资源目录配置不正确")
if not os.path.isfile(LIB_BACKDROP):
    with open(LIB_BACKDROP, 'w') as file:
        pass
    print("找不到背景索引文件")
if not os.path.isfile(LIB_COSTUME):
    with open(LIB_COSTUME, 'w') as file:
        pass
    print("找不到造型索引文件")
if not os.path.isfile(LIB_SOUND):
    with open(LIB_SOUND, 'w') as file:
        pass
    print("找不到声音索引文件")
if not os.path.isfile(LIB_SPRITE):
    with open(LIB_SPRITE, 'w') as file:
        pass
    print("找不到角色索引文件")


print("""
=========使用说明：==========
1.将本脚本放在scratch根目录，或配置资源目录的路径
2.拖入文件或文件夹
3.回车确认

资源类型说明：
角色文件：.sprite2
背景文件：.jpg
造型文件：.png、.svg
音频文件：.wav
===========================
""")


# 获取md5
def get_md5(file_path):
    md5 = None
    if os.path.isfile(file_path):
        with open(file_path, 'rb') as f:
            md5_obj = hashlib.md5()
            md5_obj.update(f.read())
        hash_code = md5_obj.hexdigest()
        md5 = str(hash_code).lower()
    return md5


class Push:
    def __init__(self, fullpath, name=""):
        self.fullpath = fullpath
        self.path, self.filename = os.path.split(fullpath)
        self.name, self.suffix = os.path.splitext(self.filename)
        self.suffix = self.suffix.split(".")[-1]
        if name != "": self.name = name

    def push_costume(self):
        print("处理造型:", self.name)
        md5 = get_md5(self.fullpath)
        md5_filename = md5 + "." + self.suffix
        shutil.copy(self.fullpath, PATH_ASSET + md5_filename)
        custume_obj = {"assetId": md5,
                    "name": self.name,
                    "md5ext": md5_filename,
                    "bitmapResolution": 1 if self.suffix == 'svg' else 2,
                    "dataFormat": self.suffix,
                    "rotationCenterX": 0,
                    "rotationCenterY": 0,
                     "tags": []}
        print(custume_obj)
        with open(LIB_COSTUME, 'r', encoding="utf-8") as f:
            text = f.read()
            text = '[]' if text == "" else text
            json_data = json.loads(text)
            json_data.insert(0, custume_obj)
        with open(LIB_COSTUME, 'w', encoding='utf-8') as f:
            text_data = '[\n'
            for j in json_data:
                text_data += json.dumps(j)
                text_data += ",\n"
            text_data = text_data[:-2]
            text_data += "\n]"
            f.write(text_data)

    def push_back(self):
        print("处理背景:", self.name)
        md5 = get_md5(self.fullpath)
        md5_filename = md5 + "." + self.suffix
        shutil.copy(self.fullpath, PATH_ASSET + md5_filename)
        back_obj = {"assetId": md5,
                    "name": self.name,
                    "md5ext": md5_filename,
                    "bitmapResolution": 1 if self.suffix == 'svg' else 2,
                    "dataFormat": self.suffix,
                    "rotationCenterX": 0,
                    "rotationCenterY": 0,
                     "tags": []}
        print(back_obj)
        with open(LIB_BACKDROP, 'r', encoding="utf-8") as f:
            text = f.read()
            text = '[]' if text == "" else text
            json_data = json.loads(text)
            json_data.insert(0, back_obj)
        with open(LIB_BACKDROP, 'w', encoding='utf-8') as f:
            text_data = '[\n'
            for j in json_data:
                text_data += json.dumps(j)
                text_data += ",\n"
            text_data = text_data[:-2]
            text_data += "\n]"
            f.write(text_data)

    def push_sound(self):
        print("处理声音:", self.name)
        md5 = get_md5(self.fullpath)
        md5_filename = md5 + "." + self.suffix

        # 计算音频时长
        duration = 0.00
        # with contextlib.closing(wave.open(self.fullpath, 'r')) as f:
        #     frames = f.getnframes()
        #     rate = f.getframerate()
        #     duration = frames / float(rate)
        # duration = round(duration, 3)
        shutil.copy(self.fullpath, PATH_ASSET + md5_filename)
        sound_obj = {"assetId": md5,
                     "name": self.name,
                     "md5ext": md5_filename,
                     "dataFormat": self.suffix,
                     "sampleCount": 0,
                     "rate": 0,
                     "tags": [],
                     }
        print(sound_obj)
        with open(LIB_SOUND, 'r', encoding="utf-8") as f:
            text = f.read()
            text = '[]' if text == "" else text
            json_data = json.loads(text)
            json_data.insert(0, sound_obj)
        with open(LIB_SOUND, 'w', encoding='utf-8') as f:
            text_data = '[\n'
            for j in json_data:
                text_data += json.dumps(j)
                text_data += ",\n"
            text_data = text_data[:-2]
            text_data += "\n]"
            f.write(text_data)

    def push(self):
        if self.suffix == "wav":
            self.push_sound()
        elif self.suffix == "jpg":
            self.push_back()
        elif self.suffix == "png" or self.suffix == "svg":
            self.push_costume()
        else:
            print("无法识别对应格式的文件")


while True:
    path = input("\n\n拖入文件或文件夹:\n")
    if os.path.isdir(path):
        path += "\\"
        input_type = input("输入该文件夹的类型：0.自动 1.背景   2.造型  3.声音\n")
        for lists in os.listdir(path):
            push = Push(path + lists)
            if input_type == "0":
                push.push()
            elif input_type == "1":
                push.push_back()
            elif input_type == "2":
                push.push_costume()
            elif input_type == "3":
                push.push_sound()
            else:
                push.push()
    else:
        path.replace("\"", "")
        filename_full = os.path.split(path)[1]
        file_name, file_suffix = os.path.splitext(filename_full)
        push = Push(path, file_name)
        push.push()
