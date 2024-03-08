from string import ascii_uppercase
import pygame as pg
from pygame.sprite import Sprite

from app_settings import *
from draw_funcs import *

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

class ErrorMessage:
    def __init__(self,text_args,time):
        self.text_args = text_args
        self.time = time
        self.last_update = pg.time.get_ticks() - time
    def update(self):
        self.now = pg.time.get_ticks()
        time_passed = self.now - self.last_update
        if time_passed < self.time:
            self.draw()
    def draw(self):
        ta = self.text_args
        if len(ta) == 4:
            draw_text(ta[0],ta[1],ta[2],ta[3])
        else:
            draw_text(ta[0],ta[1],ta[2],ta[3],ta[4],ta[5],ta[6],ta[7],ta[8])
    def renew(self):
        self.last_update = self.now

class Image:
    def __init__(self,surface:pg.Surface,name:str,coordinates:tuple,
                 page:str="constant",colorkey:tuple=None,alpha:int=255):
        self.surface = surface
        self.name = name
        self.coordinates = coordinates
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.page = page
        self.image = pg.image.load(name).convert()
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        print(self.rect)
        self.size = [self.rect[2],self.rect[3]]
        self.width = self.size[0]
        self.height = self.size[1]
        self.colorkey = colorkey
        if colorkey != None:
            self.image.set_colorkey(colorkey)
        self.image.set_alpha(alpha)
    def draw(self):
        self.surface.blit(self.image,self.rect)
    def scale(self,size:tuple):
        self.image = pg.transform.scale(self.image,size)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

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
    def __init__(self,surface:pg.Surface,rect:list,color:tuple,page:str="constant"):
        self.surface = surface
        self.rect = rect
        self.coordinates = [rect[0],rect[1]]
        self.size = [rect[2],rect[3]]
        self.x = rect[0]
        self.y = rect[1]
        self.width = rect[2]
        self.height = rect[3]
        self.color = color
        self.page = page
    def draw(self):
        pg.draw.rect(self.surface,self.color,self.rect)

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
        self.inner_bar = Button(self.surface,"",new_rect,print,PRIMARY_COLOR,
                                BLACK,self.page,20)
        self.font_size = int(self.inner_bar.height * 0.8)
        self.text_margin = self.inner_bar.height * 0.2
        self.text_coordinates = (self.inner_bar.x + self.text_margin,
                                 self.inner_bar.y + self.inner_bar.height/2)
        
        factor = 0.2
        margin = self.inner_bar.height * factor
        size = (1 - (2 * factor)) * self.inner_bar.height
        self.clear_button = Image(self.surface,"clear text.png",
                                  [self.inner_bar.x + self.inner_bar.width - size - margin,
                                   self.inner_bar.y + margin],
                                   colorkey=BLACK)
        self.clear_button.scale([size,size])

        error_message_coordinates = [self.outer_bar.x + self.outer_bar.width/2,
                                     self.outer_bar.y + self.outer_bar.height * 1.2]
        self.error_dict = {"too long":
                           ErrorMessage([self.surface,MAX_TICKER_LENGTH_MESSAGE,
                                        error_message_coordinates,self.font_size,
                                        RED,"midtop",FONT,False,False],
                                        ERROR_MESSAGE_TIME),
                           "too short":
                           ErrorMessage([self.surface,MIN_TICKER_LENGTH_MESSAGE,
                                        error_message_coordinates,self.font_size,
                                        RED,"midtop",FONT,False,False],
                                        ERROR_MESSAGE_TIME),
                           "invalid char":
                           ErrorMessage([self.surface,INVALID_CHAR_MESSAGE,
                                        error_message_coordinates,self.font_size,
                                        RED,"midtop",FONT,False,False],
                                        ERROR_MESSAGE_TIME)}
    def update(self,click:bool,key_up:list):
        pos = pg.mouse.get_pos()
        self.now = pg.time.get_ticks()
        if click:
            if collides(self.rect,coordinates=pos):
                self.clicked = True
                self.last_cursor_blink = self.now
                if collides(self.clear_button.rect,coordinates=pos):
                    self.typed = ""
            else:
                self.clicked = False

        if self.now - self.last_cursor_blink >= 2 * CURSOR_BLINK_INTERVAL:    
            self.last_cursor_blink = self.now

        for message in self.error_dict:
            self.error_dict[message].update()

        if self.clicked:
            self.typing(key_up)
        self.draw(click)
    def typing(self,key_up:list):
        if key_up == "":
            pass
        elif key_up == "\x08":
            if len(self.typed) > 0:
                self.typed = self.typed[:-1]
        elif key_up == "\r":
            if len(self.typed) > 0:
                self.clicked = False
                self.search()
            else:
                self.error_dict["too short"].renew()
        elif len(self.typed) < 5 and key_up in ascii_uppercase:
            self.typed += key_up
        elif len(self.typed) == 5:
            self.error_dict["too long"].renew()
        elif key_up not in ascii_uppercase and key_up != "":
            self.error_dict["invalid char"].renew()
    def draw(self,click:bool):
        self.outer_bar.update(click)
        self.inner_bar.update(click)
        self.clear_button.draw()

        if self.typed == "" and not self.clicked:
            draw_text(self.surface,self.background_text,self.text_coordinates,
                      self.font_size,SEARCH_BAR_BACKGROUND_TEXT_COLOR,align="midleft")
        else:
            draw_text(self.surface,self.typed,self.text_coordinates,self.font_size,
                      SECONDARY_COLOR,align="midleft")

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
    def search(self):
        pass

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