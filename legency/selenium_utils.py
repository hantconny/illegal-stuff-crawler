# -*- coding:utf-8 -*-

from selenium import webdriver

from settings import *


def get_driver():
    chrome_options = webdriver.ChromeOptions()
    # 指定绑定版本的chrome浏览器，防止主机的chrome浏览器升级后与chromedriver不匹配导致失败
    chrome_options.binary_location = CHROME_TEST

    """capability选项"""
    # 开启chrome的性能日志
    chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

    """experimental选项"""
    # 开关配置
    # 禁止弹出窗口，禁止chrome正受到自动测试软件的控制
    exclude_switches = ['disable-popup-blocking', 'enable-automation']
    chrome_options.add_experimental_option('excludeSwitches', exclude_switches)

    """argument选项"""
    # 通过bot.sannysoft.com的反bot测试
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    # 设置语言为英语，因为要查找英语内容，如不设置有时会变为中文，导致内容查找失败
    chrome_options.add_argument('--lang=en-US')
    # 在容器化（docker）、低内存环境中使用该选项降低对内存的消耗
    chrome_options.add_argument('--disable-dev-shm-usage')
    # 一个奇怪的错误，启动时chrome即奔溃，但在海外win-server机器上正常，需要加上该参数才能在本地win-10机器上正常运行
    chrome_options.add_argument('--no-sandbox')
    # 可以添加headless称为无头浏览器（不启动界面）
    # chrome_options.add_argument('--headless')
    # 使用已经保存了登录信息的用户目录，避免每次运行都需要进行登录或刷新绕过登录弹窗，但是需要手动登录一次才能在该目录下保存登录信息
    if LOGIN:
        chrome_options.add_argument("--user-data-dir={user_data_dir}".format(user_data_dir=CHROME_USER_DATA_DIR))
    # 国内应用VPN代理
    if PROXY_ENABLED:
        chrome_options.add_argument('--proxy-server={}'.format(HTTP_PROXY))

    driver = webdriver.Chrome(options=chrome_options)

    return driver


def scroll_to_bottom(driver_):
    """
    滑动到页面底部
    :param driver_:
    :return:
    """
    execute_script(driver_, 'window.scrollTo(0, document.documentElement.scrollHeight)')


def scroll_fix_pixel(driver_, fix_pix_: str):
    """
    向下滑动固定像素
    :param driver_:
    :param fix_pix_:
    :return:
    """
    cmd = 'window.scrollBy(0, {pixel})'.format(pixel=fix_pix_)
    execute_script(driver_, cmd)


def execute_script(driver_, cmd_):
    """
    执行特定js
    :param driver_:
    :param cmd_:
    :return:
    """
    return driver_.execute_script(cmd_)


def sleep(seconds_):
    """
    等待 n 秒
    :param seconds_:
    :return:
    """
    time.sleep(seconds_)
