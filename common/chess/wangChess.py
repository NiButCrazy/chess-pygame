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



    def active_map_block(self):
        active_block = self.game_map.map_data[self.list_y + self.toward][self.list_x]
        active_block.display = True
        self.game_map.active_block_set.add(active_block)