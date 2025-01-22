"""
逻辑代码集合处和游戏入口
"""
import sys
import pygame
import time
from common import config
from common.scene import gameScene
from common.resources import ICON
from common.scene.menuScene import *
from common.sceneManager import scene_manager
from common.eventManager import emit, event_manager
from common.inputBox import message_box



# 初始化，切记这是所有游戏代码操作之前
pygame.init()
# 设置一个Surface类的图标
pygame.display.set_icon(ICON)
# 设置标题
pygame.display.set_caption("阿伟的国际象棋🤣👉🤡")
# 设置屏幕大小
screen = pygame.display.set_mode((config.get_config("width"), config.get_config("height")))
# ==== 设定初始场景UI ====
# 将菜单场景和游戏场景推入场景列表进行初始化
scene_manager.push_scene("menu", create_menu_scene(screen), bg_music="music2.mp3")
# 加载启动场景
scene_manager.load_welcome_scene(screen)


while True:
    # 事件监听
    for event in pygame.event.get():
        # 是否开启事件穿透。只针对鼠标事件
        event.enabled_event_penetration = False
        if event.type == pygame.QUIT:
            res = message_box("太狠心了", "要离开了吗？")
            if res:
                pygame.quit()
                sys.exit()
        # 游戏是否处于暂停状态
        elif event_manager.game_stop:
            time.sleep(scene_manager.FPS_CLOCK)
            continue
        else:
            # 向事件管理器发送事件
            emit(event, stop_emit = False)

    # 清屏
    screen.fill((0, 0, 0))
    # 这是背景图片绘制
    screen.blit(scene_manager.now_scene[1], (0, 0))
    # UI绘制
    for ui in scene_manager.now_scene[0]:
        ui.update(scene_manager.FPS_CLOCK)
    # 更新屏幕
    pygame.display.flip()
    # 保证帧率，注意！！！这种sleep控制帧数本质上是完全错误的，只是懒得修改以前的代码了
    time.sleep(scene_manager.FPS_CLOCK)

