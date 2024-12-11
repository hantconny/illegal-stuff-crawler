# -*- coding:utf-8 -*-
import os
import time

from DrissionPage import ChromiumPage
from tqdm import tqdm

from settings import DUMP_DIR, GETTYIMAGES_COM_VIDEO_URL_PATTERN, GETTYIMAGES_COM_IMAGE_URL_PATTERN


def search_download_video(keywords, pages=1):
    """
    从 gettyimages.com 搜索关键词并下载特定页数的视频
    :param keywords: 关键词列表 ['keyword 1', 'keyword 2', 'keyword 3']
    :param pages: 需要下载的总页数
    :return: None
    """
    driver = ChromiumPage()

    for keyword in keywords:
        keyword = str.lower(keyword)

        output_dir = os.path.join(DUMP_DIR, "gettyimages_com", "video", keyword)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_dir = os.path.abspath(output_dir)

        driver.get(GETTYIMAGES_COM_VIDEO_URL_PATTERN.format(keyword))

        # 切换为固定列模式，默认模式无法加载视频
        driver.ele("@data-testid=gallery-grid-toggle-fixed").click()

        total_page = int(driver.ele("@name=page").next().text)

        if pages > total_page:
            pages = total_page

        driver.download.set.save_path(output_dir)

        for i in range(1, pages + 1):
            # 避免取到网站logo等无关图片
            images = driver.ele("@data-testid=galleryContainer").eles("tag:img")

            for image in tqdm(images, desc="分析中"):
                # 悬停以加载 <video> 标签
                image.hover()
                time.sleep(2)

            videos = driver.ele("@data-testid=galleryContainer").eles("tag:video")

            for num, video in enumerate(videos, start=1):
                video_url = video.attr("src")
                _, ext = os.path.splitext(video_url)
                output_name = "{keyword}_{page}_{num}{ext}".format(keyword=keyword,
                                                                   page=str.zfill(str(i), 3),
                                                                   num=str.zfill(str(num), 3),
                                                                   ext=ext.split("?")[0])

                # 任务中断重新执行时不要重新下载
                if os.path.exists(os.path.join(output_dir, output_name)):
                    continue

                driver.download(video_url, rename=output_name)

                time.sleep(3)

            driver.ele("@data-testid=pagination-button-next").click()

    driver.close()


def search_download_image(keywords, pages=1):
    """
    从 gettyimages.com 搜索关键词并下载特定页数的图片
    :param keywords: 关键词列表 ['keyword 1', 'keyword 2', 'keyword 3']
    :param pages: 需要下载的总页数
    :return: None
    """
    driver = ChromiumPage()

    for keyword in keywords:
        keyword = str.lower(keyword)

        output_dir = os.path.join(DUMP_DIR, "gettyimages_com", "image", keyword)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_dir = os.path.abspath(output_dir)

        driver.get(GETTYIMAGES_COM_IMAGE_URL_PATTERN.format(keyword))

        # 切换为固定列模式，默认模式无法加载视频
        driver.ele("@data-testid=gallery-grid-toggle-fixed").click()

        total_page = int(driver.ele("@name=page").next().text)

        if pages > total_page:
            pages = total_page

        driver.download.set.save_path(output_dir)

        for i in range(1, pages + 1):
            # 避免取到网站logo等无关图片
            images = driver.ele("@data-testid=galleryContainer").eles("tag:img")

            for num, image in enumerate(images, start=1):
                image_url = image.attr("src")
                _, ext = os.path.splitext(image_url)
                output_name = "{keyword}_{page}_{num}{ext}".format(keyword=keyword,
                                                                   page=str.zfill(str(i), 3),
                                                                   num=str.zfill(str(num), 3),
                                                                   ext=ext.split("?")[0])

                # 任务中断重新执行时不要重新下载
                if os.path.exists(os.path.join(output_dir, output_name)):
                    continue

                driver.download(image_url, rename=output_name)

                time.sleep(3)

            driver.ele("@data-testid=pagination-button-next").click()

    driver.close()
