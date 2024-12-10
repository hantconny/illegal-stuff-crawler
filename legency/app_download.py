"""
下载图片视频资源
下载原始响应json，检查到底是删帖还是限时快拍（24小时后消失）
"""
import glob
import json
import subprocess
from urllib.parse import urlsplit

import requests
from jsonpath import jsonpath
from loguru import logger

from selenium_utils import scroll_to_bottom, sleep, get_driver
from settings import *

# /home/rhino/sns/tiktok-crawler-YYYY-MM-DD_HH-mm-ss_ssssss.log
logger.add(os.path.join(DUMP_DIR, 'tiktok_crawler_{time:YYYYMMDD}.log'), rotation="50 MB", retention="3 days",
           compression="gz", enqueue=True)

driver = get_driver()

# 设置浏览器最大化，但是会导致该爬虫错误
driver.maximize_window()

# 下载图片视频
DOWNLOAD_RES = False

def go(url):
    item_list = []
    driver.get(url)
    # 在没有登录信息的情况下，大概率出现需要刷新的问题，所以直接刷新，修改为使用登录信息后，则不再需要改行代码
    # driver.refresh()

    retry = RETRY_LIMIT
    scroll = SCROLL_LIMIT

    if scroll > 15:
        raise Exception('Too large for tiktok!')

    while scroll > 0:
        scroll_to_bottom(driver)
        scroll -= 1
        sleep(retry)

    results = _get_log()

    for result in results:
        # 有时会因为加载问题导致实际上还有更多视频，但tk返回的响应中显示没有更多视频，遇到这种响应跳过避免解析报错
        if not jsonpath(json.loads(result['body']), 'itemList'):
            continue

        item_list.extend(json.loads(result['body'])['itemList'])

        if DOWNLOAD_RES:
            for item in json.loads(result['body'])['itemList']:
                video_id = item['id']

                # 如果已经有video_id开头的相关文件（即使不全），也不再对该video_id进行解析下载了，过多的调用tiktok的解析api，tiktok会拒绝链接
                if len(glob.glob(video_id + '*.*', root_dir=DUMP_DIR)) > 0:
                    continue

                parse_video_url = 'https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={video_id}'.format(
                    video_id=video_id)
                response = requests.get(parse_video_url).json()
                if jsonpath(item, '$..imagePost'):
                    # 对于多张图片的轮播帖，全部下载
                    for i, image_url in enumerate(response['aweme_list'][0]['image_post_info']['images']):
                        command = 'aria2c.exe "{url}" --dir={dir} -o {output}'.format(
                            url=image_url['owner_watermark_image']['url_list'][1],
                            dir=DUMP_DIR,
                            output='{video_id}_{index}.jpeg'.format(video_id=video_id, index=i))
                        subprocess.Popen(command, shell=True)
                else:
                    command = 'aria2c.exe "{url}" --dir={dir} -o {output}'.format(
                        url=response['aweme_list'][0]['video']['download_addr']['url_list'][0],
                        dir=DUMP_DIR,
                        output='{video_id}.mp4'.format(video_id=video_id))
                    subprocess.Popen(command, shell=True)

    # 增加json文件保存，看能不能找到限时快拍
    split_result = urlsplit(url)
    filename = '{ts}_{path}_{query}_original.json'.format(ts=TODAY,
                                                path=split_result.path.replace('/', '_'),
                                                query=split_result.query)

    with open(os.path.join(DUMP_DIR, filename), 'w', encoding='utf-8') as f:
        logger.debug("writing original json to file")
        f.writelines(json.dumps(item_list))

    logger.success('{} all done'.format(url))


def _get_log():
    logs_raw = sorted(driver.get_log("performance"), key=lambda x: x['timestamp'])
    logs = [json.loads(lr["message"])["message"] for lr in logs_raw]

    results = []

    for log in filter(
            lambda x: x['method'] == 'Network.responseReceived' and 'api/post/item_list' in x['params']['response'][
                'url'],
            logs):
        try:
            request_id = log["params"]["requestId"]
            results.append(driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id}))
        except Exception as s:
            logger.error(s)
            pass

    return results


if __name__ == '__main__':
    try:
        go(TARGET)
    finally:
        driver.close()
        driver.quit()
