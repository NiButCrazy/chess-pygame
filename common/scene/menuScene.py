"""
开始菜单场景
"""
import pygame
import sys

from common import uiBase
from webbrowser import open
from .startSceneBtn import StartSceneBtn

from common import resources
from common.inputBox import create_input_box, message_box
from common.config import get_config, save_config, get_config_all, reload_config
from common.eventManager import event_manager
from common.eventManager import set_event_penetration
from common.sceneManager import scene_manager


__all__ = [
    "create_scene",
]

# FPS预设列表d
FPS_PRESET = [30, 60, 120, 240]


screen_width = get_config("width")
screen_height = get_config("height")
game_version = get_config("version")

setting_ui_background_img = resources.MENU_setting_bg_img
create_img = resources.MENU_create_author_img

font_path = "font.ttf"


hover_sound_effect = resources.EFFECT_hover

# 注册自定义事件，防止pygame自带事件来不及更新
event_manager.register_event("打开开始游戏")
event_manager.register_event("打开设置")
event_manager.register_event("打开致谢")
event_manager.register_event("打开排行")

def create_scene(screen: pygame.Surface) -> tuple[list[StartSceneBtn], pygame.Surface]:
    """
    开始菜单场景
    :param screen: 想要绘制的Surface对象
    :return: 返回一个列表，list[0]是包含所有UIBase实例的列表，list[1]是一个背景图片的Surface对象
    """


    # 此场景的背景图片
    background_img = resources.MENU_bg_img
    # 加载各选项所关联的图片
    btn_start_game_switch_img = resources.MENU_switch_start_img
    btn_setting_switch_img = resources.MENU_switch_setting_img
    btn_create_switch_img = resources.MENU_switch_create_img
    btn_online_switch_img = resources.MENU_switch_online_img
    btn_exit_switch_img = resources.MENU_switch_exit_img

    # 选项所关联的图片
    switch_img_surface = uiBase.UIBase(screen, 200, 170, (400, 400))
    switch_img_surface.set_background_image(btn_exit_switch_img)
    switch_img_surface.enabled_event = False
    # 选项所关联的文字
    switch_text = uiBase.UIBase(screen, 400, 550, (0,0), text="欢迎", font_size=28, font_color=(125, 125, 125), font_family = "font.ttf", user_font_family=True, center_anchor = True)
    switch_text.enabled_event =False
    # 开始游戏按钮
    btn_start_game = StartSceneBtn(screen, -52, 100, (200, 70), text = "双人",font_size = 22)
    btn_start_game.mouse_enter(lambda event, args: (switch_img_surface.set_background_image(btn_start_game_switch_img), switch_text.set_text(content = "同屏双人")))
    btn_start_game.mouse_up(lambda event, args: open_start_game(screen))
    scene_manager.ui_dict["btn_start_game"] = btn_start_game
    # 联机按钮
    btn_online = StartSceneBtn(screen, -52, 180, (200, 70), text = "联机", font_size = 22)
    btn_online.mouse_enter(lambda event, args: (switch_img_surface.set_background_image(btn_online_switch_img), switch_text.set_text(content = "开发中...")))
    # btn_setting.mouse_up(lambda event, args: open_setting(screen, btn_setting))
    # 设置按钮
    btn_setting = StartSceneBtn(screen, -52, 260, (200, 70), text = "设置", font_size = 22)
    btn_setting.mouse_enter(lambda event, args: (switch_img_surface.set_background_image(btn_setting_switch_img), switch_text.set_text(content = "懒狗设置")))
    btn_setting.mouse_up(lambda event, args: open_setting(screen,btn_setting))
    # 致谢按钮
    btn_create = StartSceneBtn(screen, -52, 340, (200, 70), text = "致谢", font_size = 22)
    btn_create.mouse_enter(lambda event, args: ( switch_img_surface.set_background_image(btn_create_switch_img), switch_text.set_text(content = "开发者名单")))
    btn_create.mouse_up(lambda event, args: open_create(screen, btn_create))
    # 退出按钮
    btn_exit = StartSceneBtn(screen, -52, screen_height - 100, (200, 70), text = "退出", font_size = 22)
    btn_exit_img = resources.MENU_ui_exit_img

    # 忽略形参类型检查
    # noinspection PyUnusedLocal
    def btn_exit_enter(event: pygame.event.Event, option):
        btn_exit.set_background_image(btn_exit_img)
        switch_img_surface.set_background_image(btn_exit_switch_img)
        switch_text.set_text(content="你真要狠心离开吗")

    # 可以忽略形参类型检查
    # noinspection PyUnusedLocal
    def btn_exit_up(event: pygame.event.Event, option):
        res = message_box("太狠心了", "要离开了吗？")
        if res:
            pygame.quit()
            sys.exit()


    btn_exit.mouse_enter(btn_exit_enter)
    btn_exit.mouse_up(btn_exit_up)
    # 版本号
    version = uiBase.UIBase(screen, screen_width - 118, screen_height - 40, (0,0), text = game_version, font_size = 18,font_family = 'font.ttf',user_font_family = True)
    version.enabled_event = False
    # 将按钮添加进UI列表
    ui_list= [
        btn_start_game,
        btn_online,
        btn_setting,
        btn_create,
        btn_exit,
        version,
        switch_img_surface,
        switch_text
    ]
    return ui_list,background_img

