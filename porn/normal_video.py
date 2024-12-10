# -*- coding:utf-8 -*-
from service.gettyimages_com import search_download_video


def go():
    keywords = ["supermodel", "swimsuit", "actress"]
    search_download_video(keywords)


if __name__ == '__main__':
    go()