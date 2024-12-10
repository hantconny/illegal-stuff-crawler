import os.path
import time

"""
命名规则为/home/rhino/{project}/{sub-proj}
project可选值为: ip, sns, tor, illegal
sub-proj可选值为: 
  ip: v4, v6
  sns: fb, tw, ut, ins, tk, vk
  tor: 直接存放
  illegal: gettyimages_com
"""
DUMP_DIR = 'D:/home/rhino/illegal'
if not os.path.exists(DUMP_DIR):
    os.makedirs(DUMP_DIR)

# gettyimages.com 视频综合搜索
GETTYIMAGES_COM_VIDEO_URL_PATTERN = "https://www.gettyimages.com/search/2/film?phrase={}"

# gettyimages.com 图片综合搜索
GETTYIMAGES_COM_IMAGE_URL_PATTERN = "https://www.gettyimages.com/search/2/image?phrase={}"

# # 20231202
# TODAY = time.strftime('%Y%m%d', time.localtime())
# # Chrome测试版解压位置，不要与客户机使用相同的Chrome
# CHROME_TEST = 'D:/ENV/chromedriver/chrome-win64/chrome.exe'
# # 保存登录信息，指定为一个非用户使用Chrome的目录，一般指定在爬虫输出目录同级
# CHROME_USER_DATA_DIR = 'D:/home/rhino/chrome'
#
# PROXY_ENABLED = True
#
# RETRY_LIMIT = 5
# # 向下滚动的次数
# SCROLL_LIMIT = 5
#
# APP_TYPE = 'illegal'
#
# # OWLS设控文件输出目录 20240102.text
# OWLS_TARGET_DIR = 'D:/home/rhino/snsMapping/accountInfo'
#
# HTTP_PROXY_CONFIG = {
#     'HOST': '127.0.0.1',
#     'PORT': '7890'
# }
#
# HTTP_PROXY = {
#     'http': '{host}:{port}'.format(host=HTTP_PROXY_CONFIG['HOST'], port=HTTP_PROXY_CONFIG['PORT']),
#     'https': '{host}:{port}'.format(host=HTTP_PROXY_CONFIG['HOST'], port=HTTP_PROXY_CONFIG['PORT'])
# }
#
# CMD_PROXY = '{host}:{port}'.format(host=HTTP_PROXY_CONFIG['HOST'], port=HTTP_PROXY_CONFIG['PORT'])
#
# ARIA2C_PATH = r"D:\ENV\aria2-1.35.0-win-64bit-build1\aria2c.exe"
