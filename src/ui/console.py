import random

from src.ai.dumb_ai import DumbAI
from src.game.board import Board, in_bounds
import src.game.game
from src.game.entities import Wall


class Console:
    def __init__(self):
        self.board_class=Board()
        self.player_to_move=0


    def run_console(self):
        while True:
            play_mode=input("choose:\n1. human vs ai\n2. human vs human\n")

            # rps

            if play_mode=="1":
                print("let's settle who will start first the classic way: a fair game of rock-paper-scissors")
                rps_done=0
                while rps_done==0:
                    print("choose:")
                    print("1. rock")
                    print("2. paper")
                    print("3. scissors")
                    human_rps_choice=int(input())
                    ai_rps_choice=random.randint(1,3)
                    result=src.game.game.rps(human_rps_choice,ai_rps_choice)
                    rps_list=["rock","paper","scissors"]
                    print(rps_list[human_rps_choice-1]+" vs "+rps_list[ai_rps_choice-1])
                    if result==0:
                        print("tie!")
                    elif result==1:
                        print("you win!")
                    elif result==-1:
                        print("you lost!")
                    self.player_to_move=1+(result==-1)
                    if result!=0: rps_done=1
            elif play_mode=="2":
                print("just rock-paper-scissors irl for first to move")
                self.player_to_move=1
            else: print("please type 1 or 2")


            game_over=0
            while game_over==0:
                if self.player_to_move==1:
                    print("do you want to (m)ove or place a (w)all?")
                    player_choice=input()
                    if player_choice=="m":
                        valid_move=0
                        while valid_move==0:
                            print("where do you want to go?")
                            direction=input("1. up\n2. down\n3. left\n4. right\n")
                            if direction=="1":
                                p1_row=self.board_class.player1[0]-1
                                p1_col=self.board_class.player1[1]
                            elif direction=="2":
                                p1_row = self.board_class.player1[0] + 1
                                p1_col = self.board_class.player1[1]
                            elif direction=="3":
                                p1_row = self.board_class.player1[0]
                                p1_col = self.board_class.player1[1] - 1
                            elif direction=="4":
                                p1_row = self.board_class.player1[0]
                                p1_col = self.board_class.player1[1] + 1
                            if in_bounds(p1_row, p1_col) == False or self.board_class.check_if_wall(
                                    self.player_to_move,self.board_class, p1_row, p1_col)==True or self.board_class.check_if_player(self.player_to_move,p1_row,p1_col)==True:
                                print("illegal move")
                            else:
                                self.board_class.move_player(self.player_to_move,p1_row,p1_col)
                                valid_move=1

                    elif player_choice=="w":
                        valid_wall=0
                        while valid_wall==0:
                            print("insert the coordinates for the wall, e.g. h (1,0), (1,1),(2,1) and (2,0) means there's a horizontal wall of length 2 between those coordinates")
                            dir=input("direction (h/v): ")
                            cord1_x=int(input("x1: "))
                            cord1_y=int(input("y1: "))
                            cord2_x =int( input("x2: "))
                            cord2_y =int( input("y2: "))
                            cord3_x =int( input("x3: "))
                            cord3_y =int( input("y3: "))
                            cord4_x =int( input("x4: "))
                            cord4_y =int( input("y4: "))
                            if (dir=="h" or dir=="v") and in_bounds(cord1_x,cord1_y)==True and in_bounds(cord2_x,cord2_y)==True and in_bounds(cord3_x,cord3_y)==True \
                                    and in_bounds(cord4_x,cord4_y)==True and self.board_class.validate_wall((cord1_x,cord1_y))==True\
                                    and self.board_class.validate_wall((cord2_x,cord2_y))==True and self.board_class.validate_wall((cord3_x,cord3_y))==True\
                                    and self.board_class.validate_wall((cord4_x,cord4_y))==True:
                                valid_wall=1
                                print()
                                self.board_class.place_wall(Wall(dir,(cord1_x,cord1_y),(cord2_x,cord2_y),(cord3_x,cord3_y),(cord4_x,cord4_y)))
                            else: print("invalid coordinates, please don't go off the grid")
                    self.print_board()
                    self.print_walls_list()
                    self.player_to_move = 3 - self.player_to_move


                if self.player_to_move==2:
                    if play_mode=="2":
                        print("do you want to (m)ove or place a (w)all?")
                        player_choice = input()
                        if player_choice == "m":
                                valid_move=0
                                while valid_move == 0:
                                    print("where do you want to go?")
                                    direction = input("1. up\n2. down\n3. left\n4. right\n")
                                    if direction == "1":
                                        p2_row = self.board_class.player2[0] - 1
                                        p2_col = self.board_class.player2[1]
                                    elif direction == "2":
                                        p2_row = self.board_class.player2[0] + 1
                                        p2_col = self.board_class.player2[1]
                                    elif direction == "3":
                                        p2_row = self.board_class.player2[0]
                                        p2_col = self.board_class.player2[1] - 1
                                    elif direction == "4":
                                        p2_row = self.board_class.player2[0]
                                        p2_col = self.board_class.player2[1] + 1
                                    if in_bounds(p2_row, p2_col) == False or self.board_class.check_if_wall(
                                            self.player_to_move, self.board_class, p2_row,
                                            p2_col) == True or self.board_class.check_if_player(self.player_to_move,
                                                                                                p2_row, p2_col) == True:
                                        print("illegal move")
                                    else:
                                        self.board_class.move_player(self.player_to_move, p2_row, p2_col)
                                        valid_move=1
                        elif player_choice == "w":
                            valid_wall = 0
                            while valid_wall == 0:
                                print(
                                    "insert the coordinates for the wall, e.g. h (1,0), (1,1),(2,1) and (2,0) means there's a horizontal wall of length 2 between those coordinates")
                                dir = input("direction (h/v): ")
                                cord1_x = int(input("x1: "))
                                cord1_y = int(input("y1: "))
                                cord2_x = int(input("x2: "))
                                cord2_y = int(input("y2: "))
                                cord3_x = int(input("x3: "))
                                cord3_y = int(input("y3: "))
                                cord4_x = int(input("x4: "))
                                cord4_y = int(input("y4: "))
                                if (dir == "h" or dir == "v") and in_bounds(cord1_x, cord1_y) == True and in_bounds(
                                        cord2_x, cord2_y) == True and in_bounds(cord3_x, cord3_y) == True \
                                        and in_bounds(cord4_x, cord4_y) == True and self.board_class.validate_wall(
                                    (cord1_x, cord1_y)) == True \
                                        and self.board_class.validate_wall(
                                    (cord2_x, cord2_y)) == True and self.board_class.validate_wall(
                                    (cord3_x, cord3_y)) == True \
                                        and self.board_class.validate_wall((cord4_x, cord4_y)) == True and self.astr(self.board_class,Wall(dir,(cord1_x,cord1_y),(cord2_x,cord2_y),(cord3_x,cord3_y),(cord4_x,cord4_y))):

                                    valid_wall = 1
                                    self.board_class.place_wall(Wall(dir,(cord1_x,cord1_y),(cord2_x,cord2_y),(cord3_x,cord3_y),(cord4_x,cord4_y)))
                                else:
                                    print("invalid coordinates, please don't go off the grid")
                    elif play_mode=="1":
                        ai = DumbAI(self.board_class)
                        ans = 1
                        if self.board_class.bot_walls > 0:
                            ans = random.randint(1, 2)
                        call = ai.start_ai(ans)
                        if call[0] == 'h' or call[0] == 'v':
                            self.board_class.place_wall(Wall(call[0],call[1],call[2],call[3],call[4]))
                            self.p2_walls = self.board_class.bot_walls
                        else:
                            self.board_class.move_player(self.player_to_move, call[0], call[1])

                    self.print_board()
                    self.print_walls_list()
                    self.player_to_move = 3 - self.player_to_move
                if self.board_class.p1_win()==True:
                    print("player 1 won!")
                    game_over=1
                elif self.board_class.p2_win()==True:
                    game_over=1
                    print("player 2 won!")
            return


    def astr(self,board,wall_e):
        astar= src.game.game.AStarSearch(1, board)
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

    def print_board(self):
        for row in range(0,9):
            for col in range(0,9):
                print(self.board_class.board[row][col], end = "   ")
            print()

    def print_walls_list(self):
        print("walls at the following coordinates:")
        for wall in self.board_class.walls_list:
            print(wall)

