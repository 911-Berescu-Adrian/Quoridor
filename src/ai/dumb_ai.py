import random


from src.game.entities import Wall
from src.game.game import AStarSearch


class DumbAI:
    def __init__(self,board):
        self.board_class=board

    def start_ai(self,ans):
        """
        starting the ai by randomly choosing between moving or placing a wall, if there are any
        :return: arguments to place a wall or where to move the player
        """
        if ans==1:
            return self.move_ai()
        else: return self.place_wall_ai()

    def move_ai(self):
        """
        randomly moves player2, but prioritizes going down
        :return: new coords for player2
        """
        row,col=self.board_class.player2
        neighbours=[]
        neigh=(row+1,col)
        if self.coords_in_board(neigh[0], neigh[1]) and not self.board_class.check_if_wall(2, self.board_class,
                neigh[0], neigh[1]) and not self.board_class.check_if_player(2, neigh[0], neigh[1]):
            neighbours.append(neigh)
        neigh=(row,col-1)
        if self.coords_in_board(neigh[0], neigh[1]) and not self.board_class.check_if_wall(2, self.board_class,
                neigh[0], neigh[1]) and not self.board_class.check_if_player(2, neigh[0], neigh[1]):
            neighbours.append(neigh)
        neigh = (row, col + 1)
        if self.coords_in_board(neigh[0], neigh[1]) and not self.board_class.check_if_wall(2, self.board_class,
                                                                                           neigh[0], neigh[
                                                                                               1]) and not self.board_class.check_if_player(
            2, neigh[0], neigh[1]):
            neighbours.append(neigh)
        neigh = (row - 1, col)
        if self.coords_in_board(neigh[0], neigh[1]) and not self.board_class.check_if_wall(2, self.board_class,
                neigh[0], neigh[1]) and not self.board_class.check_if_player(2, neigh[0], neigh[1]):
            neighbours.append(neigh)
        a=0
        if neighbours[0] != (row+1,col):
            a=random.randint(0,len(neighbours)-1)
        return neighbours[a]

                
    def coords_in_board(self,row,col):
        return 0<=row<=8 and 0<=col<=8


    def find_wall_coords(self,player_coord):
        """
        generating possible coords for a wall
        :param player_coord: (x,y) for player2
        :return: list of coords for a wall
        """
        if self.coords_in_board(player_coord[0]-1,player_coord[1]): # up
            if self.coords_in_board(player_coord[0]-1,player_coord[1]+1): # up right
                return [player_coord,(player_coord[0]-1,player_coord[1]),(player_coord[0]-1,player_coord[1]+1),(player_coord[0],player_coord[1]+1)]
            elif self.coords_in_board(player_coord[0]-1,player_coord[1]-1): # up left
                return [player_coord,(player_coord[0]-1,player_coord[1]),(player_coord[0]-1,player_coord[1]-1),(player_coord[0],player_coord[1]-1)]
        elif self.coords_in_board(player_coord[0]+1,player_coord[1]): # down
            if self.coords_in_board(player_coord[0] + 1, player_coord[1] + 1): # down right
                return [player_coord,(player_coord[0]+1,player_coord[1]),(player_coord[0]+1,player_coord[1]+1),(player_coord[0],player_coord[1]+1)]
            elif self.coords_in_board(player_coord[0]+1,player_coord[1]-1): # down left
                return [player_coord,(player_coord[0]+1,player_coord[1]),(player_coord[0]+1,player_coord[1]-1),(player_coord[0],player_coord[1]-1)]

    def astr(self,board,wall_e,player):
        """
        checks if there's a path
        :param board: current board
        :param wall_e: potential wall
        :param player: player2
        :return: bool, False if wall_e blocks every path from player2 to goal, True otherwise
        """
        astar=AStarSearch(2,board)
        board.walls_list.append(wall_e)
        ans=False
        ans_p1=False
        ans_p2=False
        for i in range(0,9):
            ans=astar.a_star_search(board,self.board_class.player1,((0,i)))
            ans_p1=ans_p1 or ans
        for i in range(0,9):
            ans = astar.a_star_search(board, self.board_class.player2, ((8, i)))
            ans_p2 = ans_p2 or ans
        board.walls_list.remove(wall_e)
        ans=ans_p1 and ans_p2
        return ans

    def place_wall_ai(self):
        """
        places a wall, prioritizing placing it near the enemy player or placing it randomly in the matrix if the other
        options aren't valid
        :return: parameters for a wall
        """
        dir=random.randint(1,2)
        if dir==1: dir="h"
        else: dir="v"
        wcords=self.find_wall_coords(self.board_class.player1)
        if self.board_class.validate_wall_coords(Wall(dir, wcords[0],wcords[1],wcords[2],wcords[3])):
            if self.astr(self.board_class,Wall(dir, wcords[0],wcords[1],wcords[2],wcords[3]),2):
                self.board_class.bot_walls -= 1
                return [dir, wcords[0],wcords[1],wcords[2],wcords[3]]
        else:
            while True:
                x=random.randint(0,8)
                y=random.randint(0,8)
                wcords=self.find_wall_coords((x,y))
                if self.board_class.validate_wall_coords(Wall(dir, wcords[0], wcords[1], wcords[2], wcords[3])):
                    if self.astr(self.board_class, Wall(dir, wcords[0], wcords[1], wcords[2], wcords[3]), 2):
                        self.board_class.place_wall(Wall(dir, wcords[0], wcords[1], wcords[2], wcords[3]))
                        self.board_class.bot_walls -= 1
                        return [dir, wcords[0],wcords[1],wcords[2],wcords[3]]

        
