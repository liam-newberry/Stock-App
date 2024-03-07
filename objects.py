import pygame as pg
from pygame.sprite import Sprite

from app_settings import *
from draw_funcs import *
from object_funcs import *

class Button:
    def __init__(self,surface:pg.Surface,text:str,rect:list,function,button_color:list,
                 text_color:list,page:str="constant",radius:int=20):
        self.surface = surface
        self.text = text
        self.rect = rect
        self.function = function
        self.coordinates = [rect[0],rect[1]]
        self.size = [rect[2],rect[3]]
        self.x = self.coordinates[0]
        self.y = self.coordinates[1]
        self.width = self.size[0]
        self.height = self.size[1]
        self.button_color = button_color
        self.text_color = text_color
        self.page = page
        self.radius = radius
    def update(self,click:bool):
        newly_selected = False
        pos = pg.mouse.get_pos()
        if collides(self.rect,coordinates=pos) and click:
            newly_selected = True
        self.draw()
        return newly_selected
    def draw(self):
        draw_round_rect2(self.surface,self.button_color,self.radius,self.rect)
        draw_text(self.surface,self.text,
                  [self.x+self.width/2,self.y+self.height/2],
                  int(self.height*1),self.text_color,"center")

class Image:
    pass

class NavButton(Button):
    def __init__(self,surface:pg.Surface,text:str,text_rect:list,function,selected:bool=False):
        super().__init__(surface,text,text_rect,function,SECONDARY_COLOR,PRIMARY_COLOR)
        self.selected = (selected == text)
        self.hover_length = 0
    def update(self,click:bool):
        newly_selected = False
        pos = pg.mouse.get_pos()
        collided = collides(self.rect,coordinates=pos)
        if collided and click:
            newly_selected = True
        self.draw()
        self.hover_animation(collided)
        return newly_selected
    def draw(self):
        button = draw_round_rect(self.surface,SECONDARY_COLOR,20,
                                 self.coordinates,self.size)
        if not self.selected:
            draw_text(self.surface,self.text,[button[0]+button[2]/2,button[1]+button[3]/2],
                      50,PRIMARY_COLOR,"center")
        elif self.selected:
            draw_round_rect(self.surface,PRIMARY_COLOR,20,[self.x+5,self.y+5],
                                [self.width-10,self.height-10])
            draw_text(self.surface,self.text,[button[0]+button[2]/2,button[1]+button[3]/2],
                      50,SECONDARY_COLOR,"center")
    def hover_animation(self,collided:bool):
        if collided:
            self.hover_length += self.width * 0.1
            if self.hover_length > self.width:
                self.hover_length = self.width
        elif not collided:
            self.hover_length -= self.width * 0.1
            if self.hover_length < 0:
                self.hover_length = 0
        x = ((self.width - self.hover_length) / 2) + self.x
        y = self.y + self.height + 5 
        width = int(self.hover_length)
        height = self.height / 10
        pg.draw.rect(self.surface,SECONDARY_COLOR,
                     [x,y,width,height])

class Page():
    def __init__(self,app:object,name:str):
        self.app = app
        self.name = name
        self.object_list = []

class Rectangle():
    pass

