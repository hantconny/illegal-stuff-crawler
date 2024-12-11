# -*- coding:utf-8 -*-

from service.gettyimages_com import search_download_video


def go():
    keywords = [
        "Cocaine",
        "Heroin",
        "Marijuana",
        "Methamphetamine",
        "Opium",
        "Oxicodona",
        "Oxycodone"
    ]
    search_download_video(keywords, 5)


if __name__ == '__main__':
    go()
