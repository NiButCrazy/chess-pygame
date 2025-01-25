"""
游戏场景
"""

import pygame
import threading
import time
from common.sceneManager import scene_manager
from common import resources
from common.eventManager import event_manager
from common.uiBase import UIBase
from common.config import *
from common.gameMap import GameMap


# 背景图片的画布，为了调整背景图片的大小和位置
background_surface = pygame.Surface((800,800))
background_surface.fill((255, 255, 255))
# 调整源图片的比例和大小
background_img = pygame.transform.smoothscale(resources.GAME_bg_img,(800,1700))
# 将图片绘制到画布上去
background_surface.blit(background_img,(0,-250))
# 字体路径
font_path = "font.ttf"
# 按钮图片加载
play_img = resources.GAME_ui_play_img
pause_img = resources.GAME_ui_pause_img
# 音效加载
hover_sound_effect = resources.EFFECT_hover
press_sound_effect = resources.EFFECT_press
press_sound_effect.set_volume(0.2)


class TimerThread( threading.Thread ):
    """
    一个定时器线程类
    """
    def __init__(self, ui: UIBase = None):
        super().__init__()
        self.seconds = 0
        self.seconds_format = "00:00"
        self.stop = True
        self.ui = ui
        # 设为守护线程
        self.daemon = True
        # 绑定的按钮
        self.btn: UIBase | None = None

    def run(self):
        while True:
            time.sleep( 1 )
            if self.stop:continue
            self.seconds += 1
            self.format_seconds(self.seconds)
            if not self.ui is None:
                self.ui.set_text(self.seconds_format)

    def format_seconds(self,seconds):
        """
        将秒数转换为分秒的格式。
        :param : 秒数
        """
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        self.seconds_format = f"{minutes:02d}:{seconds:02d}"

    def stop_timer(self):
        self.stop = True

def create_scene(screen: pygame.Surface) -> tuple[list[UIBase], pygame.Surface]:
    """
    游戏场景
    :param screen: 想要绘制的Surface对象
    :return: 返回一个列表，list[0]是包含所有UIBase实例的列表，list[1]是一个背景图片的Surface对象
    """
    # 获取配置
    config = get_config_all()

    # 基础信息文本
    base_info_text = "双人互啄 {0}".format(config["player_names"][config["player_name_index"]])

    # 基础信息UI
    base_info = UIBase(screen, -50, 0, (800, 50), (255, 255, 255), base_info_text, 23,
                       (0, 0, 0), font_path, True, enabled_event = False)

    scene_manager.ui_dict["base_info"] = base_info

    # 返回按钮
    back_btn = UIBase(screen, 25, 27, (30, 30), (255, 255, 255), "", 23,
                      (0, 0, 0), font_path, True,center_anchor = True)
    back_btn.set_background_image(path = resources.GAME_ui_back_btn_img)
    back_btn.opacity = 100
    back_btn.mouse_enter(lambda event, option:(back_btn.transition_opacity(255, 0.0),
                                               pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND),
                                               hover_sound_effect.play()))
    back_btn.mouse_leave(lambda event, option: (back_btn.transition_opacity(100, 0.0),
                                                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW),
                                                back_btn.transition_scale(1, 1, 0.05)))
    back_btn.mouse_up(
        lambda event, option: (
            scene_manager.smooth_toggle_scene(screen, "menu"),
            scene_manager.ui_dict["btn_start_game"].set_text("继续"),
            back_btn.transition_scale(1, 1, 0.05),
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW),
            press_sound_effect.play()
        )
    )
    back_btn.mouse_down(lambda event, option: back_btn.transition_scale(1.1, 1.1, 0.1))
    # 游戏加载渲染区域
    game_ui = UIBase(screen, 75, 75, (640,640))
    game_ui.opacity = 0
    # 开始游戏按钮
    start_game_btn = UIBase(screen, 400, 200, (0, 0), text = "开始游戏", font_size = 30,
                            center_anchor = True, user_font_family = True, font_family = font_path)

    start_game_btn.mouse_up(
        lambda e, a: (
            start_game_btn.transition_opacity(0, 0.5).then(start_game, ui = game_ui,
                                                           btn = start_game_btn),
            press_sound_effect.play(),
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW),
            fade_out_bg_img(1)
        )
    )
    start_game_btn.mouse_enter(lambda event, option: (start_game_btn.set_text(font_size = 33),
                                                      pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND),
                                                      hover_sound_effect.play()))
    start_game_btn.mouse_leave(lambda event, option: (pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW),
                                                      start_game_btn.set_text(font_size = 30)))
    # UI列表推入
    ui_list = [
        base_info,
        back_btn,
        game_ui,
        # start_game_btn
    ]
    load_new_game(game_ui)
    return ui_list, background_surface



# noinspection PyUnusedLocal
def load_new_game(ui: UIBase, **option):
    """
    载入新游戏
    :param ui: 父容器
    :param option: 函数携带参数
    :return:
    """
    ui.opacity = 255 # 调试用
    # ui.transition_opacity(255, 1) # 正常淡入
    game_map = GameMap(ui, 640)
    # 如果游戏是第一次开始，则...
    if not event_manager.game_has_started:
        event_manager.game_has_started = True

# noinspection PyUnusedLocal
def start_game(option: dict[str, UIBase]):
    """
    开始游戏回调函数
    :param option: 携带参数
    :return:
    """
    game_ui = option["ui"]
    btn = option["btn"]
    load_new_game(game_ui)
    btn.close()


def __fade_out_bg_img(duration: float = 0.5):
    fps_clock = scene_manager.FPS_CLOCK
    step = duration / fps_clock
    now_step = 0
    fade_step = 255 / step
    while now_step < step:
        now_step += 1
        background_surface.fill((255, 255, 255))
        background_img.set_alpha(255 - now_step * fade_step)
        background_surface.blit(background_img, (0,-250))
        time.sleep(fps_clock)
    background_surface.fill((255, 255, 255))
    background_img.set_alpha(0)
    background_surface.blit(background_img, (0,-250))

def fade_out_bg_img(duration: float = 0.5):
    """
    背景图片淡出
    :param duration:
    :return:
    """
    thread = threading.Thread(target = __fade_out_bg_img, args = (duration,))
    thread.daemon = True
    thread.start()