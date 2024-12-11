# -*- coding:utf-8 -*-
from service.gettyimages_com import search_download_video


def go():
    keywords = ["war", "terrorism"]
    search_download_video(keywords, 5)


if __name__ == '__main__':
    go()
