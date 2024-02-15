import pygame as pg
from pygame.sprite import Sprite

from app_settings import *
from draw_funcs import *

class Button:
    def __init__(self,surface:pg.Surface,text:str,rect:list,function):
        # Sprite.__init__(self)
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
    def update(self,click:bool):
        newly_selected = False
        pos = pg.mouse.get_pos()
        if collides(self.rect,coordinates=pos) and click:
            newly_selected = True
        self.draw()
        return newly_selected
    def draw(self):
        draw_round_rect(self.surface,SECONDARY_COLOR,20,
                        [self.coordinates[0]+5,self.coordinates[1]+5],
                        [self.size[0]*1.5-10,self.size[1]*1.5-10])
        draw_text(self.surface,self.text,
                  [self.rect[0]+self.rect[2]/2,self.rect[1]+self.rect[3]/2],
                  50,PRIMARY_COLOR,"center")
        
class NavButton(Button):
    def __init__(self,surface:pg.Surface,text:str,text_rect:list,function,selected:bool=False):
        super().__init__(surface,text,text_rect,function)
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