setting_info_bomb_number: uiBase.UIBase | None = None

def open_setting(screen: pygame.Surface, btn: StartSceneBtn):
    """
    打开设置UI
    :param screen: 要绘制的surface
    :param btn: 绑定的按钮
    :return:
    """
    if not btn.has_open_ui:
        # 读取设置
        reload_config()
        # 计算出游戏更新循环周期
        fps_clock = scene_manager.FPS_CLOCK
        # 发送一个打开设置的事件，间接更新渲染视图
        event_manager.post_event("打开设置")
        btn.has_open_ui = True
        # 创建半透明的黑色遮罩
        setting_ui_mask = uiBase.UIBase(screen, 0, 0, (screen_width, screen_height), color = (0, 0, 0))
        # 创建一个背景图片
        setting_ui = uiBase.UIBase(screen, 100, -30, (600,800))
        setting_ui.set_background_image(setting_ui_background_img)
        # 加载设置选项操作的图片
        btn_right_arrow_img = resources.MENU_ui_btn_right_arrow_img
        btn_left_arrow_img = resources.MENU_ui_btn_left_arrow_img
        # 背景图片设为遮罩子节点，方便管理
        setting_ui_mask.children.append(setting_ui)
        # 创建一个关闭设置UI的函数
        def close_setting_ui(event, option):
            if "mouse_btn" in option and not option["mouse_btn"] == event.button:
                return
            # 防止这傻逼pycharm给我弹一个未使用形参的警告
            if not option == {} or not event:
                pass
            btn.has_open_ui = False
            # 保存配置
            save_config()
            # 及时更新信息
            scene_manager.ui_dict["base_info"].set_text("双人互啄 {0}".format(get_config("player_names")[get_config("player_name_index")]))
            # 淡出
            setting_ui_mask.transition_opacity(0, 0.1, fps_clock, children_together = False).then(lambda **options: setting_ui_mask.close())
            setting_ui.transition_opacity(0, 0.2, fps_clock)
        # 开启遮罩的键盘事件
        setting_ui_mask.enabled_keyboard_event = True
        # 将背景图片的鼠标事件开启事件穿透
        setting_ui.mouse_up(lambda event,options: set_event_penetration(event,True))
        # 绑定鼠标右键点击关闭设置UI
        setting_ui_mask.mouse_up(close_setting_ui, mouse_btn = 3)
        setting_ui_mask.bind_keyboard_callback(pygame.K_ESCAPE, pygame.KEYUP, close_setting_ui)

        # =========================================创建设置UI的具体内容=============================================
        common_option = {"font_size": 25, "font_color": (0, 0, 0), "font_family": "font.ttf", "user_font_family":True}
        setting_ui_dict = {
            "玩家名称": ( f"{get_config('player_names')[get_config('player_name_index')]}", "知子莫如父" ),
            "窗口大小": ( f"{get_config('width')} x {get_config('height')}", "暂不支持更改" ),
            "游戏帧率": ( f"{get_config('FPS')} FPS", "你玩的不是3A大作" ),
            "背景音乐": ( f"{int(get_config('volume') * 100)}", "调整背景音乐的音量" )
        }
        ui_num = 0
        # 用于设置选项的提示文本
        setting_ui_tips = uiBase.UIBase(screen, 400, 580, (0, 0), text = "", center_anchor = True,**common_option)
        setting_ui_tips.set_text(font_color = (150,150,150))
        setting_ui.children.append(setting_ui_tips)
        # 生成设置选项的选项和按钮
        for title, content in setting_ui_dict.items():
            # 设置标题
            setting_info_title = uiBase.UIBase(screen, 250, 230 + ui_num * 50, (0, 0), text = title, **common_option)
            # 设置内容
            setting_info = uiBase.UIBase(screen, 500, 230 + ui_num * 50, (0, 0), text = content[0], **common_option)
            setting_info_title.enabled_event = False
            setting_info.opacity = 0
            setting_info_title.opacity = 0
            if title == "玩家名称":
                setting_info.name = get_config('player_names')[get_config('player_name_index')]
            else:
                setting_info.name = title

            # 扩大判定区域，使得可以按到箭头按钮
            setting_info.rect.width += 80
            size = setting_info.rect.size
            setting_info.move_by(-int( size[0]/2 ),0)
            pos_x_r = int( 483 + size[0] / 2)
            pos_x_l = int(515 - size[0] / 2)
            pos_y = int( 244 + ui_num * 50 )
            # 右箭头按钮
            btn_right_arrow = uiBase.UIBase(screen, pos_x_r, pos_y, (20, 20), center_anchor = True)
            btn_right_arrow.set_background_image(btn_right_arrow_img)
            # 左箭头按钮
            btn_left_arrow = uiBase.UIBase(screen, pos_x_l, pos_y, (20, 20), center_anchor = True)
            btn_left_arrow.set_background_image(btn_left_arrow_img)
            btn_left_arrow.display = False
            btn_right_arrow.display = False
            # 不允许和父元素一起透明度过渡
            btn_left_arrow.allow_opacity_transition_follow_parent = False
            btn_right_arrow.allow_opacity_transition_follow_parent = False
            # 绑定按钮和选项的事件
            setting_info.mouse_enter(setting_info_mouse_enter,btn = (btn_right_arrow,btn_left_arrow), tips = setting_ui_tips, tips_text = content[1],info = setting_info,title = title)
            setting_info.mouse_leave(setting_info_mouse_leave, btn = (btn_right_arrow, btn_left_arrow))
            setting_info.mouse_up(setting_info_mouse_up, btn = (btn_right_arrow,btn_left_arrow), tips = setting_ui_tips, info = setting_info,title = title)
            btn_right_arrow.mouse_up(setting_right_arrow_mouse_up, btn = btn_right_arrow, info = setting_info, title = title)
            btn_right_arrow.mouse_down(setting_arrow_mouse_down, btn = btn_right_arrow)
            btn_right_arrow.mouse_enter(setting_arrow_mouse_enter, btn = btn_right_arrow)
            btn_right_arrow.mouse_leave(setting_arrow_mouse_leave, btn = btn_right_arrow, info = setting_info, title = title)
            btn_left_arrow.mouse_up(setting_left_arrow_mouse_up, btn = btn_left_arrow, info = setting_info, title = title)
            btn_left_arrow.mouse_down(setting_arrow_mouse_down, btn = btn_left_arrow)
            btn_left_arrow.mouse_enter(setting_arrow_mouse_enter, btn = btn_left_arrow)
            btn_left_arrow.mouse_leave(setting_arrow_mouse_leave, btn = btn_left_arrow, info = setting_info, title = title)
            # 设置事件穿透，防止上下层级的事件循环传递导致鬼畜
            btn_right_arrow.enabled_event_penetration = True
            btn_left_arrow.enabled_event_penetration = True
            setting_info.children.append(btn_right_arrow)
            setting_info.children.append(btn_left_arrow)
            setting_ui.children.append(setting_info_title)
            setting_ui.children.append(setting_info)
            ui_num += 1
        # =======================================================================================================
        # 淡入效果
        setting_ui_mask.opacity = 0
        setting_ui.opacity = 0
        # 预加载情况下，必须先把子节点推入children渲染列表中，children_together这个参数才有效
        setting_ui_mask.transition_opacity(70, 0.1, fps_clock, children_together = False)
        setting_ui.transition_opacity(255, 0.15, fps_clock)
        # 把遮罩推入渲染UI列表
        scene_manager.now_scene[0].append(setting_ui_mask)

