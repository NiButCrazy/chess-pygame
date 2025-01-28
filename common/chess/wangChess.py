"""
我是秦始皇，vivo 50
"""

import pygame
from .basicChess import BasicChess
from common.gameMap import GameMap
from typing import Literal


class WangChess(BasicChess):

    offset_x = 20
    offset_y = 8
    chess_img_size = (40, 65)

    def __init__(self, screen: pygame.Surface,
                 x: int, y: int, size: int, game_map: GameMap,
                 chess_color: Literal["white", "black"],
                 chess_name: Literal["P1", "P2"]
                 ):
        super().__init__(screen, x, y, size, game_map, "wang", chess_color, chess_name)

        # 记录 P1 和 P2 的王的最初 y 坐标
        self.name_to_list_y = { 'P1': 0, 'P2': 7 }

    def active_map_block(self):
        for v in [-1, 1]:
            for x, y in [[1, 1], [-1, 1], [0, 1], [1,0]]:
                dest_y = self.list_y + y * v
                dest_x = self.list_x + x * v
                if dest_y < 0 or dest_y > 7 or dest_x < 0 or dest_x > 7:
                    continue
                dest_block = self.game_map.map_data[dest_y][dest_x]
                if dest_block.chess is None:
                    dest_block.display = True
                    self.game_map.active_block_set.add(dest_block)
                    # ============ 王车易位 =============== 丑陋的代码，我实在是懒得写了( ´･･)ﾉ(._.`)
                    if self.name_to_list_y[self.chess_name] == self.list_y:
                        if self.list_x == 3:
                            # 可能是 车 的地图块
                            dest_block_2 = self.game_map.map_data[self.list_y][0]
                            # 需要判定为空的地图块
                            dest_block_3 = self.game_map.map_data[self.list_y][1]
                            dest_block_4 = self.game_map.map_data[self.list_y][2]
                            if (dest_block_2.chess and
                                not dest_block_3.chess and
                                not dest_block_4.chess and
                                dest_block_2.chess.chess_name == self.chess_name and
                                dest_block_2.chess.chess_type == 'che'):
                                dest_block_4.display = True
                                dest_block_4.border = 'WangChe'
                                self.game_map.active_block_set.add(dest_block_4)
                                dest_block_4.switch_block = dest_block_2
                        elif self.list_x == 5:
                            # 可能是 车 的地图块
                            dest_block_2 = self.game_map.map_data[self.list_y][7]
                            # 需要判定为空的地图块
                            dest_block_3 = self.game_map.map_data[self.list_y][6]
                            if (dest_block_2.chess and
                                not dest_block_3.chess and
                                dest_block_2.chess.chess_name == self.chess_name and
                                dest_block_2.chess.chess_type == 'che'):
                                dest_block_3.display = True
                                dest_block_3.border = 'WangChe'
                                self.game_map.active_block_set.add(dest_block_3)
                                dest_block_3.switch_block = dest_block_2


                else:
                    # 如果该区域是敌方棋子
                    if dest_block.chess.chess_name != self.chess_name:
                        dest_block.chess.enabled_event = True
                        self.game_map.change_chess_state(dest_block, 'eaten')




    def finish_move(self):
        super().finish_move()
        # ============ 王车易位 ===============
