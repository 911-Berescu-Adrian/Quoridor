
from src.game.entities import Cell


def in_bounds( x, y):
    return (0 <= x < 9) and (0 <= y < 9)

class Board:
    def __init__(self):
        self.board=[[Cell(0) for i in range(9)] for j in range(9)]
        self.walls_list=[]
        self.board[0][4]="P2"
        self.player2=(0,4)
        self.board[8][4]="P1"
        self.player1=(8,4)
        self.bot_walls=10

    def check_if_wall(self,player,board,new_x,new_y):
        if player==1:
            return self.check_wall_player(board,board.player1,(new_x,new_y))
        elif player==2:
            return self.check_wall_player(board,board.player2,(new_x,new_y))

    def check_wall_player(self,board,player_coords,new_coords):
        """
        checking whether a player's move is legal, depending on each wall's type
        :param board: the current board
        :param player_coords: (x,y) for the player to move
        :param new_coords: new (x,y) for the current player
        :return: bool, True if there is a wall stopping the player from moving, False otherwise
        """
        for wall in board.walls_list:
            for cord1 in wall.coords:
                for cord2 in wall.coords:
                    if cord1==player_coords and cord2==new_coords:
                        if wall.direction=="h":
                            if (cord1[0]==cord2[0]-1 or cord1[0]-1==cord2[0]) and cord1[1]==cord2[1]:
                                return True
                        elif wall.direction=="v":
                            if (cord1[1] == cord2[1] - 1 or cord1[1] - 1 == cord2[1]) and cord1[0]==cord2[0]:
                                return True
        return False

    def check_if_player(self,player,x,y):
        """
        checking if there's another player stopping a possible move
        :param player: player to move
        :param x: new x
        :param y: new y for the player's next possible move
        :return: bool, True if there is a player stopping the player from moving, False otherwise
        """
        player=3-player
        if player==1:
            if x==self.player1[0] and y==self.player1[1]:
                return True
        elif player==2:
            if x==self.player2[0] and y==self.player2[1]:
                return True
        return False

    def move_player(self,player,new_x,new_y):
        """
        simply moves the player in the matrix if the new coords are valid
        :param player: int, player to move
        :param new_x: int
        :param new_y: int
        """
        if in_bounds(new_x,new_y):
            if player==1:
                self.board[self.player1[0]][self.player1[1]]=0
                self.player1=(new_x,new_y)
                self.board[new_x][new_y]="P1"
            elif player==2:
                self.board[self.player2[0]][self.player2[1]] = 0
                self.player2=(new_x,new_y)
                self.board[new_x][new_y]="P2"
        return

    def validate_wall_coords(self,wall):
        """
        if cont<4 it means the new wall doesn't collide with any other wall
        :param wall: new possible wall
        :return: bool, True if the new wall isn't colliding (is valid), False otherwise
        """
        cont=0
        for c in wall.coords:
            if self.validate_wall(c)==False:
                cont+=1
        return cont<4

    def validate_wall(self,cord1):
        """
        if we find one coordinate that's the same we found possible colliding walls
        :param cord1: one coord of a wall
        :return: bool, True if the coords are different, False otherwise
        """
        for wall in self.walls_list:
            for cord in wall.coords:
                if cord==cord1:
                    return False
        return True

    def place_wall(self,wall):
        self.walls_list.append(wall)

    def p1_win(self):
        return self.player1[0]==0

    def p2_win(self):
        return self.player2[0]==8