class SearchBar():
    def __init__(self,surface:pg.Surface,background_text:str,
                 rect:list,font:str,page:str="constant"):
        self.surface = surface
        self.background_text = background_text
        self.rect = rect
        self.coordinates = [rect[0],rect[1]]
        self.size = [rect[2],rect[3]]
        self.x = self.coordinates[0]
        self.y = self.coordinates[1]
        self.width = self.size[0]
        self.height = self.size[1]
        self.font = font
        self.page = page
        self.clicked = False
        self.typed = ""
        self.last_cursor_blink = 0

        self.inner_bar_margin = 0.1 * self.height
        new_rect = [self.x+self.inner_bar_margin,self.y+self.inner_bar_margin,
                    self.width-(2*self.inner_bar_margin),self.height-(2*self.inner_bar_margin)]
        self.outer_bar = Button(self.surface,"",self.rect,print,SECONDARY_COLOR,BLACK,
                                self.page,radius=25)
        self.inner_bar = Button(self.surface,"Button",new_rect,print,PRIMARY_COLOR,
                                BLACK,self.page,20)
        self.font_size = int(self.inner_bar.height * 0.8)
        self.text_margin = self.inner_bar.height * 0.2
        self.text_coordinates = (self.inner_bar.x + self.text_margin,
                                 self.inner_bar.y + self.inner_bar.height/2)
    def update(self,click:bool,key_up:list):
        pos = pg.mouse.get_pos()
        self.now = pg.time.get_ticks()
        if click:
            if collides(self.rect,coordinates=pos):
                self.clicked = True
                self.last_cursor_blink = self.now
            else:
                self.clicked = False
        if self.now - self.last_cursor_blink >= 2 * CURSOR_BLINK_INTERVAL:    
            self.last_cursor_blink = self.now
        if self.clicked:
            self.typing(key_up)
        self.draw(click)
    def typing(self,key_up:list):
        if key_up == "\x08":
            if len(self.typed) > 0:
                self.typed = self.typed[:-1]
        elif len(self.typed) < 5:
            self.typed += key_up
        elif len(self.typed) == 5:
            pass # insert draw warning message from settings.py
    def draw(self,click:bool):
        self.outer_bar.update(click)
        self.inner_bar.update(click)
        if self.typed == "" and not self.clicked:
            draw_text(self.surface,self.background_text,self.text_coordinates,
                      self.font_size,SEARCH_BAR_BACKGROUND_TEXT_COLOR,align="midleft")
        else:
            pass
            # draw_text("fix this/temporary")
        # self.typed_rect = draw_text(self.surface,"hello",
        #                             self.coordinates,
        #                             50,WHITE,align="midleft")
        # self.typed_rect = draw_text(self.surface,self.typed,
        #                             [self.x + 20, self.y + (self.height/2)],
        #                             30,BLACK,align="midleft")
        # print(True)
        if self.clicked:
            self.clicked_animation()
    def clicked_animation(self):
        if self.now - self.last_cursor_blink <= CURSOR_BLINK_INTERVAL:
            typed_rect = draw_text(self.surface,self.typed,[0,0],self.font_size,draw=False)
            cursor_rect = [self.inner_bar.x + self.text_margin + typed_rect[2],
                           self.inner_bar.y + (self.inner_bar.height * 0.1),
                           CURSOR_WIDTH,
                           self.inner_bar.height * 0.8]
            pg.draw.rect(self.surface,WHITE,cursor_rect)

def collides(rect1:list,rect2:list=None,coordinates:list=None):
    if rect2 != None:
        rect1_x = rect1[0]
        rect1_y = rect1[1]
        rect1_width = rect1[2]
        rect1_height = rect1[3]
        rect2_x = rect2[0]
        rect2_y = rect2[1]
        rect2_width = rect2[2]
        rect2_height = rect2[3]
        if rect1_x >= rect2_x and rect1_x <= rect2_x + rect2_width:
            return True
        elif rect1_y >= rect2_y and rect1_y <= rect2_y + rect2_height:
            return True
        elif rect2_x >= rect1_x and rect2_x <= rect1_x + rect1_width:
            return True
        elif rect2_y >= rect1_y and rect2_y <= rect1_y + rect1_height:
            return True
        else:
            return False
    elif coordinates != None:
        rect_x = rect1[0]
        rect_y = rect1[1]
        rect_width = rect1[2]
        rect_height = rect1[3]
        x = coordinates[0]
        y = coordinates[1]
        if x >= rect_x and x <= rect_x + rect_width:
            if y >= rect_y and y <= rect_y + rect_height:
                return True
        return False

def create_nav_bar(surface:object,elements:dict,x_margin:int,y_margin:int,selected:str):
    item_num = len(elements)
    largest_button = 0
    button_list = []
    spacing = (HEIGHT - y_margin) / item_num
    y_val = spacing / 2 + y_margin
    for item in elements:
        text = item
        text_rect = draw_text(surface,text.capitalize(),[0,0],50,BLACK,draw=False)
        size = [text_rect[2],text_rect[3]]
        y_coord = y_val - (size[1] / 2)
        rect = [x_margin,y_coord,size[0]*1.5,size[1]*1.5]
        function = elements[item]
        button = NavButton(surface,text,rect,function,selected)
        button_list.append(button)
        y_val += spacing
        if largest_button < button.width:
            largest_button = button.width
    return button_list, largest_button + (x_margin * 2)