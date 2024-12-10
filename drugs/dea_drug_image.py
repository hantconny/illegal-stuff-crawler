# -*- coding:utf-8 -*-
import os
import time

from DrissionPage import ChromiumPage

from settings import DUMP_DIR


def go():
    url_pattern = "https://www.dea.gov/factsheets?page={}"

    driver = ChromiumPage()

    for i in range(4):
        url = url_pattern.format(i)

        driver.get(url)

        # 毒品名
        drug_categories = driver.eles(".teaser__heading")

        for drug_category in drug_categories:
            detail_page_url = drug_category.ele("tag:a").attr("href")

            drug_name = drug_category.text

            output_dir = os.path.join(DUMP_DIR, "dea", "image", drug_name)

            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # 在新tab页打开毒品详情
            detail_tab = driver.new_tab(detail_page_url)

            # 图片列表容器
            images_box = detail_tab.ele(".field__items")

            if images_box:
                # 如果有该元素，取该元素下的所有图片

                # 缩略图列表
                images = [div.ele("tag:img") for div in images_box.eles(".text-image__image") if div.ele("tag:img")]

                # 大图列表
                a_links = images_box.eles(".media-gallery-img-download-link")

                # 两个列表要大小一致才能进行拉链表迭代
                if len(images) == len(a_links):
                    for num, (image, alink) in enumerate(zip(images, a_links), start=1):
                        download_link = alink.attr("href")
                        # 图片是懒加载的，要滚动到可视区域
                        alink.scroll.to_see()
                        _, ext = os.path.splitext(download_link)
                        output_name = "{}_{}{}".format(drug_name, num, ext)

                        # 任务中断重新执行时不要重新下载
                        if os.path.exists(os.path.join(output_dir, output_name)):
                            continue

                        # 将大图链接设置到缩略图上，利用缩略图的img元素执行save()方法
                        image.set.attr("src", download_link)
                        image.save(path=output_dir, name=output_name, rename=False)

                        # 防封
                        time.sleep(3)
            else:
                # 如果没有，则取标题图
                image = detail_tab.ele(".media-caption__media").ele("tag:img")
                _, ext = os.path.splitext(image.attr("src"))
                output_name = "{}_{}{}".format(drug_name, "1", ext)
                image.save(path=output_dir, name=output_name, rename=False)

            detail_tab.close()

    driver.close()


if __name__ == '__main__':
    go()