# 箭头按钮进入函数
# noinspection PyUnusedLocal
def setting_arrow_mouse_enter(event: pygame.event.Event, option: dict[str, uiBase.UIBase]):
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

# 箭头按钮离开函数
# noinspection PyUnusedLocal
def setting_arrow_mouse_leave(event: pygame.event.Event, option: dict[str, uiBase.UIBase]):
    btn = option["btn"]
    btn.transition_scale(1, 1, 0.05)
    setting_info = option["info"]
    if not setting_info.name == "未命名":
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

# 箭头按钮按下函数
# noinspection PyUnusedLocal
def setting_arrow_mouse_down(event: pygame.event.Event, option: dict[str, uiBase.UIBase]):
    btn = option["btn"]
    btn.transition_scale(1.3, 1.3, 0.05)
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)


# 右箭头按钮鼠标抬起函数
def setting_right_arrow_mouse_up(event: pygame.event.Event, option: dict[str, uiBase.UIBase | str]):
    # 通知父级已捕获到事件
    event.has_catch = True
    btn = option["btn"]
    setting_info = option["info"]
    btn.enabled_event = True
    title = option["title"]
    btn.transition_scale(1, 1, 0.05)
    if title == "窗口大小":
        pass
    elif title == "游戏帧率":
        index = FPS_PRESET.index(get_config("FPS"))
        if index + 1 < len(FPS_PRESET):
            now_fps = FPS_PRESET[index + 1]
            setting_info.set_text(str(now_fps) + " FPS")
            get_config_all()["FPS"] = now_fps
            scene_manager.FPS_CLOCK = 1 / now_fps


    elif title == "背景音乐":
        now_volume = get_config("volume")
        now_volume = round(now_volume + 0.1,1)
        if now_volume <= 1:
            setting_info.set_text(str(int(now_volume*100)))
            get_config_all()["volume"] = now_volume
            pygame.mixer.music.set_volume(now_volume)

    elif title == "玩家名称":
        player_names = get_config("player_names")
        name_index = player_names.index(setting_info.name)
        if name_index - 1 >= 0:
            name = player_names[name_index - 1]
            setting_info.set_text(name)
            setting_info.name = name
            get_config_all()["player_name_index"] = name_index - 1

