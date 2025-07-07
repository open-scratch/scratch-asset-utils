import json
import os
import requests

pretend = False
downloaded = set()

# 这里替换成你的代理服务器
proxies = {
    'http': 'socks5h://127.0.0.1:10808',
    'https': 'socks5h://127.0.0.1:10808'
}

def download_file(url, path):
    if os.path.exists(path):
        print("skip:" + path)
        return
    floder = "/".join(path.split("/")[0:-1])
    if not os.path.exists(floder):
        os.makedirs(floder)
    print("downloading:" + url)
    res = requests.get(url, proxies=None)
    if path in downloaded:
        return None
    if res.status_code == 200:
        print("download ok:" + path)
        with open(path, "wb") as f:
            f.write(res.content)
            downloaded.add(path)
            return res.content
    else:
        return None


def download_media(json_path):
    if not json_path: return None
    media_url = "https://xxx/svglibrary/%s"
    cover_url = "https://xxx/pnglibrary/%s"
    download_path_media = "svglibrary/"
    download_path_cover = "pnglibrary/"

    with open(json_path, "r", encoding="utf8") as f:
        media = json.load(f)
        backgrounds = media.get("backgrounds", {})
        sprites = media.get("sprites", {})
        for m in backgrounds:
            print("download background:" + m['md5'])
            res = download_file(media_url % m['md5'], download_path_media + m['md5'])
            res = download_file((cover_url % m['md5']).replace("svg", "png"), download_path_cover + m['md5'].replace("svg", "png"))
        for m in sprites:
            print("download sprite:" + m['md5'])
            res = download_file(media_url % m['md5'], download_path_media + m['md5'])
            res = download_file((cover_url % m['md5']).replace("svg", "png"), download_path_cover + m['md5'].replace("svg", "png"))
            if 'pose' in m:
                poses = m['pose'].split(';')
                for pose in poses:
                    print("download sprite:pose:" + pose)
                    res = download_file(media_url % pose, download_path_media + pose)
                    res = download_file((cover_url % pose).replace("svg", "png"), download_path_cover + pose.replace("svg", "png"))


# 下载
download_media("media.json")

print("download finished")
