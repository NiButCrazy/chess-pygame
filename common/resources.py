"""
一个用于注册和管理资源的对象
"""

import pygame

# 音频模块初始化
pygame.mixer.init()

# 音效
EFFECT_hover = pygame.mixer.Sound("../resource/sound effect/btn_sound effect.mp3")
EFFECT_press = pygame.mixer.Sound("../resource/sound effect/btn_press_sound_effect.mp3")

# 游戏UI图标
ICON = pygame.image.load("../resource/ui/icon.png")

# 启动欢迎界面
WELCOME_bg_img = pygame.image.load("../resource/image/welcome.png")

# 菜单界面
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