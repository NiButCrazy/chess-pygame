"""
游戏地图以及部分游戏逻辑
"""

import pygame
from typing import Any, Literal
from common.uiBase import UIBase
from common import resources


class MapBlock:
    """
    地图方块类，记录地图方块信息
    """

    def __init__(self, screen: pygame.Surface, x: int, y: int, size: int, display:bool = True):

        # 防止导致循环引用
        from .chess.basicChess import BasicChess

        self.screen = screen
        self.list_x = x
        self.list_y = y
        self.relative_x = x * size + 79
        self.relative_y = y * size + 79
        self.width = self.height= size
        self.opacity = 255
        self.display = display
        # 初始化绘制区域
        self.rect = pygame.Rect(
            self.relative_x,
            self.relative_y,
            self.width,
            self.height
        )
        self.border = self.create_border(border_width=4, border_color=resources.MAP_BLOCK_BORDER_COLOR)
        self.chess: None | BasicChess = None

    # noinspection PyMethodMayBeStatic
    def receive_event(self, event: pygame.event.Event, **option) -> bool:
        return True

    def update(self, fps_clock):
        """
        游戏更新回调
        :param fps_clock: 帧数频率
        :return:
        """
        if self.display:
            self.screen.blit(self.border, self.rect)

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
        # 信息叠加层已激活的对象集合
        self.active_block_set: set[MapBlock] = set()
        # 存储地图数据的对象
        self.map_data: list[list[MapBlock | None]] = [[ None for _ in range(8)] for _ in range(8)]
        # 注入地图数据
        for y in range(8):
            for x in range(8):
                self.map_data[y][x] = MapBlock(container.screen,x, y, self.block_size, False)
                self.container.children.append(self.map_data[y][x])

        # container.children.append(MapBlock(container.screen, 0, 0, self.block_size))

        # 绘制棋盘
        for row in range(8):
            for col in range(8):
                color = resources.WHITE if (row + col) % 2 == 0 else resources.BLACK
                pygame.draw.rect(self.game_map_base, color, (col * self.block_size + 4,
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
        chess_type_list = ["che", 'ma', 'xiang', 'wang', 'hou', 'xiang', 'ma', 'che']
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
                container.children.append(BinChess(
                    self.container.screen,
                    x, chess_pos[chess_name][0],
                    self.block_size,
                    self,
                    self.chess_color[chess_name],
                    chess_name
                ))
                container.children.append(
                    chess_type_dict[chess_type_list[x]](
                        self.container.screen,
                        x, chess_pos[chess_name][1],
                        self.block_size,
                        self,
                        self.chess_color[chess_name],
                        chess_name
                    )
                )

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

            # self.map_data[list_y][list_x].display = True
            # self.active_block_set.add(self.map_data[list_y][list_x])
            # print(self.active_block_set)

    def cancel_select_chess(self):
        """
        取消任何棋子的选中状态
        :return:
        """
        if self.selected_chess is not None:
            # 使得上一个被选中的棋子取消被选中的状态
            self.selected_chess.selected = False
            self.selected_chess.show_outline = None
            self.selected_chess = None
            for block in self.active_block_set:
                block.display = False
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


