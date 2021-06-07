# 工具函数集合


# 精确点击
# driver.tap([(100, 20), (100, 60), (100, 100)], 500)


# 上滑 手势从下至上 0.5为一整页
def swipe_up(driver, n=0.3):
    # tuple: 获取屏幕大小
    size = (driver.get_window_size()['width'], driver.get_window_size()['height'])
    # 定义滑动参数
    x = int(size[0] * 0.5)  # x坐标
    y1 = int(size[1] * 0.9)  # 起始y坐标
    y2 = int(size[1] * (0.9 - 0.9 * n))    # 终点y坐标
    # 执行动作
    driver.swipe(x, y1, x, y2)


# 下滑
def swipe_down(driver, n=0.3):
    # tuple: 获取屏幕大小
    size = (driver.get_window_size()['width'], driver.get_window_size()['height'])
    # 定义滑动参数
    x = int(size[0] * 0.5)  # x坐标
    y1 = int(size[1] * 0.2)  # 起始y坐标
    y2 = int(size[1] * (0.2 + 0.6 * n))    # 终点y坐标
    # 执行动作
    driver.swipe(x, y1, x, y2)


# 返回 实际为左右边缘滑动 只适用于部分边缘滑动返回的手机
def back(driver):
    # tuple: 获取屏幕大小
    size = (driver.get_window_size()['width'], driver.get_window_size()['height'])
    # 定义滑动参数
    x = int(size[0] * 0.3)  # x坐标
    y = int(size[1] * 0.5)  # 起始y坐标
    # 执行动作 屏幕边缘滑动返回
    driver.swipe(0, y, x, y)


# 判断当前页面driver内有无以type类型值为value的元素
# by:
#        'id' / 'xpath' / 'class' / 'link text' / 'partial link text'
#        'name' / 'tag name' / 'css selector'
# value: -str
def has_element(driver, by, value):
    flag = False
    try:
        if by == "id":
            driver.find_element_by_id(value)
        elif by == "xpath":
            driver.find_element_by_xpath(value)
        elif by == "class":
            driver.find_element_by_class_name(value)
        elif by == "link text":
            driver.find_element_by_link_text(value)
        elif by == "partial link text":
            driver.find_element_by_partial_link_text(value)
        elif by == "name":
            driver.find_element_by_name(value)
        elif by == "tag name":
            driver.find_element_by_tag_name(value)
        elif by == "css selector":
            driver.find_element_by_css_selector(value)
        flag = True
    except Exception as e:
        flag = False
    finally:
        return flag


# 返回xpath序列
def get_xpath_serial(xpath_value_mod, n):
    return xpath_value_mod.replace('[-n-]', '[' + str(n) + ']', 1)


# 执行函数
# @param: search_num -Int 每页上搜索数目
#         view_num -Int 翻页次数
#         swipe_up_dis -Float 上滑幅度
def do_xpath_unit(driver, xpath_set, search_num=20, view_num=3, swipe_up_dis=0.5):

    result = []

    # 若开启遍历
    if xpath_set[1]:
        # 上滑几次
        for _ in range(view_num):
            # 每个页面默认搜索15个元素
            for i in range(search_num):
                print(i)

                xpath_value_mod = xpath_set[0][0][1]
                xpath_target = get_xpath_serial(xpath_value_mod, i)

                # 验证序列目标是否存在
                if has_element(driver, 'xpath', xpath_target):

                    # 开启循环
                    for xpath_unit in xpath_set[0]:

                        result_dict = {}

                        try:
                            if xpath_unit[0] == 'get_text':
                                text = driver.find_element_by_xpath(get_xpath_serial(xpath_unit[1], i)).text

                                result_dict[xpath_unit[2]] = text

                            if xpath_unit[0] == 'click':
                                driver.find_element_by_xpath(get_xpath_serial(xpath_unit[1], i)).click()

                            if xpath_unit[0] == 'back':
                                back(driver)
                        except Exception:
                            continue
                        finally:
                            # 防止重复
                            if result_dict not in result:
                                result.append(result_dict)

                # 目标序列不存在
                else:
                    continue
            # 上滑翻页
            swipe_up(driver, swipe_up_dis)

    else:
        result_dict = {}
        # 开启循环
        for xpath_unit in xpath_set[0]:
            try:
                if xpath_unit[0] == 'get_text':
                    text = driver.find_element_by_xpath(xpath_unit[1]).text
                    result_dict[xpath_unit[2]] = text

                if xpath_unit[0] == 'click':
                    driver.find_element_by_xpath(xpath_unit[1]).click()

                if xpath_unit[0] == 'back':
                    back(driver)
            except Exception:
                continue
            finally:
                # 防止重复
                if result_dict not in result:
                    result.append(result_dict)

    if result:
        return result
    else:
        return


# 打印抓取结果
def print_result(result, unit_num=1):
    i = 0
    p = 0
    for result_unit in result:
        for key, values in result_unit.items():
            if i % unit_num == 0:
                p += 1
                print(str(p) + ': ' + key + ': ' + values)
            else:
                _space = ' ' * len(str(p)) + '  '
                print(_space + key + ': ' + values)

        i += 1


