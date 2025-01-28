"""
士兵棋子
"""


import pygame
from .basicChess import BasicChess
from common.gameMap import GameMap
from .houChess import HouChess
from .cheChess import CheChess
from .maChess import MaChess
from .xiangChess import XiangChess
from common import resources
from typing import Literal

chess_switch = {
    '皇后': HouChess,
    '车': CheChess,
    '马': MaChess,
    '象': XiangChess
}

class BinChess(BasicChess):

    offset_x = 20
    offset_y = 8
    chess_img_size = (40, 65)

    def __init__(self, screen: pygame.Surface,
                 x: int, y: int, size: int, game_map: GameMap,
                 chess_color: Literal["white", "black"],
                 chess_name: Literal["P1", "P2"]
                 ):
        super().__init__(screen, x, y, size, game_map, "bin", chess_color, chess_name)
        # 记录开局是否移动过两步
        self.move_two_step = False
        # 记录是否移动过
        self.have_moved = False
        # 记录走棋步数
        self.move_step_num = 0



    def active_map_block(self):
        # 解释一下， (not self.have_moved) 作为“布尔值”可以隐性转换为 0 或 1，直接对应了[移动过走一格，没移动走两格]
        for num in range(1, 2 + ( not self.have_moved )):
            dest_y = self.list_y + self.toward * num
            # 抵达地图边缘
            if dest_y < 0 or dest_y > 7:
                continue
            toward_block = self.game_map.map_data[dest_y][self.list_x]
            # 如果正前方没有棋子
            if not toward_block.chess:
                toward_block.display = True
                self.game_map.active_block_set.add(toward_block)
            else: break

        for x in [1, -1]:
            dest_y = self.list_y + self.toward
            dest_x = self.list_x + x
            if dest_y < 0 or dest_y > 7 or dest_x < 0 or dest_x > 7 :
                continue
            dest_block = self.game_map.map_data[dest_y][dest_x]
            # 如果该区域是敌方棋子
            if dest_block.chess and dest_block.chess.chess_name != self.chess_name:
                dest_block.chess.enabled_event = True
                self.game_map.change_chess_state(dest_block, 'eaten')

        # =========== 路过吃兵的代码 ================
        for x in [1, -1]:
            dest_x = self.list_x + x
            if dest_x < 0 or dest_x > 7:
                continue
            # 获取水平面上的左右格子
            near_block = self.game_map.map_data[self.list_y][dest_x]
            near_chess = near_block.chess
            if (near_chess and
                near_chess.chess_type == "bin" and
                not near_chess.chess_name == self.chess_name and
                near_chess.move_two_step and
                near_chess.move_step_num == 1
                ):
                # 获取可以吃的格子
                dest_block = self.game_map.map_data[near_chess.list_y + self.toward][near_chess.list_x]
                if dest_block.chess is None:
                    dest_block.display = True
                    dest_block.border = 'LuGuo'
                    dest_block.switch_block = near_block
                    self.game_map.active_block_set.add(dest_block)
                    dest_block.change_render_index(63)


    def move_to(self, list_x: int, list_y: int):

        # 记录开局是否移动过两步
        if not self.move_two_step:
            # 相对距离
            relative_distance = abs(self.list_y - list_y)
            if relative_distance == 2:
                # 记录开局是否移动过两步
                self.move_two_step = True

        super().move_to(list_x, list_y)

        # 记录是否移动过
        self.have_moved =True
        self.move_step_num += 1

    def finish_move(self):
        super().finish_move()
        # 抵达地图边缘时
        if self.list_y == 0 or self.list_y == 7:
            # 兵的升变
            self.state = 'edge'
            self.show_outline = 'green'
            self.game_map.select_chess(self)
            # self.game_map.container.enabled_event_children = False
            # self.game_map.container.enabled_event = False
            self.game_map.create_choose_ui('选择升变对象', {
                '皇后': resources.CHESS_img_map['white']['hou'],
                '车': resources.CHESS_img_map['white']['che'],
                '马': resources.CHESS_img_map['white']['ma'],
                '象': resources.CHESS_img_map['white']['xiang']
            }, self.become_chess, (70, 120))

    def become_chess(self, chess_type: str):
        """
        变成某个棋子
        :param chess_type: 棋子类型
        :return:
        """
        new_chess: BasicChess = chess_switch[chess_type](
            self.screen, self.list_x, self.list_y, self.block_size,
            self.game_map, self.chess_color, self.chess_name)

        self.die()
        self.game_map.map_data[self.list_y][self.list_x].chess = new_chess
        self.game_map.container.children.insert(65, new_chess)
        self.game_map.cancel_select_chess()

        