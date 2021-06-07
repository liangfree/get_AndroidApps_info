# This is a main file to run process.
# by: liangfei
# time: 2021.05

import time
import datetime
from appium import webdriver

from caps import caps
from tools import *
from xpath import *


# HTTP链接地址
GLOBAL_WEBDRIVERHTTPLOC = 'http://127.0.0.1:4723/wd/hub'


# main:
if __name__ == '__main__':

    # ==== 微信 == start =============================================
    # 打开app
    # driver = webdriver.Remote(GLOBAL_WEBDRIVERHTTPLOC, caps['weixin'])

    # 打开app需要时间较长 最短3秒
    # time.sleep(5)

    # ---------------------------------------------------
    # 微信 任务一 抓取信息 最近聊天
    # result = do_xpath_unit(driver, xpath_weixin[0], 20, 10)
    # print_result(result, 3)

    # ---------------------------------------------------
    # 微信 任务二 抓取朋友圈信息
    # do_xpath_unit(driver, xpath_weixin[1])
    # time.sleep(0.5)
    # do_xpath_unit(driver, xpath_weixin[2])
    # time.sleep(0.5)
    # result = do_xpath_unit(driver, xpath_weixin[3], 5, 20)
    # print_result(result, 2)

    # ==== 微信 == end =============================================

    # ==== QQ == start =============================================
    # 打开app
    # driver = webdriver.Remote(GLOBAL_WEBDRIVERHTTPLOC, caps['qq'])

    # 打开app需要时间较长 最短3秒
    # time.sleep(5)

    # ---------------------------------------------------
    # QQ 抓取信息 最近聊天
    # do_xpath_unit(driver, xpath_qq[0])
    # time.sleep(0.5)
    # for _ in range(30):
    #     swipe_down(driver, 0.9)
    # result = do_xpath_unit(driver, xpath_qq[1], 20, 20)
    # print_result(result, 2)

    # ==== QQ == end =============================================

    # ==== 便签 == start =============================================
    # 打开app
    # driver = webdriver.Remote(GLOBAL_WEBDRIVERHTTPLOC, caps['bianqian'])

    # 打开app需要时间较长 最短3秒
    # time.sleep(3)

    # ---------------------------------------------------
    # 便签 获取便签
    # result = do_xpath_unit(driver, xpath_bianqian[0], 7, 10)
    # print_result(result, 2)

    # ==== 便签 == end =============================================

    # ==== 知乎 == start =============================================
    # 打开app
    driver = webdriver.Remote(GLOBAL_WEBDRIVERHTTPLOC, caps['zhihu'])

    # 打开app需要时间较长 最短3秒 开屏广告时间较长
    time.sleep(10)

    # ---------------------------------------------------
    # 点击推荐按钮
    do_xpath_unit(driver, xpath_zhihu[0])
    time.sleep(0.5)
    # 知乎 获取推荐首页
    result = do_xpath_unit(driver, xpath_zhihu[1], 7, 10)

    print(result)
    print_result(result, 4)

    # ==== 知乎 == end =============================================





