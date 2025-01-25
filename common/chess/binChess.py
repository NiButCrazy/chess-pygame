"""
士兵棋子
"""


import pygame
from .basicChess import BasicChess
from typing import Literal


class BinChess(BasicChess):

    offset_x = 20
    offset_y = 5
    chess_img_size = (40, 70)

    def __init__(self, screen: pygame.Surface,
                 x: int, y: int, size: int,
                 chess_color: Literal["white", "black"],
                 chess_name: Literal["P1", "P2"]
                 ):
        super().__init__(screen, x, y, size, "bin", chess_color, chess_name)







        