# 左箭头按钮鼠标抬起函数
def setting_left_arrow_mouse_up(event: pygame.event.Event, option: dict[str, uiBase.UIBase | str]):
    # 通知父级已捕获到事件
    event.has_catch = True
    btn = option["btn"]
    btn.enabled_event = True
    setting_info = option["info"]
    title = option["title"]
    btn.transition_scale(1, 1, 0.05)
    if title == "窗口大小":
        pass
    elif title == "游戏帧率":
        index = FPS_PRESET.index(get_config("FPS"))
        if index - 1 >= 0:
            now_fps = FPS_PRESET[index - 1]
            setting_info.set_text(str(now_fps) + " FPS")
            get_config_all()["FPS"] = now_fps
            scene_manager.FPS_CLOCK = 1 / now_fps


    elif title == "背景音乐":
        now_volume = get_config("volume")
        now_volume = round(now_volume - 0.1,1)
        if now_volume >= 0:
            setting_info.set_text(str(int(now_volume*100)))
            get_config_all()["volume"] = now_volume
            pygame.mixer.music.set_volume(now_volume)

    elif title == "玩家名称":
        player_names = get_config("player_names")
        name_index = player_names.index(setting_info.name)
        if name_index + 1 < len(player_names):
            name = player_names[name_index + 1]
            setting_info.set_text(name)
            setting_info.name = name
            get_config_all()["player_name_index"] = name_index + 1


