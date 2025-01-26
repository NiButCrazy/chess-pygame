"""
🐎棋子
"""

import pygame
from .basicChess import BasicChess
from common.gameMap import GameMap
from typing import Literal


class MaChess(BasicChess):

    offset_x = 20
    offset_y = 8
    chess_img_size = (40, 65)

    def __init__(self, screen: pygame.Surface,
                 x: int, y: int, size: int, game_map: GameMap,
                 chess_color: Literal["white", "black"],
                 chess_name: Literal["P1", "P2"]
                 ):
        super().__init__(screen, x, y, size, game_map, "ma", chess_color, chess_name)



    def active_map_block(self):
        for v in [-1, 1]:
            for x, y in [[2, 1], [1, 2], [-1, 2], [-2, 1]]:
                dest_y = self.list_y + y * v
                dest_x = self.list_x + x * v
                if dest_y < 0 or dest_y > 7 or dest_x < 0 or dest_x > 7:
                    continue
                dest_block = self.game_map.map_data[dest_y][dest_x]
                if dest_block.chess is None:
                    dest_block.display = True
                    self.game_map.active_block_set.add(dest_block)
                else:
                    # 如果该区域是敌方棋子
                    if dest_block.chess.chess_name != self.chess_name:
                        self.game_map.change_chess_state(dest_block, 'eaten')