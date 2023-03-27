

from queue import PriorityQueue

from src.game.board import Board


def rps(choice_human,choice_ai):
    """
    this function determines the outcome of a round of rock-paper-scissors with 2 given inputs
    :param choice_human: 1-rock, 2-paper, 3-scissors
    :param choice_ai: same as the human's, but chosen randomly
    :return: int number representing the human's victory (1), defeat (-1) or a tie (0)
    """
    choice_human-=1
    choice_ai-=1
    if choice_human==choice_ai:
        return 0
    if (choice_human+2)%3==choice_ai:
        return 1
    return -1

class AStarSearch:
    def __init__(self,player,board):
        self.board_class=board
        self.player_to_move=player

    def manhattan_dist(self,current_pos,finish):
        """
        computing the distance between 2 cells, helps with heuristics for a* search
        :param current_pos: the (x,y) coordinates for the current position
        :param finish: (x,y) for for our end goal
        :return: int, the manhattan distance between 2 cells or how much we have to travel to reach our goal
        """
        return abs(current_pos[0]-finish[0])+abs(current_pos[1]-finish[1])

    def coords_in_board(self,row,col):
        return 0<=row<=8 and 0<=col<=8

    def get_neighbours(self,row,col,board):
        """
        finding and validating the neighbours of a given cell, checking if there are any walls or players
        that would stop us from moving to a neighbour
        :param row: x of current cell
        :param col: y of current cell
        :param board: current board
        :return: list of available neighbours
        """
        neighbours=[]
        x,y=board.player1
        board.player1=(row,col)
        neigh=(row-1,col)
        if self.coords_in_board(neigh[0],neigh[1]) and not board.check_if_wall(self.player_to_move,board,neigh[0],neigh[1]) and not board.check_if_player(self.player_to_move,neigh[0],neigh[1]):
            neighbours.append(neigh)
        neigh=(row+1,col)
        if self.coords_in_board(neigh[0],neigh[1]) and not board.check_if_wall(self.player_to_move,board,neigh[0],neigh[1]) and not board.check_if_player(self.player_to_move,neigh[0],neigh[1]):
            neighbours.append(neigh)
        neigh=(row,col-1)
        if self.coords_in_board(neigh[0],neigh[1]) and not board.check_if_wall(self.player_to_move,board,neigh[0],neigh[1]) and not board.check_if_player(self.player_to_move,neigh[0],neigh[1]):
            neighbours.append(neigh)
        neigh=(row,col+1)
        if self.coords_in_board(neigh[0],neigh[1]) and not board.check_if_wall(self.player_to_move,board,neigh[0],neigh[1]) and not board.check_if_player(self.player_to_move,neigh[0],neigh[1]):
            neighbours.append(neigh)
        board.player1=(x,y)
        return neighbours


    def a_star_search(self,board_class,start,finish):
        """
        a pathfinding algorithm, similar to dijkstra's, but where you also add a heuristic, the manhattan distance 
        between the current cell and the finish
        the basic idea of the algorithm is f(x)=g(x)+h(x), where f is the combined score, g is the number of steps
        made up to that stage and h is the manh. distance from the cell x to the finish 
        we select the cells with the lowest combined score (if equal select lower dist)

        :param board_class: current board
        :param start: the coordinates of player 1 or 2
        :param finish: the first/last row
        :return: bool, True if it finds a path from the player to the finish line and False otherwise
        """
        open=PriorityQueue()
        open.put((self.manhattan_dist(start,finish),self.manhattan_dist(start,finish),start))
        dist_from_start=[[1000 for i in range(9)] for j in range(9)]
        dist_from_start[start[0]][start[1]]=0
        combined_score = [[1000 for i in range(9)] for j in range(9)]
        combined_score[start[0]][start[1]]=self.manhattan_dist(start,finish)
        path={}
        while not open.empty():
            current=open.get()[2]
            if current==finish:
                return True
               # break
            for neigh in self.get_neighbours(current[0],current[1],board_class):
                new_dist=dist_from_start[current[0]][current[1]]+1
                new_comb_score=self.manhattan_dist(neigh,finish)+new_dist

                if new_comb_score<combined_score[neigh[0]][neigh[1]]:
                    combined_score[neigh[0]][ neigh[1]]=new_comb_score
                    dist_from_start[neigh[0]][ neigh[1]]=new_dist
                    open.put((new_comb_score,new_dist,neigh))
                    path[neigh]=current
        return False
        # winning_path={}
        # cell=current
        # while cell!=start:
        #     winning_path[path[cell]]=cell
        #     cell=path[cell]
        # return True


