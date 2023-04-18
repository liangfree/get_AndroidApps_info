# get_AndroidApps_info

## 1 基于Appium的Android应用数据收集方法

本章介绍一种可行的方法——基于Appium的Android应用数据收集方法，也是本文成功获取到App信息的方法，首先简要介绍Appium，其次简要介绍环境配置，最后概述方法过程。

### 1.1 Appium简介

Appium是一个自动化测试开源工具，支持IOS、Android平台上的原生应用、web应用和混合应用。
- Appium采用C/S架构，Client端是可供用户下载的客户端，Server端是NodeJS的web服务器，Client与Server之间采用HTTP通信，在上层发送JSON格式数据；

- Appium在webDriver（Selenium WebDrier）的基础上丰富了更多接口，形成了自己的一套API；

- Appium的核心即Server端的指令翻译库，其作用是将来自于客户端的不同语言、不同平台的指令翻译成可供目标设备（例如本工作中的Android 10设备）执行的指令，这也是Appium最核心的跨平台特性（iOS、Android、Windows）原因所在；

- Appium是开源的，他属于JS Foundation（Open JS Foundation，是关键开源 JavaScript 项目的主要家园，包括 Appium、Dojo、jQuery、Node.js 和 webpack 等 27 个项目），JS Foundation在层级上又属于The LINUX Foundation。

**工作原理**

![屏幕截图 2021-06-07 091438](figs/屏幕截图 2021-06-07 091438.jpg)

### 1.2 环境配置

- Java + Python（Packages）：Appium-Python-Client v1.1.0
- Android SDK（Android 11 R API Level 30）
- Appium（for Windows v1.21）
- Android设备（HMA-AL00 HUAWEI Mate20 Android 10 条件：USB调试+亮屏）
- adb: Windows环境变量

最后，使用以下命令验证连接设备是否成功：

```shell
adb devices
```
shell 返回值：
```shell
List of devices attached
HJS5T19829001972        device 
```
代表已接入Android设备。

在Appium Client中配置变量验证是否工作正常：

![image-20210607092730526](figs/image-20210607092730526.png)

点击左侧元素，右侧会出现Android界面xml解析。


### 1.3 方法概述

**流程总览**

整个流程可分为5个部分，注意，以下步骤均建立在上述环境配置正常的条件下。

1. 编写Python程序，用于自动化测试；

2. 获取App包的启动信息；

3. 在Appium客户端中查看元素xpath属性值，设计点击顺序；

4. 在Python程序中编写配置文件；

5. 运行抓取App数据；

**Python程序**

程序共分为4个文件，架构如下：

- main.py：主程序文件，所有执行均在此调用；
- tools.py：工具函数文件，main中所有执行的函数均在此定义；
- caps.py：App链接文件，包含关键的App包信息和启动Activity；
- xpath.py：App的xpath点击顺序，不同App只需定义不同的xpath变量即可，更换不同App时需在此修改；


核心代码如下：

（tools.py：上滑函数）

```python
# 上滑 手势从下至上 0.5为一整页
def swipe_up(driver, n=0.3):
    # tuple: 获取屏幕大小
    size = (driver.get_window_size()['width'],
            driver.get_window_size()['height'])
    # 定义滑动参数
    x = int(size[0] * 0.5)  # x坐标
    y1 = int(size[1] * 0.9)  # 起始y坐标
    y2 = int(size[1] * (0.9 - 0.9 * n))    # 终点y坐标
    # 执行动作
    driver.swipe(x, y1, x, y2)
```

（tools.py：返回函数，利用了某些Android系统边缘滑动返回上一级的手势操作）

```python
# 返回 实际为左右边缘滑动 只适用于部分边缘滑动返回的手机
def back(driver):
    # tuple: 获取屏幕大小
    size = (driver.get_window_size()['width'],
            driver.get_window_size()['height'])
    # 定义滑动参数
    x = int(size[0] * 0.3)  # x坐标
    y = int(size[1] * 0.5)  # 起始y坐标
    # 执行动作 屏幕边缘滑动返回
    driver.swipe(0, y, x, y)
```
（tools.py：主要函数，通用的App抓取逻辑）

```python
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
                                text = driver.find_element_by_xpath(
                                    get_xpath_serial(xpath_unit[1], i)
                                ).text

                                result_dict[xpath_unit[2]] = text

                            if xpath_unit[0] == 'click':
                                driver.find_element_by_xpath(
                                    get_xpath_serial(xpath_unit[1], i)
                                ).click()

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

```

（caps.py：微信启动参数）
```python
# 微信
    'weixin': {
        'platformName': GLOBAL_PLATFORMNAME,
        'deviceName': GLOBAL_DEVICENAME,
        'platformVersion': GLOBAL_PLATFORMVERSION,
        'noReset': GLOBAL_NORESET,
        'unicodeKeyboard': GLOBAL_UNICODEKEYBOARD,
        'appPackage': 'com.tencent.mm',
        'appActivity': '.ui.LauncherUI',
    },
```

在上述结构组织下，更换抓取目标App只需在xpath.py文件内配置好参数即可运行抓取数据，更多详细代码请参照”4 备注“部分关于源代码的注释。

**获取APP包信息：查看包名称及启动Activity**

获取App的启动信息是第一步，所有测试App的启动参数配置均在caps.py文件中，例如上述微信的启动参数，Appium所需的核心启动参数如下（以小红书App为例）：

