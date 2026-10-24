import os
from pathlib import Path

# from start.settings import BASE_DIR
import requests
import parsel
def spider_bing():
    r = requests.get(
        "https://cn.bing.com/HPImageArchive.aspx",
        params={"format": "js", "idx": 0, "n": 1, "mkt": "zh-CN"},
        timeout=10,
    )
    img = r.json()["images"][0]
    # urlbase 形如 /th?id=OHR.YellowstoneWolves_ZH-CN6767268961
    img_url = f"https://cn.bing.com{img['urlbase']}_UHD.jpg&pid=hp&w=2000"
    # print(img_url)
    img_data = requests.get(img_url).content
    BASE_DIR = Path(__file__).resolve().parent.parent
    # BASE_DIR工程化目录
    with open(BASE_DIR.joinpath(f'app/blog/static/imgs/bing.jpg'), "wb") as handler:
        handler.write(img_data)

if __name__ == "__main__":
    spider_bing()