import random
import time

import pygame

from src.ai.dumb_ai import DumbAI
from src.game.board import Board
from src.game.entities import Wall
from src.game.game import AStarSearch
import src.game.game
from pygame import mixer

pygame.init()


class Gui:
    def __init__(self):
        self.run=True
        self.win_height = 860
        self.win_width = 1375
        self.font = pygame.font.Font('freesansbold.ttf', 33)
        self.human_choice=0
        self.player_to_move=1
        self.board_class=Board()
        self.play_mode=1
        self.hover_walls=[]
        self.delete_hover_walls=[]
        self.p1_walls=10
        self.p2_walls=10

    def pygame_doesnt_have_text(self,window,x,y,width,height,text):
        pygame.draw.rect(window, (234,237,243), (x, y, width, height))
        text_surf = self.font.render(text, True, (100,100,100))
        textRect = text_surf.get_rect()
        textRect.center = (x + width / 2, y + height / 2)
        window.blit(text_surf, textRect)

    def button(self,window,x,y,width,height,text,action,width_inside=None,border_radius=None):
        pygame.draw.rect(window,(234,237,243),(x,y,width,height),width_inside,border_radius)
        text_surf=self.font.render(text,True,(100,100,100))
        textRect = text_surf.get_rect()
        textRect.center=(x+width/2,y+height/2)
        window.blit(text_surf,textRect)
        self.hover_button(window,x,y,width,height,text)

    def is_btn_pressed(self,window,x,y,width,height,text,action):
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds/click.mp3'))
        click = pygame.mouse.get_pressed()
        mousex, mousey = pygame.mouse.get_pos()
        if click[0] == 1 and x < mousex < x + width and y < mousey < y + height:
            action()
            return True
        return False

    def hover_button(self,window,x,y,width,height,text):
        mousex,mousey=pygame.mouse.get_pos()
        if x<mousex<x+width and y<mousey<y+height:
            pygame.draw.rect(window, (234,237,243), (x, y, width, height))
            pygame.draw.polygon(window,(220,38,38),((x,y-10),(x-20,y+height+10),(x+width,y+50),(x+width+20,y-10)))
            text_surf = self.font.render(text, True, (255,255,255))
            textRect = text_surf.get_rect()
            textRect.center = (x+width//2,y+height//2)
            window.blit(text_surf, textRect)

    def start_screen(self):
        window = pygame.display.set_mode((self.win_width // 1, self.win_height // 1))

        window = pygame.display.set_mode((self.win_width//2, self.win_height//2))
        pygame.display.set_caption("fortnite chess")
        colors=[(255,255,255),(255,255,255),(212, 214, 214),(120, 120, 120),(59, 59, 59),(0, 0, 0),(59, 59, 59),(120, 120, 120),(212, 214, 214),(255,255,255),(255,255,255)]
        color_index = -1
        while self.run:
            pygame.time.delay(200)

            font = self.font
            color_index=(color_index+1)%len(colors)
            text = font.render('press start', True, colors[color_index])
            textRect = text.get_rect()
            textRect.center = (self.win_width // 4, self.win_height // 4)
            window.blit(text, textRect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.KEYDOWN:
                    if event.key==pygame.K_SPACE or event.key==pygame.K_RETURN:
                        mixer.music.load("sounds/jazzy.mp3")
                        mixer.music.play(-1)
                        self.main_menu()
            pygame.display.update()
            window.fill((0,0,0))


    def main_menu(self):
        pygame.time.delay(100)
        pygame.display.set_caption("fortnite chess")
        bg=pygame.image.load("images/menu.png")
        window = pygame.display.set_mode((self.win_width, self.win_height))
        while self.run:
            window.blit(bg, (0, 0))
            self.button(window, self.win_width // 2 - 40, self.win_height // 2 - 150, 80, 40, "play",
                        self.select_play_mode_menu, 0, 0)
            self.button(window, self.win_width // 2 - 45, self.win_height // 2 - 60, 100, 40, "about",
                        self.help_menu, 0, 0)
            self.button(window, self.win_width // 2 - 67, self.win_height // 2 + 30, 145, 40, "settings",
                        self.settings_menu, 0, 0)
            self.button(window, self.win_width // 2 - 40, self.win_height // 2 + 120, 80, 40, "quit",
                        quit, 0, 0)
            for event in pygame.event.get():
                if event.type==pygame.MOUSEBUTTONDOWN:
                    self.is_btn_pressed(window, self.win_width // 2 - 40, self.win_height // 2 - 150, 80, 40, "play",self.select_play_mode_menu)
                    self.is_btn_pressed(window, self.win_width // 2 - 45, self.win_height // 2 - 60, 100, 40, "about",self.help_menu)
                    self.is_btn_pressed(window, self.win_width // 2 - 67, self.win_height // 2 + 30, 145, 40, "settings",self.settings_menu)
                    self.is_btn_pressed(window, self.win_width // 2 - 40, self.win_height // 2 + 120, 80, 40, "quit",quit)
                if event.type == pygame.QUIT:
                    self.run = False
            pygame.display.update()



    def help_menu(self):
        pygame.time.delay(100)
        window = pygame.display.set_mode((self.win_width, self.win_height))
        while self.run:
            bg = pygame.image.load("images/menu.png")
            window.blit(bg, (0, 0))
            self.pygame_doesnt_have_text(window,600,200,100,20,"quoridor is a 2-player board game where your goal is to")
            self.pygame_doesnt_have_text(window, 500, 250, 100, 20,
                                         "get your pawn to the other side of the 'map'")
            self.pygame_doesnt_have_text(window, 590, 350, 100, 20,
                                         "you can use walls to block your opponent's moves and")
            self.pygame_doesnt_have_text(window, 465, 400, 100, 20,
                                         "create a maze-like structure by the end")
            self.pygame_doesnt_have_text(window, 650, 500, 100, 20,
                                         "you can move up, down, left and right and place up to 10 walls")
            self.button(window, self.win_width // 2 - 40, self.win_height - 260, 80, 40, "back",
                        self.main_menu, 0, 0)
            for event in pygame.event.get():
                if event.type==pygame.MOUSEBUTTONDOWN:
                    self.is_btn_pressed(window, self.win_width // 2 - 40, self.win_height - 260, 80, 40, "back",self.main_menu)
                if event.type == pygame.QUIT:
                    self.run = False
            pygame.display.update()

    def dummy_func(self):
        return

    def settings_menu(self):
        pygame.time.delay(100)
        window = pygame.display.set_mode((self.win_width, self.win_height))
        while self.run:
            bg = pygame.image.load("images/menu.png")
            window.blit(bg, (0, 0))
            self.pygame_doesnt_have_text(window, 360, 300, 100, 20,
                                         "sound volume")
            self.pygame_doesnt_have_text(window, 440+150, 300, 10, 10,
                                         "-")
            self.pygame_doesnt_have_text(window, 480+150, 300, 10, 10,
                                         "+")
            self.pygame_doesnt_have_text(window, 400+150, 300, 10, 10,
                                         "||")
            self.pygame_doesnt_have_text(window, 500, 350, 100, 20,
                                         "download RAM for free (works)")
            self.button(window, 440+150, 300, 10, 10,
                                         "-",None,0,0)
            self.button(window, 480+150, 300, 10, 10,
                                         "+",None,0,0)
            self.button(window, 400+150, 300, 10, 10,
                                         "||",None,0,0)
            self.button(window, self.win_width // 2 - 40, self.win_height - 260, 80, 40, "back",
                        self.main_menu, 0, 0)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.is_btn_pressed(window, self.win_width // 2 - 40, self.win_height - 260, 80, 40, "back",
                                        self.main_menu)
                    if self.is_btn_pressed(window, 440+150, 300, 10, 10,
                                         "-",self.dummy_func):
                        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.1)
                    if self.is_btn_pressed(window, 480+150, 300, 10, 10,
                                         "+",self.dummy_func):
                        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.1)
                    if self.is_btn_pressed(window, 400+150, 300, 10, 10,
                                         "||",self.dummy_func):
                        pygame.mixer.music.stop()
                if event.type == pygame.QUIT:
                    self.run = False
            pygame.display.update()

    def select_play_mode_menu(self):
        pygame.time.delay(100)
        window = pygame.display.set_mode((self.win_width, self.win_height))
        pygame.display.set_caption("fortnite chess")
        while self.run:
            bg = pygame.image.load("images/menu.png")
            window.blit(bg, (0, 0))
            image=pygame.image.load("images/singleplayer.png")
            self.button(window,400,400,100,100,"1p",self.rps_menu_1p,0,0)
            self.button(window, 800, 400, 100, 100, "2p", self.rps_menu_2p, 0, 0)
            window.blit(image, (300, 285))
            image = pygame.image.load("images/twoplayers.png")
            window.blit(image, (700, 300))
            self.button(window, self.win_width // 2 - 40, self.win_height - 260, 80, 40, "back",
                        self.main_menu, 0, 0)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.is_btn_pressed(window, self.win_width // 2 - 40, self.win_height - 260, 80, 40, "back",
                                        self.main_menu)
                    self.is_btn_pressed(window,400,400,100,100,"1p",self.rps_menu_1p)
                    self.is_btn_pressed(window, 800, 400, 100, 100, "2p", self.rps_menu_2p)
                if event.type == pygame.QUIT:
                    self.run = False
            pygame.display.update()

    def rps_human_choice(self,value):
        self.human_choice=value


    def rps_menu_1p(self):
        pygame.time.delay(100)
        res=0
        window = pygame.display.set_mode((self.win_width, self.win_height))
        rps=["rock","paper","scissors"]
        while self.run:
            while res==0:
                bg = pygame.image.load("images/menu.png")
                window.blit(bg, (0, 0))
                self.button(window, 400, 400, 100, 20, "rock", lambda: self.rps_human_choice(1), 0, 0)
                self.button(window, 600, 400, 100, 20, "paper", lambda: self.rps_human_choice(2), 0, 0)
                self.button(window, 800, 400, 100, 20, "scissors", lambda: self.rps_human_choice(3), 0, 0)
                self.button(window, self.win_width // 2 - 40, self.win_height - 260, 80, 40, "back",
                            self.main_menu, 0, 0)
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.is_btn_pressed(window, 400, 400, 100, 100, "rock", lambda: self.rps_human_choice(1))
                        self.is_btn_pressed(window, 600, 400, 100, 100, "paper", lambda: self.rps_human_choice(2))
                        self.is_btn_pressed(window, 800, 400, 100, 100, "scissors", lambda: self.rps_human_choice(3))
                        self.is_btn_pressed(window, self.win_width // 2 - 40, self.win_height - 260, 80, 40, "back",
                                            self.select_play_mode_menu)
                    if event.type == pygame.QUIT:
                        self.run = False
                        quit()
                if self.human_choice:
                    ai_choice = random.randint(1, 3)
                    res = src.game.game.rps(self.human_choice, ai_choice)
                    self.pygame_doesnt_have_text(window,600,200,100,20,rps[self.human_choice-1]+" vs "+rps[ai_choice-1])
                    if res==0:
                        self.pygame_doesnt_have_text(window,600,250,100,20,"tie! choose again")
                    elif res==1:
                        self.pygame_doesnt_have_text(window, 600, 250, 100, 20, "you won!")
                    elif res==-1:
                        self.pygame_doesnt_have_text(window, 600, 250, 100, 20, "you lost!")
                        self.player_to_move=2
                pygame.display.update()
            time.sleep(2)
            self.game_board()

    def rps_menu_2p(self):
        pygame.time.delay(100)
        self.play_mode=2
        window = pygame.display.set_mode((self.win_width, self.win_height))
        while self.run:
            bg = pygame.image.load("images/menu.png")
            window.blit(bg, (0, 0))
            self.pygame_doesnt_have_text(window, 600, 200, 100, 100, "play rps in real life to decide who's goes first")
            self.button(window, 600, 400, 150, 20, "continue", self.game_board, 0, 0)
            self.button(window, self.win_width // 2 - 40, self.win_height - 260, 80, 40, "back",
                        self.main_menu, 0, 0)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.is_btn_pressed(window, self.win_width // 2 - 40, self.win_height - 260, 80, 40, "back",
                                        self.select_play_mode_menu)
                    self.is_btn_pressed(window, 600, 400, 150, 20, "continue", self.game_board)
                if event.type == pygame.QUIT:
                    self.run = False
            pygame.display.update()

    def draw_board(self,window):

        for z in self.delete_hover_walls:
            pygame.draw.line(z[0],z[1],z[2],z[3],z[4])
            if z[5]=="hover":
                self.delete_hover_walls.remove(z)

        top_left = (423, 150)
        top_right = (945, 150)
        bottom_right = (1146, 755)
        bottom_left = (221, 755)
        # pygame.draw.polygon(window, [116, 103, 83], (top_left, top_right, bottom_right, bottom_left))
        start = (top_right[0] - top_left[0]) // 9
        stop = (bottom_right[0] - bottom_left[0]) // 9
        starty = (bottom_left[1] - top_left[1]) // 9
        stopy = (bottom_right[1] - top_right[1]) // 9
        for line in range(0, 8):
            pygame.draw.line(window, [86, 67, 67], (top_left[0] + start * (line + 1), top_left[1]),
                             (bottom_left[0] + stop * (line + 1), bottom_right[1]), 14)
            pygame.draw.line(window, [86, 67, 67], (bottom_left[0], (top_left[1] + starty * (line + 1))),
                             (bottom_right[0], (top_right[1] + stopy * (line + 1))), 14)

        pygame.draw.line(window, [86, 67, 67], (top_left[0] + start * (-1 + 1), top_left[1]),
                         (bottom_left[0] + stop * (-1 + 1), bottom_right[1]), 10)  # left board side
        pygame.draw.line(window, [86, 67, 67], (top_left[0] + start * (8 + 1), top_left[1]),
                         (bottom_left[0] + stop * (8 + 1), bottom_right[1]), 12)  # right board side
        pygame.draw.line(window, [86, 67, 67], (bottom_left[0], (top_left[1] + starty * (-1 + 1))),
                         (bottom_right[0], (top_right[1] + stopy * (-1 + 1))), 7)  # top side
        pygame.draw.line(window, [86, 67, 67], (bottom_left[0] - 3, (top_left[1] + starty * (8 + 1))),
                         (bottom_right[0] - 3, (top_right[1] + stopy * (8 + 1))), 18)  # bottom side

        top_left = (423, 150 - 10)
        top_right = (945, 150 - 10)
        bottom_right = (1146, 755)
        bottom_left = (221 - 6, 755)

        pygame.draw.polygon(window, (234,237,243), ((0, 0), top_left, bottom_left, (0, self.win_height)))
        pygame.draw.polygon(window, (234,237,243), ((self.win_width, 0), top_right, bottom_right, (self.win_width, self.win_height)))

        for z in self.hover_walls:
            pygame.draw.line(z[0],z[1],z[2],z[3],z[4])
            if z[5]=="hover":
                self.delete_hover_walls.append([z[0],(116, 103, 83),z[2],z[3],z[4],z[5]])
                self.hover_walls.remove(z)

    def get_board_cell(self,mousex,mousey):
        deltay=755-150
        mousey-=156  # 150 initial y + 6 line width between rows
        row=int(mousey/deltay*9)
        deltax=[]
        for i in range(0,9):
            x_start=423-int(i*(423-221)/9)
            x_end=945+int(i*(1146-945)/9)
            delta_x = x_end - x_start
            deltax.append([x_start, x_end, delta_x])
        mousex-=deltax[row][0] # 423 initial x + 6 line width
        column=int(mousex/deltax[row][2]*9)
        return row,column

    def cell_to_offset(self,window,row,col):
        deltay = 755 - 150
        deltax=[]
        for i in range(0,10):
            x_start=423-int(i*(423-221)/9)
            x_end=945+int(i*(1146-945)/9)
            delta_x=x_end-x_start
            deltax.append([x_start,x_end,delta_x])
        top_left=(deltax[row][0]+int(col*deltax[row][2]/9)+2,int(150+row*deltay/9))
        top_right=(deltax[row][0]+int((col+1)*deltax[row][2]/9)+2,int(150+row*deltay/9))
        bottom_right=(deltax[row+1][0]+int((col+1)*deltax[row+1][2]/9)+2,int(150+(row+1)*deltay/9))
        bottom_left=(deltax[row+1][0]+col*int(deltax[row+1][2]/9)+2,int(150+(row+1)*deltay/9))
        return top_left,top_right,bottom_right,bottom_left

    def check_height(self,mousey):
        return 150<=mousey<=755

    def coords_in_board(self,row,col):
        return 0<=row<=8 and 0<=col<=8

    def check_coords(self,player,row,col):
            if player==1:
                return ((self.board_class.player1[0]==row+1 or self.board_class.player1[0]==row-1) and self.board_class.player1[1]==col) or (self.board_class.player1[0]==row and (self.board_class.player1[1]==col-1 or self.board_class.player1[1]==col+1))
            elif player==2:
                 return ((self.board_class.player2[0]==row+1 or self.board_class.player2[0]==row-1) and self.board_class.player2[1]==col) or (self.board_class.player2[0]==row and (self.board_class.player2[1]==col-1 or self.board_class.player2[1]==col+1))

    def get_neighbours(self,row,col):
        neighbours=[]
        neigh=(row-1,col)
        if self.coords_in_board(neigh[0],neigh[1]) and not self.board_class.check_if_wall(self.player_to_move,self.board_class,neigh[0],neigh[1]) and not self.board_class.check_if_player(self.player_to_move,neigh[0],neigh[1]):
            neighbours.append(neigh)
        neigh=(row+1,col)
        if self.coords_in_board(neigh[0],neigh[1]) and not self.board_class.check_if_wall(self.player_to_move,self.board_class,neigh[0],neigh[1]) and not self.board_class.check_if_player(self.player_to_move,neigh[0],neigh[1]):
            neighbours.append(neigh)
        neigh=(row,col-1)
        if self.coords_in_board(neigh[0],neigh[1]) and not self.board_class.check_if_wall(self.player_to_move,self.board_class,neigh[0],neigh[1]) and not self.board_class.check_if_player(self.player_to_move,neigh[0],neigh[1]):
            neighbours.append(neigh)
        neigh=(row,col+1)
        if self.coords_in_board(neigh[0],neigh[1]) and not self.board_class.check_if_wall(self.player_to_move,self.board_class,neigh[0],neigh[1]) and not self.board_class.check_if_player(self.player_to_move,neigh[0],neigh[1]):
            neighbours.append(neigh)
        return neighbours



    def is_on_color(self,window,color):
        ok = window.get_at(pygame.mouse.get_pos()) == color
        return ok

    def is_vertical_wall(self,mousex,mousey):
        row,col=self.get_board_cell(mousex,mousey)
        if row==8 or col==9:
            return False
        return not self.is_horizontal_wall(mousex,mousey)

    def is_horizontal_wall(self,mousex,mousey):
        deltay = 755 - 150
        deltax = []
        for i in range(0, 10):
            x_start = 423 - int(i * (423 - 221) / 9)
            x_end = 945 + int(i * (1146 - 945) / 9)
            delta_x = x_end - x_start
            deltax.append([x_start, x_end, delta_x])
        row,col=self.get_board_cell(mousex,mousey)
        if row==8 or col==9:
            return False
        return deltax[row+1][0]<=mousex<=deltax[row+1][1]  and abs(mousey-(150+int((row+1)*deltay/9)))<6

    def draw_vertical_wall(self,window,mousex,mousey,text):
        row,col=self.get_board_cell(mousex,mousey)
        if col<8:
            tl,tr,b,bl=self.cell_to_offset(window,row,col)
            tl, a, br, bl = self.cell_to_offset(window, row+1, col)
            self.hover_walls.append([window,(217, 176, 139),tr,br,6,text])
            if text != "hover":
                self.board_class.place_wall(Wall("v", (row, col), (row + 1, col), (row, col + 1), (row + 1, col + 1)))

    def draw_horizontal_wall(self,window,mousex,mousey,text):
        deltay = 755 - 150
        deltax = []
        for i in range(0, 10):
            x_start = 423 - int(i * (423 - 221) / 9)
            x_end = 945 + int(i * (1146 - 945) / 9)
            delta_x = x_end - x_start
            deltax.append([x_start, x_end, delta_x])
        row,col=self.get_board_cell(mousex,mousey)
        if col<=7:
            self.hover_walls.append([window,(217, 176, 139),(deltax[row+1][0]+int(col*deltax[row+1][2]/9)   ,150+int((row+1)*deltay/9)),(deltax[row+1][0]+int((col+2)*deltax[row+1][2]/9)    ,150+int((row+1)*deltay/9)),6,text])
            if text!="hover":
                self.board_class.place_wall(Wall("h", (row, col), (row + 1, col), (row, col + 1), (row + 1, col + 1)))



    def astr(self,board,wall_e,player):
        astar=AStarSearch(1,board)
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


    def game_board(self):
        mixer.music.load("sounds/gametime.mp3")
        mixer.music.play(-1)
        pygame.time.delay(100)
        window = pygame.display.set_mode((self.win_width, self.win_height))
        window.fill((234, 237, 243))
        top_left = (423, 150)
        top_right = (945, 150)
        bottom_right = (1146, 755)
        bottom_left = (221, 755)
        pygame.draw.polygon(window, [116, 103, 83], (top_left, top_right, bottom_right, bottom_left))
        self.draw_board(window)
        pygame.display.update()
        index=0
        colors=[[116, 103, 83],[83, 130, 85],[86, 150, 68],[78, 150, 57],[60, 140, 36],[78, 150, 57],[86, 150, 68],[83, 130, 85],[116, 103, 83]]
        color_index=0
        while self.run:

            if self.board_class.p1_win():
                self.victory_icon(window)
                self.victory_lap()
                time.sleep(7)
                self.run=0
            elif self.board_class.p2_win():
                self.victory_icon(window)
                self.victory_lap()
                time.sleep(7)
                self.run = 0

            pygame.draw.polygon(window, (38, 38, 38), self.cell_to_offset(window, self.board_class.player2[0], self.board_class.player2[1]))
            pygame.draw.polygon(window, (207, 204, 204), self.cell_to_offset(window, self.board_class.player1[0], self.board_class.player1[1]))
            color_index += 1
            color_index %= len(colors)
            mx,my=pygame.mouse.get_pos()
            if self.check_height(my):
                if self.is_on_color(window,(86, 67, 67,255)):
                    if self.is_vertical_wall(mx,my):
                        self.draw_vertical_wall(window,mx,my,"hover")
                    elif self.is_horizontal_wall(mx,my):
                        self.draw_horizontal_wall(window,mx,my,"hover")
                elif not self.is_on_color(window,(234,237,243,255)):
                    mx,my=self.get_board_cell(mx,my)
                    if self.player_to_move==1:
                        if mx==self.board_class.player1[0] and my==self.board_class.player1[1]:
                            neigh=self.get_neighbours(self.board_class.player1[0],self.board_class.player1[1])
                            for i in range(0,len(neigh)):
                                time.sleep(0.07)
                                pygame.draw.polygon(window,colors[color_index],self.cell_to_offset(window,neigh[i][0],neigh[i][1]))
                        else:
                            neigh = self.get_neighbours(self.board_class.player1[0], self.board_class.player1[1])
                            for i in range(0, len(neigh)):
                                time.sleep(0.07)
                                pygame.draw.polygon(window, colors[0],
                                                    self.cell_to_offset(window, neigh[i][0], neigh[i][1]))



                    elif self.player_to_move==2:
                        if self.play_mode==2:
                            if mx == self.board_class.player2[0] and my == self.board_class.player2[1]:
                                neigh = self.get_neighbours(self.board_class.player2[0], self.board_class.player2[1])
                                for i in range(0, len(neigh)):
                                    time.sleep(0.07)
                                    pygame.draw.polygon(window, colors[color_index],
                                                        self.cell_to_offset(window, neigh[i][0], neigh[i][1]))
                            else:
                                neigh = self.get_neighbours(self.board_class.player2[0], self.board_class.player2[1])
                                for i in range(0, len(neigh)):
                                    time.sleep(0.07)
                                    pygame.draw.polygon(window, colors[0],
                                                        self.cell_to_offset(window, neigh[i][0], neigh[i][1]))

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    if index>0:
                        mousex, mousey = pygame.mouse.get_pos()
                        if self.player_to_move==1:
                            if self.is_on_color(window,(116, 103, 83,255)):
                                row,col=self.get_board_cell(mousex, mousey)
                                valid_move=0
                                while valid_move==0:
                                   if (row,col) in self.get_neighbours(self.board_class.player1[0],self.board_class.player1[1]):
                                        valid_move=1
                                        pygame.draw.polygon(window,(116, 103, 83),self.cell_to_offset(window,self.board_class.player1[0],self.board_class.player1[1]))
                                        self.board_class.move_player(self.player_to_move,row,col)
                                        pygame.display.flip()
                            elif self.is_on_color(window,(86, 67, 67,255)) or self.is_on_color(window,(217, 176, 139,255)):
                                mx,my=mousex,mousey
                                row,col=self.get_board_cell(mx,my)
                                if self.board_class.validate_wall_coords(Wall("v",(row,col),(row,col+1),(row+1,col),(row+1,col+1))) and self.p1_walls:
                                    if self.is_vertical_wall(mx, my) and self.astr(self.board_class,Wall("v",(row,col),(row,col+1),(row+1,col),(row+1,col+1)),1):



                                        self.draw_vertical_wall(window, mx, my, "yo")
                                        self.p1_walls-=1
                                    elif self.is_horizontal_wall(mx, my) and self.astr(self.board_class,Wall("h",(row,col),(row,col+1),(row+1,col),(row+1,col+1)),1):



                                        self.draw_horizontal_wall(window, mx, my, "yo")
                                        self.p1_walls -= 1
                            self.player_to_move = 3 - self.player_to_move


                        elif self.player_to_move==2:
                            if self.play_mode==2:
                                if self.is_on_color(window, (116, 103, 83, 255)):
                                    row, col = self.get_board_cell(mousex, mousey)
                                    valid_move=0
                                    while valid_move==0:
                                        if (row,col) in self.get_neighbours(self.board_class.player2[0],self.board_class.player2[1]):
                                            valid_move=1
                                            pygame.draw.polygon(window, (116, 103, 83),
                                                                self.cell_to_offset(window, self.board_class.player2[0],
                                                                                    self.board_class.player2[1]))
                                            self.board_class.move_player(self.player_to_move, row, col)
                                            pygame.display.flip()
                                elif self.is_on_color(window,(86, 67, 67,255)) or self.is_on_color(window,(217, 176, 139,255)):
                                    mx, my = mousex, mousey
                                    row, col = self.get_board_cell(mx, my)
                                    if self.board_class.validate_wall_coords(Wall("v",(row,col),(row,col+1),(row+1,col),(row+1,col+1))) and self.p2_walls:
                                        if self.is_vertical_wall(mx, my) and self.astr(self.board_class,Wall("v",(row,col),(row,col+1),(row+1,col),(row+1,col+1)),2):
                                            self.draw_vertical_wall(window, mx, my, "yo")
                                            self.p2_walls -= 1
                                        elif self.is_horizontal_wall(mx, my) and self.astr(self.board_class,Wall("h",(row,col),(row,col+1),(row+1,col),(row+1,col+1)),2):
                                            self.draw_horizontal_wall(window, mx, my, "yo")
                                            self.p2_walls -= 1
                            elif self.play_mode==1:
                                ai=DumbAI(self.board_class)
                                ans = 1
                                if self.board_class.bot_walls > 0:
                                    ans = random.randint(1, 2)
                                call=ai.start_ai(ans)
                                if call[0]=='h' or call[0]=='v':
                                    self.p2_walls=self.board_class.bot_walls
                                    self.board_class.place_wall(Wall(call[0],call[1],call[2],call[3],call[4]))
                                    mousex,mousey=self.cell_to_offset(window,call[1][0],call[1][1])[0]
                                    mousex+=5
                                    mousey+=5
                                    if call[0]=='h':
                                        self.draw_horizontal_wall(window,mousex,mousey,"yo")
                                    else: self.draw_vertical_wall(window,mousex,mousey,"yo")
                                else:
                                    pygame.draw.polygon(window, (116, 103, 83),self.cell_to_offset(window, self.board_class.player2[0],
                                                                            self.board_class.player2[1]))
                                    self.board_class.move_player(self.player_to_move, call[0], call[1])
                                    pygame.display.flip()

                            self.player_to_move = 3 - self.player_to_move

                    index+=1
                if event.type == pygame.QUIT:
                    self.run = False

            self.draw_board(window)
            if self.board_class.p1_win():
                self.victory_icon(window)
            elif self.board_class.p2_win():
                self.victory_icon(window)
            self.pygame_doesnt_have_text(window, 100, 20,200, 50, "p1 walls: " + str(self.p1_walls))
            self.pygame_doesnt_have_text(window, 1000, 20, 200, 50, "p2 walls: " + str(self.p2_walls))
            pygame.display.update()

    def victory_lap(self):
        mixer.music.load("sounds/victory.mp3")
        mixer.music.play()
        time.sleep(7)

    def victory_icon(self,window):
        image = pygame.image.load("images/vicroyale.png")
        window.blit(image, (500, 300))


