"""
Game of Life imp by O.Gindia
30-09-2020
"""
from typing import Tuple, List
from time import sleep
from random import randint
from asciimatics.screen import Screen


class Board:
    """
    Game of Life Board
    """
    __board: List[bool] = []
    __width: int = 0
    __height: int = 0

    def __init__(self, w: int, h: int):
        self.__board = []
        self.__width = w
        self.__height = h
        for _ in range(w*h):
            self.__board.append(False)

    def add_cell_at_location(self, x: int, y: int) -> None:
        """
        you can use it multiple times before ticks
        """
        self.__board[self.__xy_to_index(x, y)] = True

    def tick(self) -> List[bool]:
        self.__apply_rules()
        return self.__board

    def __apply_rules(self) -> None:
        buffer_board = [False for _ in range(len(self.__board))]
        for index, cell in enumerate(self.__board):
            neighbours_count = self.__get_active_neighbours_count(index)
            life_cond = (2 <= neighbours_count <= 3) and cell
            dead_cond = (neighbours_count == 3) and not cell
            if life_cond or dead_cond:
                buffer_board[index] = True
        self.__board = buffer_board

    def __get_active_neighbours_count(self, i: int) -> int:
        neighbours = self.__get_neighbours_indexs(i)
        result = 0
        try:
            for neighbour in neighbours:
                if self.__board[neighbour]:
                    result += 1
        except IndexError:
            result = 0
        finally:
            return result

    def __get_neighbours_indexs(self, i: int) -> List[int]:
        """
        return:
            indexes of all 8 directions.
        """
        xy = self.__index_to_xy(i)
        x = xy[0]
        y = xy[1]

        if x >= self.__width-1 or y >= self.__height-1 or x-1 < 0 or y-1 < 0:
            return []

        result = []
        result.append(self.__xy_to_index(x, y+1))
        result.append(self.__xy_to_index(x, y-1))
        result.append(self.__xy_to_index(x+1, y+1))
        result.append(self.__xy_to_index(x+1, y-1))
        result.append(self.__xy_to_index(x+1, y))
        result.append(self.__xy_to_index(x-1, y+1))
        result.append(self.__xy_to_index(x-1, y-1))
        result.append(self.__xy_to_index(x-1, y))
        return result

    def __index_to_xy(self, i: int) -> Tuple:
        x = int(i % self.__width)
        y = int(i/self.__width)
        return (x, y)

    def __xy_to_index(self, x: int, y: int) -> int:
        return x + self.__width*y


# UI IMP
update_timer = 0.01


def main(screen):
    width = screen.width
    height = screen.height
    board = Board(width, height)
    while True:
        # logic
        board_state = board.tick()
        # drawing
        for i, cell in enumerate(board_state):
            x = int((i % width))
            y = int((i/width))
            if cell is True:
                screen.print_at('+', x, y, colour=3)
            else:
                screen.print_at('-', x, y, colour=9)
        # input
        ev = screen.get_key()
        if ev in (ord('q'), ord('Q')):
            return
        elif ev in (ord('g'), ord('G')):
            # a small glider
            board.add_cell_at_location(20, 20)
            board.add_cell_at_location(21, 21)
            board.add_cell_at_location(22, 21)
            board.add_cell_at_location(22, 20)
            board.add_cell_at_location(22, 19)
        elif ev in (ord('w'), ord('W')):
            # random shapes
            for _ in range(randint(1, 100)):
                board.add_cell_at_location(
                    randint(1, width-1), randint(1, height-1))

        # refresh
        sleep(update_timer)
        screen.refresh()


if __name__ == '__main__':
    try:
        Screen.wrapper(main)
    except KeyboardInterrupt:
        print('')
