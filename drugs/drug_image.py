# -*- coding:utf-8 -*-
from service.gettyimages_com import search_download_image


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

    search_download_image(keywords, 5)


if __name__ == '__main__':
    go()