```python
{
    'platformName': GLOBAL_PLATFORMNAME,        # 平台名称
    'deviceName': GLOBAL_DEVICENAME,            # 设备名称
    'platformVersion': GLOBAL_PLATFORMVERSION,  # 系统版本号
    'noReset': GLOBAL_NORESET,                  # 免登陆TRUE
    'unicodeKeyboard': GLOBAL_UNICODEKEYBOARD,  # 使用Unicode以输入中文
    'appPackage': 'com.tencent.mm',             # apk的包名
    'appActivity': '.ui.LauncherUI',            # App启动关键Activity
}
```
对于测试过程中的同一台设备而言，'platformName'（平台名称）、'deviceName'（设备名称）、'platformVersion'（系统版本号）、'noReset'（免登陆TRUE）、'unicodeKeyboard'（开启Unicode）参数不需要改变，而关键的'appPackage'（apk的包名）、'appActivity'（Activity名）等不容易获取，前者为App包的id，后者为启动主页面的进程id。

网上有大量的关于常见APP的包信息和Activity信息资料，但一般已经失效（App版本更新等原因）或不正确，显然，默认的方法字段不适用于大部分App，本文采用以下方法获取上述两项关键参数。使用以下shell命令查看当前活动App相关信息：

```shell
adb shell dumpsys window w |findstr \/ |findstr name=
```
shell 返回值如下：

```shell
mSurface=Surface(name=GestureNavBottom)/@0x3fb13a1
mSurface=Surface(name=GestureNavRight)/@0x3fb1215
mSurface=Surface(name=GestureNavLeft)/@0x3fb1323
mAnimationIsEntrance=true
mSurface=Surface(name=StatusBar)/@0x392b383
mSurface=Surface(name=com.tencent.mm/com.tencent.mm.ui.LauncherUI)/@0x411d3bf 
mAnimationIsEntrance=true
mSurface=Surface(name=com.android.systemui.HwImageWallpaper)/@0x3b33711
```

该命令以微信为例，以上返回值第6行：'com.tencent.mm/com.tencent.mm.ui.LauncherUI'即为所需参数信息，'com.tencent.mm'为所需的微信包名称，'.ui.LauncherUI'为微信启动Activity。其他APP可采用同样方法获得，该方法能比较准确的获取上述两项关键参数。

**运行抓取程序**

在main.py中运行主程序抓取数据，主要代码如下（以微信App为例）：
```python
# 全局变量 HTTP链接地址
GLOBAL_WEBDRIVERHTTPLOC = 'http://127.0.0.1:4723/wd/hub'


# main:
if __name__ == '__main__':

    # ==== 微信 == start =============================================
    # 打开app
    driver = webdriver.Remote(GLOBAL_WEBDRIVERHTTPLOC, caps['weixin'])

    # 打开app需要时间较长 最短3秒
    time.sleep(3)

    # ---------------------------------------------------
    # 微信 任务一 抓取信息 最近聊天
    result = do_xpath_unit(driver, xpath_weixin[0], 20, 10)
    # 输出抓取结果 聊天信息
    print_result(result, 3)

    # ---------------------------------------------------
    # 微信 任务二 抓取朋友圈信息
    # 点击发现按钮
    do_xpath_unit(driver, xpath_weixin[1])
    time.sleep(0.5)
    
    # 点击朋友圈按钮
    do_xpath_unit(driver, xpath_weixin[2])
    time.sleep(0.5)
    
    # 获取朋友圈数据
    result = do_xpath_unit(driver, xpath_weixin[3], 5, 20)
    # 输出抓取结果 朋友圈信息
    print_result(result, 2)

    # ==== 微信 == end =============================================

```

### 1.4 实验结果

根据上述方法步骤，分别对微信、QQ、便签、知乎4个App抓取用户数据，详细如下：

| 序号 | App名 | 类别       | 操作                             |
| ---- | ----- | ---------- | -------------------------------- |
| 1    | 微信  | 即时聊天   | 抓取最近聊天信息、抓取朋友圈内容 |
| 2    | QQ    | 即时聊天   | 抓取群聊聊天记录                 |
| 3    | 便签  | 笔记应用   | 抓取便签笔记内容                 |
| 4    | 知乎  | 信息流应用 | 抓取信息流内容                   |

**1 微信：抓取最近聊天信息、抓取朋友圈内容**

获取到70条最近聊天信息（设置70，实际还可以更多，部分截图如下，下同）：

![weixin-2](figs/weixin-2.jpg)

获取到40条朋友圈动态：

![weixin-4](figs/weixin-4.jpg)

**2 QQ：获取群聊聊天记录**

获取到70条聊天记录，包括发送人、发送内容、时间等信息：

![qq-2](figs/qq-2.jpg)

**3 便签：获取便签笔记内容**

获取到100+条便签记录（便签笔记均来自本人记录）：

![bianqian-2](figs/bianqian-2.jpg)

**4 知乎：获取首页推荐信息流**

获取到100+信息，包括问题名称、答主昵称、回答内容、获赞数目等：

![zhihu-1](figs/zhihu-1-1623034847875.jpg)

## 2 总结

本文的主要工作在于：

- 利用Appium实现了信息抓取的简单框架，只需少量的配置信息就可以运行通用的抓取函数自动获取APP数据；
- 基于Appium的信息抓取方案本质上是基于界面层的信息获取，因此可以绕过Android底层复杂的安全机制，对于设备本身免Root，减少对设备的不利影响，也可以绕过APP厂商自定义的种种规则限制，比较通用灵活；
- 成功获取到了微信、QQ、便签、知乎等App数据，其中包括用户隐私数据，总体来说，对于信息流等数据的获取比较简单，对于微信等超级App的数据获取比较复杂，原因在于此类超级应用采用的框架更加复杂，Appium平台动作部分受限。

不足之处：

- 有线连接设备，开启USB调试，设备需一直亮屏可操作




