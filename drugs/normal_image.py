# -*- coding:utf-8 -*-
from service.gettyimages_com import search_download_image


def go():
    keywords = ["vaccine", "medication", "pharmaceutical"]

    search_download_image(keywords)


if __name__ == '__main__':
    go()
