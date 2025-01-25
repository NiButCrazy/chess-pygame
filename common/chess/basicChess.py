"""
棋子的基类
"""


import pygame
from common.uiBase import UIBase
from common import resources
from common.gameMap import GameMap
from typing import Literal


class BasicChess(UIBase):
    """
    棋子的基类,包含基础信息
    """

    offset_x: int  # 棋子图片的 x 偏移量
    offset_y: int  # 棋子图片的 y 偏移量
    chess_img_size: tuple[int, int]  # 棋子图片的尺寸
    mouse_mask = pygame.mask.Mask((1, 1), True) # 鼠标的遮罩，方便后续做鼠标相关的碰撞箱处理
    __towards = {'P1': 1, 'P2': -1} # 棋子朝向，1 朝下，-1 朝上

    def __init__(self, screen: pygame.Surface,

                 x: int, y: int,
                 size: int,
                 game_map: GameMap,
                 chess_type: str, chess_color: Literal["white", "black"],
                 chess_name: Literal["P1", "P2"],
                 ):
        """
        创建一个基本的棋子对象
        :param screen: 绘制的屏幕
        :param chess_type: 棋子类型
        :param chess_color: 棋子颜色
        :param chess_name: 棋子标识符，P1 代表上方棋，P2 代表下方棋，也就是两方玩家代表的棋
        :param x: 列表映射的 x 坐标
        :param y: 列表映射的 y 坐标
        :param size: 棋子UI的大小
        :param game_map: 游戏地图，一个 GameMap 实例对象
        """

        self.game_map = game_map
        self.chess_type = chess_type
        self.chess_color = chess_color
        self.chess_name = chess_name
        self.show_outline: Literal['orange', 'red', 'blue', 'purple'] | None = None # 轮廓颜色
        self.list_x = x
        self.list_y = y
        self.relative_x = x * size + 79
        self.relative_y = y * size + 79
        self.block_size = size
        self.chess_hover = False # 判断鼠标是否在当前棋子 Mask 上
        self.selected = False # 判断当前棋子是否被选中
        self.toward = self.__towards[chess_name] # 棋子朝向

        super().__init__(screen, self.relative_x, self.relative_y, (size, size), color = None)

        # 棋子的图片
        self.chess_img = resources.CHESS_img_map[chess_color][chess_type]
        # 棋子轮廓基础信息
        self.chess_img_outline_pos = (self.relative_x, self.relative_y)
        # 棋子缩放
        self.chess_img = pygame.transform.smoothscale(self.chess_img, self.chess_img_size)
        # 棋子轮廓遮罩
        self.chess_img_mask = pygame.mask.from_surface(self.chess_img)

        # 棋子图片位置
        self.chess_img_pos = (self.relative_x + self.offset_x, self.relative_y + self.offset_y)
        # 通用轮廓字典
        self.outline_dict = {
            'orange': self.create_outline('orange', width = 4),
            'red': self.create_outline('red', width = 4),
            'blue': self.create_outline((0, 198, 255), width = 4),
            'purple': self.create_outline((255, 0, 255), width = 4)
        }


    def create_outline(self, color: tuple[int, int, int] | str, width = 4) -> pygame.Surface:
        """
        创建轮廓
        :param color: 轮廓颜色
        :param width: 轮廓宽度
        :return: 一个填充轮廓颜色的 pygame.Surface 轮廓基底
        """
        # 最基础的轮廓画布
        chess_img_outline = pygame.Surface((self.block_size, self.block_size), pygame.SRCALPHA)
        # #  mask -> surface
        # new_obstacle_surf = self.chess_img_mask.to_surface()
        # #  相同的像素变透明
        # new_obstacle_surf.set_colorkey((0, 0, 0))
        # 绘制轮廓线, 效果一般，性能卓越
        # # 颜色填充
        # surf_w, surf_h = new_obstacle_surf.get_size()
        # for x in range(surf_w):
        #     for y in range(surf_h):
        #         if new_obstacle_surf.get_at((x, y))[0] != 0:
        #             new_obstacle_surf.set_at((x, y), color)

        # self.chess_img_outline.blit(new_obstacle_surf, (obstacle_pos[0] + offset, obstacle_pos[1]))  # right
        # self.chess_img_outline.blit(new_obstacle_surf, (obstacle_pos[0] - offset, obstacle_pos[1]))  # left
        # self.chess_img_outline.blit(new_obstacle_surf, (obstacle_pos[0], obstacle_pos[1] - offset))  # top
        # self.chess_img_outline.blit(new_obstacle_surf, (obstacle_pos[0], obstacle_pos[1] + offset))  # bottom
        # self.chess_img_outline.blit(new_obstacle_surf,
        # (obstacle_pos[0] + offset, obstacle_pos[1] - offset))  # top right
        # self.chess_img_outline.blit(new_obstacle_surf,
        # (obstacle_pos[0] + offset, obstacle_pos[1] + offset))  # bottom right
        # self.chess_img_outline.blit(new_obstacle_surf,
        # (obstacle_pos[0] - offset, obstacle_pos[1] + offset))  # bottom left
        # self.chess_img_outline.blit(new_obstacle_surf,
        # (obstacle_pos[0] - offset, obstacle_pos[1] - offset))  # top left

        # 绘制轮廓线， 效果好，但性能损耗超大
        for point in self.chess_img_mask.outline():
            x = point[0] + self.offset_x
            y = point[1] + self.offset_y
            pygame.draw.circle(chess_img_outline, color, (x, y), width)

        return chess_img_outline

    def update(self, fps_clock):
        super().update(fps_clock)

        # 只在 UI 处于 hover 状态范围内进行碰撞箱计算，节省大量性能开销
        if self.is_hover:
            # 使用遮罩进行碰撞检测
            if self.mouse_in_mask(self.chess_img_mask):
                if not self.chess_hover:
                    # 以下代码只会在鼠标进入时仅执行一次，避免重复绘制，浪费资源
                    self.chess_hover = True
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    # 如果未处于选中状态
                    if not self.selected:
                        self.show_outline = 'blue'
            else:
                if self.chess_hover:
                    # 以下代码只会在鼠标进入时仅执行一次，避免重复绘制，浪费资源
                    self.chess_hover = False
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    # 如果未处于选中状态
                    if not self.selected:
                        self.show_outline = None

        # 绘制轮廓
        if self.show_outline is not None:
            self.screen.blit(self.outline_dict[self.show_outline], self.chess_img_outline_pos)
        # 绘制棋子
        self.screen.blit(self.chess_img, self.chess_img_pos)

    # def _mouse_enter(self, event: pygame.event.Event):
    #     super()._mouse_enter(event)
    #     pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    #     self.show_outline = 'blue'
    #

    def _mouse_leave(self, event: pygame.event.Event):
        super()._mouse_leave(event)
        if not self.selected:
            self.show_outline = None
        # 避免鼠标移动太快导致 Mask 没判断到已离开UI
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.chess_hover = False

    def _mouse_down(self, event: pygame.event.Event):
        super()._mouse_down(event)
        # 鼠标按下时，如果鼠标在遮罩内，则显示轮廓
        if self.mouse_in_mask(self.chess_img_mask):
            self.show_outline = 'orange'

    def _mouse_up(self, event: pygame.event.Event):
        super()._mouse_up(event)
        # 鼠标按下时，如果鼠标在遮罩内，则执行相关函数
        if self.mouse_in_mask(self.chess_img_mask):
            if not self.selected:
                self.show_outline = 'orange'
                self.game_map.select_chess(self)
            else:
                self.game_map.cancel_select_chess()
                self.show_outline = 'blue'

    def active_map_block(self):
        """
        激活选中状态，具体内容交给子类重写
        :return:
        """
        pass

    def mouse_in_mask(self, mask):
        """
        判断鼠标是否在 mask 实例内，也就是是否发生碰撞
        :return:
        """
        # 获取鼠标位置
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # 转换鼠标位置为相对于精灵的位置
        offset_x = mouse_x - self.relative_x - self.offset_x
        offset_y = mouse_y - self.relative_y - self.offset_y
        return mask.overlap(self.mouse_mask, (offset_x, offset_y))