def setting_info_mouse_up(event: pygame.event.Event, option: dict[str, tuple[uiBase.UIBase] | str | uiBase.UIBase]):
    setting_info = option["info"]
    title = option["title"]
    tips = option["tips"]
    btn_right_arrow: uiBase.UIBase = option["btn"][0]
    btn_left_arrow: uiBase.UIBase = option["btn"][1]
    btn_right_arrow.opacity = 255
    btn_left_arrow.opacity = 255
    btn_left_arrow.enabled_event = True
    btn_right_arrow.enabled_event = True

    if title == "窗口大小":
        btn_right_arrow.opacity = 80
        btn_left_arrow.opacity = 80
        btn_left_arrow.enabled_event = False
        btn_right_arrow.enabled_event = False
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    elif title == "游戏帧率":
        now_fps = get_config("FPS")
        if now_fps == 30:
            btn_left_arrow.opacity = 80
            btn_left_arrow.enabled_event = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        elif now_fps == 240:
            btn_right_arrow.opacity = 80
            btn_right_arrow.enabled_event = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


    elif title == "背景音乐":
        now_volume = get_config("volume")
        if now_volume == 0:
            btn_left_arrow.opacity = 80
            btn_left_arrow.enabled_event = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        elif now_volume == 1:
            btn_right_arrow.opacity = 80
            btn_right_arrow.enabled_event = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    elif title == "玩家名称":
        tips.set_text("知子莫如父")
        if get_config("player_name_index") == 0:
            btn_right_arrow.opacity = 80
            btn_right_arrow.enabled_event = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        if setting_info.name == "未命名":
            btn_left_arrow.opacity = 80
            btn_left_arrow.enabled_event = False
            tips.set_text("点击新建名称")
            if not hasattr(event, "has_catch"):
                create_input_box("新建名称",setting_info = setting_info, callback = change_setting_info_name)

def change_setting_info_name(setting_info: uiBase.UIBase, name: str):
    if name:
        player_names: list = get_config("player_names")
        if name in player_names:
            setting_info.set_text(font_color = (255,0,0))
            return setting_info.set_text("名称已存在")
        player_names.insert(0, name)
        setting_info.set_text(name,font_color = (0,0,0))
        setting_info.name = name
        get_config_all()["player_name_index"] = 0


# 设置选项操作鼠标进入时
# noinspection PyUnusedLocal
def setting_info_mouse_enter(event: pygame.event.Event, option: dict[str, tuple[uiBase.UIBase] | str | uiBase.UIBase]):
    btn_right_arrow: uiBase.UIBase = option["btn"][0]
    btn_left_arrow: uiBase.UIBase = option["btn"][1]
    setting_info = option["info"]
    tips = option["tips"]
    title = option["title"]
    tips.set_text(option["tips_text"])
    btn_left_arrow.display = True
    btn_right_arrow.display = True
    btn_left_arrow.enabled_event = True
    btn_right_arrow.enabled_event = True
    btn_left_arrow.opacity = 255
    hover_sound_effect.play()
    if title == "玩家名称":
        if get_config("player_name_index") == 0:
            btn_right_arrow.opacity = 80
            btn_right_arrow.enabled_event = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        if setting_info.name == "未命名":
            if len(get_config("player_names")) > 1:
                btn_left_arrow.opacity = 80
                btn_left_arrow.enabled_event =False
            else:
                btn_left_arrow.display = False
                btn_right_arrow.display = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            tips.set_text("点击新建名称")

    elif title == "窗口大小":
        btn_left_arrow.enabled_event =False
        btn_right_arrow.enabled_event = False
        btn_right_arrow.opacity = 80
        btn_left_arrow.opacity = 80

    elif title == "游戏帧率":
        now_fps = get_config("FPS")
        if now_fps == 30:
            btn_left_arrow.opacity = 80
            btn_left_arrow.enabled_event = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        elif now_fps == 240:
            btn_right_arrow.opacity = 80
            btn_right_arrow.enabled_event = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    elif title == "背景音乐":
        now_volume = get_config("volume")
        if now_volume == 0:
            btn_left_arrow.opacity = 80
            btn_left_arrow.enabled_event = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        elif now_volume == 1:
            btn_right_arrow.opacity = 80
            btn_right_arrow.enabled_event = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

# 设置选项操作鼠标离开时
# noinspection PyUnusedLocal
def setting_info_mouse_leave(event: pygame.event.Event, option: dict[str, uiBase.UIBase]):
    btn_left_arrow, btn_right_arrow = option["btn"]
    btn_left_arrow.display = False
    btn_right_arrow.display = False
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

