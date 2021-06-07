# Appium APP连接配置文件
# Type: Dict


# 全局变量 更换设备时需修改
GLOBAL_PLATFORMNAME = 'Android'
GLOBAL_DEVICENAME = 'HMA-AL00'
GLOBAL_PLATFORMVERSION = '10'
GLOBAL_NORESET = True
GLOBAL_UNICODEKEYBOARD = True


caps = {

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

    # QQ
    'qq': {
        'platformName': GLOBAL_PLATFORMNAME,
        'deviceName': GLOBAL_DEVICENAME,
        'platformVersion': GLOBAL_PLATFORMVERSION,
        'noReset': GLOBAL_NORESET,
        'unicodeKeyboard': GLOBAL_UNICODEKEYBOARD,
        'appPackage': 'com.tencent.mobileqq',
        'appActivity': '.activity.SplashActivity',
    },

    # 便签
    'bianqian': {
        'platformName': GLOBAL_PLATFORMNAME,
        'deviceName': GLOBAL_DEVICENAME,
        'platformVersion': GLOBAL_PLATFORMVERSION,
        'noReset': GLOBAL_NORESET,
        'unicodeKeyboard': GLOBAL_UNICODEKEYBOARD,
        'appPackage': 'com.example.android.notepad',
        'appActivity': '.NotePadActivity',
    },

    # 知乎
    'zhihu': {
        'platformName': GLOBAL_PLATFORMNAME,
        'deviceName': GLOBAL_DEVICENAME,
        'platformVersion': GLOBAL_PLATFORMVERSION,
        'noReset': GLOBAL_NORESET,
        'unicodeKeyboard': GLOBAL_UNICODEKEYBOARD,
        'appPackage': 'com.zhihu.android',
        'appActivity': '.app.ui.activity.MainActivity',
    },

}

