"""
游戏地图以及部分游戏逻辑
"""

import pygame
from typing import Any, Literal, Callable

from common.sceneManager import scene_manager
from common.uiBase import UIBase
from common import resources


class MapBlock:
    """
    地图方块类，记录地图方块信息
    """

    def __init__(self, game_map, x: int, y: int, size: int, display:bool = True):

        # 防止导致循环引用
        from .chess.basicChess import BasicChess

        self.game_map: GameMap = game_map
        self.screen = self.game_map.container.screen
        self.container = self.game_map.container
        self.list_x = x
        self.list_y = y
        self.relative_x = x * size + 79
        self.relative_y = y * size + 79
        self.width = self.height = size
        self.opacity = 255
        self.display = display
        self.switch_block: None | MapBlock = None # 存储一个关联地图块
        # 棋子状态对应的背景色
        self.chess_state_to_bg = {
            'normal': 'orange',
            'special': 'blue',
            'eaten': 'red',
            'LuGuo': 'purple'
        }
        # 初始化绘制区域
        self.rect = pygame.Rect(
            self.relative_x,
            self.relative_y,
            self.width,
            self.height
        )
        # 棋子状态对应的边框色
        self.border_dict = {
            'normal': self.create_border(4, 'orange'),
            'special': self.create_border(4, (0, 198, 255)),
            'eaten': self.create_border(4, 'red'),
            'LuGuo': self.create_border(4, 'purple'),
            'WangChe': self.create_border(4, 'purple')
        }
        self.border: Literal['normal', 'special', 'eaten', 'LuGuo', 'WangChe'] = 'normal'
        self.chess: None | BasicChess = None
        self.hover = False # 鼠标是否在方块上, 只有 Display 为 True 时才绘判断
        # 通用背景字典
        self.block_bg_dict = {
            'orange': self.create_block_bg('orange'),
            'red': self.create_block_bg('red'),
            'blue': self.create_block_bg((0, 198, 255)),
            'purple': self.create_block_bg((255, 0, 255))
        }
        # 方块背景
        self.block_bg: Literal['orange', 'red', 'blue', 'purple'] | None = None

    def create_block_bg(self, color: tuple[int, int, int] | str, opacity = 80):
        # 方块背景色
        block_bg = pygame.Surface((self.width, self.height))
        block_bg.fill(color)
        block_bg.set_alpha(opacity)
        return block_bg

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def receive_event(self, event: pygame.event.Event, **option) -> bool:
        return True

    # noinspection PyUnusedLocal
    def update(self, fps_clock):
        """
        游戏更新回调
        :param fps_clock: 帧数频率
        :return:
        """
        if self.display:
            if self.block_bg:
                self.screen.blit(self.block_bg_dict[self.block_bg], self.rect)
            self.screen.blit(self.border_dict[self.border], self.rect)
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                if not self.hover:
                    self.hover = True
                    # 以下代码仅在鼠标进入时触发一次
                    if self.chess is None:
                        # 设置背景色
                        if self.border == 'normal':
                            self.block_bg = 'orange'
                        elif self.border == 'LuGuo':
                            self.block_bg = 'purple'
                            self.switch_block.chess.show_outline = 'red'
                        elif self.border == 'WangChe':
                            self.block_bg = 'purple'
                            self.switch_block.chess.show_outline = 'green'

                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        # 设置背景色
                        self.block_bg = self.chess_state_to_bg[self.chess.state]

                    self.game_map.hover_block = self
            else:
                if self.hover:
                    self.hover = False
                    # 以下代码仅在鼠标离开时触发一次
                    # 防止鼠标进入其他方块时，鼠标样式被重置上一个方块的离开状态
                    if self.game_map.hover_block is self:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        self.game_map.hover_block = None
                    # 删除背景色
                    self.block_bg = None
                    if self.border == 'LuGuo':
                        self.switch_block.chess.show_outline = None
                    elif self.border == 'WangChe':
                        self.switch_block.chess.show_outline = None


    def create_border(self, border_width, border_color) -> pygame.Surface:

        # 创建一个Surface对象来表示边框
        border_surface = pygame.Surface((self.width + border_width, self.height + border_width),
                                        pygame.SRCALPHA)
        half_border_width = border_width / 2
        # 扩大绘制区域
        self.rect = pygame.Rect(
            self.relative_x - half_border_width,
            self.relative_y - half_border_width,
            self.width + border_width,
            self.height + border_width
        )

        # 绘制边框的四个部分
        pygame.draw.rect(border_surface, border_color, (0, 0, self.width, border_width))  # 上边框
        pygame.draw.rect(border_surface, border_color, (0, self.height, self.width + border_width,
                                                        border_width))  # 下边框
        pygame.draw.rect(border_surface, border_color, (0, 0, border_width, self.height))  # 左边框
        pygame.draw.rect(border_surface, border_color, (self.width, 0, border_width,
                                                        self.height))  # 右边框

        # 设置边框中间部分的透明度
        border_surface.set_alpha(255)
        return border_surface

    def change_border(self, color, width = 4):
        self.border = self.create_border(border_width=width, border_color=color)

    def change_render_index(self, index: int):
        """
        改变自己的渲染层级，防止渲染的时候被其他优先级高的层级覆盖
        :param index: 目标渲染层级
        :return:
        """
        self.container.children.remove(self)
        self.container.children.insert(index, self)

    # 获取渲染层级位于多少
    @property
    def render_index(self):
        return self.container.children.index(self)

    # 相对于地图左上角的位置
    @property
    def relative_pos(self):
        return self.relative_x, self.relative_y

    # 列表坐标
    @property
    def pos(self):
        return self.list_x, self.list_y


