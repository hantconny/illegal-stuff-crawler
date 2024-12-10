# -*- coding:utf-8 -*-
import os
import time

from DrissionPage import ChromiumPage

from settings import DUMP_DIR, GETTYIMAGES_COM_VIDEO_URL_PATTERN, GETTYIMAGES_COM_IMAGE_URL_PATTERN


def search_download_video(keywords):
    driver = ChromiumPage()

    for keyword in keywords:
        keyword = str.lower(keyword)

        output_dir = os.path.join(DUMP_DIR, "gettyimages_com", "video", keyword)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_dir = os.path.abspath(output_dir)

        driver.get(GETTYIMAGES_COM_VIDEO_URL_PATTERN.format(keyword))

        driver.download.set.save_path(output_dir)

        images = driver.eles("tag:img")

        for image in images:
            # 悬停以加载 <video> 标签
            image.hover()
            time.sleep(2)

        videos = driver.eles("tag:video")

        for num, video in enumerate(videos, start=1):
            video_url = video.attr("src")
            _, ext = os.path.splitext(video_url)
            output_name = "{keyword}_{num}{ext}".format(keyword=keyword,
                                                        num=num,
                                                        ext=ext.split("?")[0])

            # 任务中断重新执行时不要重新下载
            if os.path.exists(os.path.join(output_dir, output_name)):
                continue

            driver.download(video_url, rename=output_name)

            time.sleep(3)

    driver.close()


def search_download_image(keywords):
    driver = ChromiumPage()

    for keyword in keywords:
        keyword = str.lower(keyword)

        output_dir = os.path.join(DUMP_DIR, "gettyimages_com", "image", keyword)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_dir = os.path.abspath(output_dir)

        driver.get(GETTYIMAGES_COM_IMAGE_URL_PATTERN.format(keyword))

        driver.download.set.save_path(output_dir)

        images = driver.eles("tag:img")

        for num, image in enumerate(images, start=1):
            image_url = image.attr("src")
            _, ext = os.path.splitext(image_url)
            output_name = "{keyword}_{num}{ext}".format(keyword=keyword,
                                                        num=num,
                                                        ext=ext.split("?")[0])

            # 任务中断重新执行时不要重新下载
            if os.path.exists(os.path.join(output_dir, output_name)):
                continue

            driver.download(image_url, rename=output_name)

            time.sleep(3)

    driver.close()
