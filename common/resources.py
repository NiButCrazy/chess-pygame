"""
一个用于注册和管理资源的对象
"""

import pygame

# 色彩
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (128,128,128)
YELLOW = (255,255,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
MAP_BORDER_COLOR = (0, 198, 255)
MAP_BLOCK_BORDER_COLOR = (255, 163, 0)


# cmd色彩
__cmd_color = {
    'reset': '\033[0m',
    'bold': '\033[01m',
    'disable': '\033[02m',
    'underline': '\033[04m',
    'reverse': '\033[07m',
    'strikethrough': '\033[09m',
    'invisible': '\033[08m',
    'black': '\033[30m',
    'red': '\033[31m',
    'green': '\033[32m',
    'orange': '\033[33m',
    'blue': '\033[34m',
    'purple': '\033[35m',
    'cyan': '\033[36m',
    'light_grey': '\033[37m',
    'dark_grey': '\033[90m',
    'light_red': '\033[91m',
    'light_green': '\033[92m',
    'yellow': '\033[93m',
    'light_blue': '\033[94m',
    'pink': '\033[95m',
    'light_cyan': '\033[96m'
}

__cmd_bg_color = {
    '':'',
    'black': '\033[40m',
    'red': '\033[41m',
    'green': '\033[42m',
    'orange': '\033[43m',
    'blue': '\033[44m',
    'purple': '\033[45m',
    'light_blue': '\033[46m',
    'white': '\033[47m',
}

def f(text:str, color:str, bg_color = '') -> str:
    """
    cmd 文字色彩转译格式化
    :param text: 源文本
    :param color: 颜色
    :parameter bg_color: (可选) 背景颜色
    :return: 格式化后的字符串
    """
    try:
        return f"{__cmd_color[color]}{__cmd_bg_color[bg_color]}{text}{__cmd_color['reset']}"
    except IndexError :
        print(f"{f('错误：', 'red')}颜色{color}不存在")



# 音频模块初始化
pygame.mixer.init()

# 音效
EFFECT_hover = pygame.mixer.Sound("../resource/sound effect/btn_sound effect.mp3")
EFFECT_press = pygame.mixer.Sound("../resource/sound effect/btn_press_sound_effect.mp3")

# 游戏UI图标
ICON = pygame.image.load("../resource/ui/icon.png")

# 启动欢迎界面
WELCOME_bg_img = pygame.image.load("../resource/image/welcome.png")

# 菜单场景
MENU_bg_img = pygame.image.load("../resource/image/background-img.jpg")
MENU_setting_bg_img = pygame.image.load("../resource/image/ui_background.png")
MENU_create_author_img = pygame.image.load("../resource/image/create.jpg")
MENU_ui_exit_img = pygame.image.load("../resource/ui/btn_exit.png")
# 菜单关联图片
MENU_switch_start_img = pygame.image.load("../resource/image/start_game.png")
MENU_switch_setting_img = pygame.image.load("../resource/image/setting2.png")
MENU_switch_create_img = pygame.image.load("../resource/image/create.png")
MENU_switch_exit_img = pygame.image.load("../resource/image/setting.png")
MENU_switch_online_img = pygame.image.load("../resource/image/rank.png")
# 菜单按钮UI
MENU_ui_btn_img = pygame.image.load("../resource/ui/btn4.png")
MENU_ui_btn_press_img = pygame.image.load("../resource/ui/btn3.png")

# 菜单设置按钮
MENU_ui_btn_right_arrow_img = pygame.image.load("../resource/ui/right.png")
MENU_ui_btn_left_arrow_img = pygame.image.load("../resource/ui/left.png")

# 游戏场景
GAME_bg_img = pygame.image.load("../resource/image/background-img2.jpg")
GAME_ui_play_img = pygame.image.load("../resource/ui/play.png")
GAME_ui_pause_img = pygame.image.load("../resource/ui/paused.png")
GAME_ui_back_btn_img = pygame.image.load("../resource/ui/left.png")

# 棋子图片映射表
CHESS_img_map: dict[str, dict[str, pygame.Surface]] = {
    'white': {
        'bin': pygame.image.load("../resource/image/white_bin.png"),
        'che': pygame.image.load("../resource/image/white_che.png"),
        "xiang": pygame.image.load("../resource/image/white_xiang.png"),
        "ma": pygame.image.load("../resource/image/white_ma.png"),
        'hou': pygame.image.load("../resource/image/white_hou.png"),
        'wang': pygame.image.load("../resource/image/white_wang.png"),
    },
    'black': {
        'bin': pygame.image.load("../resource/image/black_bin.png"),
        'che': pygame.image.load("../resource/image/black_che.png"),
        "xiang": pygame.image.load("../resource/image/black_xiang.png"),
        "ma": pygame.image.load("../resource/image/black_ma.png"),
        'hou': pygame.image.load("../resource/image/black_hou.png"),
        'wang': pygame.image.load("../resource/image/black_wang.png"),
    }
}