class GameMap:
    """
    地图类，负责与外界交互
    """

    def __init__(self, container: UIBase, size: int):
        """
        绘制地图
        :param container: 要绘制的 UIBase 对象
        :param size: 地图大小
        :return:
        """

        # 防止导致循环引用
        from .chess.basicChess import BasicChess

        # 地图大小
        self.size = size
        # 地图背景基底
        self.game_map_base = pygame.Surface((size, size))
        # 父容器UI
        self.container = container
        # 设置边框颜色
        self.game_map_base.fill(resources.MAP_BORDER_COLOR)
        # 边框粗细
        self.map_border = 4
        # 每个方格的大小
        self.block_size = (size - self.map_border * 2) // 8
        # 选中的 chess
        self.selected_chess: BasicChess | None = None
        # 当前首发回合名字, 默认为 P2
        self.round_name: Literal['P1', 'P2'] = 'P2'
        # 保存双方名字对应棋子的字典
        self.chess_dict: dict[Literal['P1', 'P2'], list[BasicChess]] = {'P1': [], 'P2': []}
        # 鼠标当前悬停的方块
        self.hover_block: MapBlock | None = None
        # 信息叠加层已激活的对象集合
        self.active_block_set: set[MapBlock] = set()
        # 存储地图数据的对象
        self.map_data: list[list[MapBlock | None]] = [[ None for _ in range(8)] for _ in range(8)]
        # 注入地图数据
        for y in range(8):
            for x in range(8):
                self.map_data[y][x] = MapBlock(self, x, y, self.block_size, False)
                self.container.children.append(self.map_data[y][x])

        # 绘制棋盘
        for row in range(8):
            for col in range(8):
                color = resources.WHITE if (row + col) % 2 == 0 else resources.BLACK
                pygame.draw.rect(self.game_map_base, color,
                                 (col * self.block_size + 4,
                                        row * self.block_size + 4,
                                        self.block_size,
                                        self.block_size))

        container.set_background_image(self.game_map_base)
        container.mouse_up(self.map_position)

        # 防止导致循环引用
        from .chess import BinChess, CheChess, WangChess, MaChess, HouChess, XiangChess
        # 记录双方玩家的棋子颜色， 默认上黑下白
        self.chess_color = {
            "P1": "black",
            "P2": "white",
        }
        chess_type_list = ["che", 'ma', 'xiang', 'hou', 'wang', 'xiang', 'ma', 'che']
        chess_type_dict = {
            "che": CheChess,
            "ma": MaChess,
            "xiang": XiangChess,
            "wang": WangChess,
            "hou": HouChess,
        }
        chess_pos = {
            "P1": [1, 0],
            "P2": [6, 7]
        }
        # 将棋子放入棋盘
        chess_name: Literal["P1", "P2"]
        for chess_name in ['P1', 'P2']:
            for x in range(8):
                chess_bin = BinChess(
                    self.container.screen,
                    x, chess_pos[chess_name][0],
                    self.block_size,
                    self,
                    self.chess_color[chess_name],
                    chess_name
                )
                chess_other = chess_type_dict[chess_type_list[x]](
                    self.container.screen,
                    x, chess_pos[chess_name][1],
                    self.block_size,
                    self,
                    self.chess_color[chess_name],
                    chess_name
                )

                # 地图方块记录数据
                self.map_data[chess_pos[chess_name][0]][x].chess = chess_bin
                self.map_data[chess_pos[chess_name][1]][x].chess = chess_other

                # 写入回合管理字典
                self.chess_dict[chess_name].append(chess_bin)
                self.chess_dict[chess_name].append(chess_other)

                # 把非当前回合的棋子禁止响应事件
                if not self.round_name == chess_name:
                    chess_bin.enabled_event = False
                    chess_other.enabled_event = False

                container.children.append(chess_bin)
                container.children.append(chess_other)

        self.choose_ui = UIBase(
            container.screen,
            container.pos_x,
            container.pos_x,
            (size, size),
            (0, 0, 0),
            enabled_event = True
        )

        self.choose_ui.display = False
        self.choose_ui.name = 'choose ui'
        self.choose_ui.opacity = 0
        self.container.children.append(self.choose_ui)


    # noinspection PyUnusedLocal
    def map_position(self, event: pygame.event.Event, option: dict[str, Any]):
        """
        映射鼠标位置到地图列表位置
        :param event: 事件对象
        :param option: 携带的的参数
        :return:
        """

        # 如果点击右键
        if event.button == 3:
            self.cancel_select_chess()
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            return

        elif event.button == 1:
            # 相对于地图左上角的位置
            relative_pos_x = event.pos[0] - 79
            relative_pos_y = event.pos[1] - 79
            # 点到边框不会触发，直接返回
            if relative_pos_x < 0 or relative_pos_y < 0:
                return
            # 映射的地图列表位置
            list_x = relative_pos_x // self.block_size
            list_y = relative_pos_y // self.block_size

            dest_block = self.map_data[list_y][list_x]

            if self.selected_chess:
                if dest_block.display and dest_block.chess is None:
                    if dest_block.border == 'LuGuo':
                        dest_block.switch_block.chess.die()
                    # 移动王车
                    che_block = None
                    origin_x = self.selected_chess.list_x
                    origin_y = self.selected_chess.list_y
                    if dest_block.border == 'WangChe':
                        che_block = dest_block.switch_block
                        che_block.chess.show_outline = None
                    # 移动棋子, 带有清屏效果，建议往后放
                    self.selected_chess.move_to(list_x, list_y)
                    # 因为清屏了，所以再判断一次
                    if che_block:
                        che_block.chess.move_to(origin_x, origin_y)
                    # 切换回合
                    self.change_round()


    def cancel_select_chess(self):
        """
        取消所有棋子的选中状态
        :return:
        """
        if self.selected_chess is not None:
            # 使得上一个被选中的棋子取消被选中的状态
            self.selected_chess.selected = False
            self.selected_chess.show_outline = None
            self.selected_chess = None
            self.hover_block = None
            for block in self.active_block_set:
                block.display = False
                if block.chess:
                    # 禁用非当前回合的棋子响应事件
                    if not block.chess.chess_name == self.round_name:
                        block.chess.enabled_event = False
                    block.chess.state = 'normal'
                block.border = 'normal'
                block.switch_block = None
            self.active_block_set.clear()

    def select_chess(self, chess):
        """
        选中棋子
        :param chess: 一个 BasicChess 实例
        :return:
        """
        # from .chess.basicChess import BasicChess
        self.cancel_select_chess()
        self.selected_chess = chess
        self.selected_chess.selected = True
        self.selected_chess.active_map_block()

    def change_chess_state(self, block: MapBlock, state: Literal[
                                                            'normal', 'eaten', 'special'
                                                        ]):
        """
        改变棋子状态与激活对应 block 的特效
        :param block: MapBlock 实例
        :param state: 棋子状态
        :return:
        """
        block.change_render_index(63)
        block.border = state
        block.display = True
        block.chess.state = state
        self.active_block_set.add(block)

    def create_choose_ui(self,
                         title: str,
                         option: dict[str, pygame.Surface],
                         callback: Callable[[str], Any],
                         image_size: tuple[int, int] = (100, 100),
                         remove_text = False
                         ):
        """
        创建一个选择 UI
        :param title: 标题
        :param option: 选择项，是一个字典类型，键-是选项名，值-是选项图片 Surface 实例
        :param callback: 回调函数, 会传入一个最终选项字符串作为参数
        :parameter image_size: 图片大小
        :parameter remove_text: 是否移除文字
        :return: 返回一个 UIBase 实例
        """
        self.choose_ui.children.clear()
        self.choose_ui.enabled_event = True
        self.choose_ui.enabled_event_children = True
        title_ui = UIBase(self.container.screen, 400, 200, (0,0), text = title,
                          font_family = 'font.ttf', user_font_family = True, center_anchor = True,
                          font_size = 40, font_color = (255, 255, 255), enabled_event = False)
        title_ui.opacity = 0
        len_option = len(option)
        # 计算间隔
        jiange = (self.size - len_option * image_size[0])/(len_option + 1)
        index = 1

        for option_title, image in option.items():
            x_pox = 40 + int( ( jiange + image_size[0] ) * index )
            option_ui = UIBase(self.container.screen, x_pox,400,  image_size, center_anchor = True)
            option_ui.set_background_image(image)
            option_text = UIBase(self.container.screen, x_pox, 500, (0, 0), text = option_title,
                                 font_family = 'font.ttf', user_font_family = True, center_anchor = True,
                                 font_size = 30, font_color = (255, 255, 255), enabled_event = False)
            if remove_text:
                option_text.display = False
            self.choose_ui.children.append(option_ui)
            option_ui.children.append(option_text)
            option_ui.mouse_enter(lambda event, o:
                                  (o['ui'].set_text(font_color = (150, 150, 205), font_size = 40),
                                   pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND),
                                   o['ui'].parent_node.transition_scale(1.1, 1.1, 0.05)
                                   ),ui = option_text)
            option_ui.mouse_leave(lambda event, o:
                                  (o['ui'].set_text(font_color = (255, 255, 255), font_size = 30),
                                   pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW),
                                   o['ui'].parent_node.transition_scale(1, 1, 0.05)
                                   ), ui = option_text)
            option_ui.mouse_up(lambda event, o: (self.close_choose_ui(),callback(o['result'])),
                               result = option_title)
            option_ui.opacity = 0
            option_text.opacity = 0
            index += 1

        self.choose_ui.children.append(title_ui)
        self.choose_ui.display = True
        self.choose_ui.transition_opacity(180, duration = 0.4,
                                          children_together = False, fps_clock = scene_manager.FPS_CLOCK
        )# .then(lambda : print(self.choose_ui.display))
        for ui in self.choose_ui.children:
            ui.transition_opacity(255, duration = 0.3, fps_clock = scene_manager.FPS_CLOCK)


    def close_choose_ui(self):
        """
        关闭选项卡 UI 触发的方法
        :return:
        """
        def close():
            self.choose_ui.display = False
        self.choose_ui.transition_opacity(0, duration = 0.3).then(close)
        self.choose_ui.enabled_event = False
        self.choose_ui.enabled_event_children = False
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def change_round(self):
        """
        改变回合
        :return:
        """
        for chess in self.chess_dict[self.round_name]:
            chess.enabled_event = False
        self.round_name: Literal['P1', 'P2'] = 'P1' if self.round_name == 'P2' else 'P2'
        for chess in self.chess_dict[self.round_name]:
            chess.enabled_event = True