press_sound_effect = resources.EFFECT_press
press_sound_effect.set_volume(0.2)


# noinspection PyUnusedLocal
def open_create(screen: pygame.Surface, btn: StartSceneBtn):
    """
    打开致谢UI
    :param screen: 要绘制的surface
    :param btn: 绑定的按钮
    :return:
    """
    if not btn.has_open_ui:
        # 计算出游戏更新循环周期
        fps_clock = scene_manager.FPS_CLOCK
        # 发送一个打开致谢的事件，间接更新渲染视图
        event_manager.post_event("打开致谢")
        btn.has_open_ui = True
        # 创建半透明的黑色遮罩
        create_ui_mask = uiBase.UIBase(screen, 0, 0, (screen_width, screen_height), color=(0, 0, 0))
        # 创建一个背景图片
        create_ui = uiBase.UIBase(screen, 400, 200, (150, 150), enabled_event = False, center_anchor = True)
        create_ui.set_background_image(create_img, use_circular_mask = True)
        # 背景图片设为遮罩子节点，方便管理
        create_ui_mask.children.append(create_ui)
        # 创建一个关闭创建UI的函数
        def close_create_ui(event, option):
            if "mouse_btn" in option and not option["mouse_btn"] == event.button:
                return
            # 防止这傻逼pycharm给我弹一个未使用形参的警告
            if not option == {} or not event:
                pass
            btn.has_open_ui = False
            # 保存配置
            save_config()
            # 淡出
            create_ui_mask.transition_opacity(0, 0.1, fps_clock, children_together=False).then(lambda **options: create_ui_mask.close())
            create_ui.transition_opacity(0, 0.2, fps_clock)
        # 开启遮罩的键盘事件
        create_ui_mask.enabled_keyboard_event = True
        # 将背景图片的鼠标事件开启事件穿透
        create_ui.enabled_event = False
        # 绑定鼠标右键点击关闭创建UI
        create_ui_mask.mouse_up(close_create_ui, mouse_btn=3)
        create_ui_mask.bind_keyboard_callback(pygame.K_ESCAPE, pygame.KEYUP, close_create_ui)
        create_ui_mask.opacity = 0
        create_ui.opacity = 0

        create_title = uiBase.UIBase(screen, 400, 350, (0,0), text = "游戏开发", font_family = font_path, user_font_family = True, center_anchor = True, font_size = 40, font_color = (255, 255, 255), enabled_event = False)
        create_member = uiBase.UIBase(screen, 400, 400, (0, 0), text = "Ni But Crazy", font_family = font_path, user_font_family = True, center_anchor = True, font_size = 30, font_color = (255, 255, 255))
        create_thank = uiBase.UIBase(screen, 400, 460, (0,0), text = "GitHub 开源地址", font_family = font_path, user_font_family = True, center_anchor = True, font_size = 20, font_color = (255, 255, 255))
        create_member.name = "member"
        create_member.opacity = 0
        create_title.opacity = 0
        create_thank.opacity = 0
        create_ui.children.append(create_member)
        create_ui.children.append(create_title)
        create_ui.children.append(create_thank)
        create_member.mouse_enter(lambda event, option: (create_member.set_text(font_color = (150, 150, 205), font_size = 33),pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)))
        create_member.mouse_leave(lambda event, option: (create_member.set_text(font_color = (255, 255, 255), font_size = 30),pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)))
        create_member.mouse_up(lambda event, option: open("https://github.com/NiButCrazy"))

        create_thank.mouse_enter(lambda event, option: (create_thank.set_text(font_color = (150, 150, 205), font_size = 20), pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)))
        create_thank.mouse_leave(lambda event, option: (create_thank.set_text(font_color = (255, 255, 255), font_size = 20), pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)))
        create_thank.mouse_up(lambda event, option: open("https://github.com/oldsky11/chess/tree/pygame"))

        create_ui_mask.transition_opacity(200, 0.1, fps_clock, children_together = False)
        create_ui.transition_opacity(255, 1, fps_clock)
        # 把遮罩推入渲染UI列表
        scene_manager.now_scene[0].append(create_ui_mask)

def open_start_game(screen: pygame.Surface):
    scene_manager.smooth_toggle_scene(screen,"game")
    event_manager.post_event("打开开始游戏")
