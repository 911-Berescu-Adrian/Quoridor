import unittest

from src.ai.dumb_ai import DumbAI
from src.game.board import Board
from src.game.entities import Wall
from src.game.game import rps, AStarSearch


class RepoTest(unittest.TestCase):
    def setUp(self) -> None:
        self.board_class=Board()


    def tearDown(self) -> None:
        pass

    def test_rps(self):
        res=rps(1,2)
        self.assertEqual(res,-1)
        res = rps(1, 3)
        self.assertEqual(res, 1)
        res = rps(1, 1)
        self.assertEqual(res, 0)

    def test_game(self):
        astar=AStarSearch(1,self.board_class)
        self.assertEqual(astar.a_star_search(self.board_class,self.board_class.player1,((0,0))),True)
        self.assertEqual(astar.a_star_search(self.board_class, self.board_class.player2, ((8, 0))), True)
        self.board_class.place_wall(Wall("h",(7,0),(8,0),(7,1),(8,1)))
        self.board_class.place_wall(Wall("h", (7, 1), (8, 1), (7, 2), (8, 2)))
        self.board_class.place_wall(Wall("h", (7, 2), (8, 2), (7, 3), (8, 3)))
        self.board_class.place_wall(Wall("h", (7, 3), (8, 3), (7, 4), (8, 4)))
        self.board_class.place_wall(Wall("h", (7, 4), (8, 4), (7, 5), (8, 5)))
        self.board_class.place_wall(Wall("h", (7, 5), (8, 5), (7, 6), (8, 6)))
        self.board_class.place_wall(Wall("v", (7, 5), (8, 5), (7, 6), (8, 6)))
        self.board_class.place_wall(Wall("h", (7, 6), (8, 6), (7, 7), (8, 7)))
        self.board_class.place_wall(Wall("h", (7, 7), (8, 7), (7, 8), (8, 8)))
        self.board_class.place_wall(Wall("h", (6, 7), (7, 7), (6, 8), (7, 8)))
        self.assertEqual(astar.a_star_search(self.board_class, self.board_class.player1, ((0, 0))), False)
        self.assertEqual(astar.a_star_search(self.board_class, self.board_class.player2, ((8, 0))), False)
        self.board_class.move_player(1,7,4)
        self.assertEqual(self.board_class.player1,(7,4))
        self.board_class.move_player(2, 1, 4)
        self.assertEqual(self.board_class.player2, (1, 4))
        self.assertEqual(self.board_class.check_if_player(2,7,4),True)
        self.assertEqual(self.board_class.p1_win(),False)
        self.assertEqual(self.board_class.p2_win(), False)
        a=str(self.board_class.board[0][0])
        self.assertEqual(a,'0')
        self.board_class.player2=(0,0)
        aii = DumbAI(self.board_class)
        aii.find_wall_coords((0,0))
        aii.find_wall_coords((8, 0))
        aii.find_wall_coords((8, 8))
        aii.find_wall_coords((0, 8))
        aii.start_ai(1)
        anotherai = DumbAI(self.board_class)
        anotherai.start_ai(2)
        self.board_class.player2 = (8,8)
        aii = DumbAI(self.board_class)
        aii.start_ai(1)
        anotherai = DumbAI(self.board_class)
        anotherai.start_ai(2)
        self.board_class.player2=(2,0)
        anotherai.move_ai()
        self.board_class.place_wall(Wall("v", (5, 5), (5, 4), (6, 5), (6, 4)))
        self.board_class.place_wall(Wall("v", (5, 5), (5,4), (6,5), (6, 6)))
        self.board_class.place_wall(Wall("h", (5, 5), (5, 6), (4, 5), (4, 6)))
        self.board_class.player2 = (5, 5)
        aii = DumbAI(self.board_class)
        aii.start_ai(1)
        anotherai = DumbAI(self.board_class)
        anotherai.start_ai(2)
        a=str(self.board_class.walls_list[0])
        self.assertEqual(a,'h (7, 0) (8, 0) (7, 1) (8, 1)')
        self.assertEqual(self.board_class.validate_wall_coords(Wall("h", (7, 6), (8, 6), (7, 7), (8, 7))),False)
        self.assertEqual(self.board_class.validate_wall_coords(Wall("h", (3, 6), (3, 6), (4, 7), (4, 7))), True)
        anotherstar = AStarSearch(2, self.board_class)
        self.assertEqual(anotherstar.a_star_search(self.board_class, self.board_class.player1, ((0, 0))), True)
        self.assertEqual(anotherstar.a_star_search(self.board_class, self.board_class.player2, ((8, 0))), True)



