# File created by: Liam Newberry
import pygame as pg
from pygame.sprite import Sprite

from app_settings import *

def draw_divider_horizantal(surface:object,color:tuple,y_coord:int,size:int):
    pg.draw.rect(surface,color,[0,y_coord,WIDTH,size])

def draw_divider_vertical(surface:object,color:tuple,x_coord:int,y_coord:int,size:int):
    pg.draw.rect(surface,color,[x_coord,y_coord,size,HEIGHT-y_coord])

def draw_logo_text(surface:object,image:object,space:int):
    image_rect = image.get_rect()
    margin = (space - image_rect[3]) / 2
    image_rect.topleft = (margin,margin)
    surface.blit(image,image_rect)
    text_start = (image_rect[0]+image_rect[2] + 5,image_rect.bottom + 10)
    od = draw_text(surface,"od",text_start,80,SECONDARY_COLOR,"bottomleft")
    ify = draw_text(surface,"ify",od.topright,80,SECONDARY_COLOR)

def draw_nav_bar1(surface:object,elements:list,x_margin:int,y_margin:int,selected:str):
    item_num = len(elements)
    largest_button = 0
    button_list = {}
    if True:#orientation == "vertical":
        spacing = (HEIGHT - y_margin) / item_num
        y_val = spacing / 2 + y_margin
        for item in elements:
            text_rect = draw_text(surface,item.capitalize(),[0,0],50,BLACK,draw=False)
            size = [text_rect[2],text_rect[3]]
            y_coord = y_val - (size[1] / 2)
            button = draw_round_rect(surface,SECONDARY_COLOR,20,[x_margin,y_coord],[size[0]*1.5,size[1]*1.5])
            if item.lower() == selected.lower():
                draw_round_rect(surface,PRIMARY_COLOR,20,[x_margin+5,y_coord+5],
                                [size[0]*1.5-10,size[1]*1.5-10])
                draw_text(surface,item.capitalize(),[button[0]+button[2]/2,button[1]+button[3]/2],
                        50,SECONDARY_COLOR,"center")
            else:
                draw_text(surface,item.capitalize(),[button[0]+button[2]/2,button[1]+button[3]/2],
                        50,PRIMARY_COLOR,"center")
            button_list[item] = button
            y_val += spacing
            if largest_button < button[2]:
                largest_button = button[2]
    return largest_button + x_margin, button_list

def draw_round_rect(surface:object,color:tuple,radius:int,coordinates:list,size:list):
    tl_coords = [coordinates[0]+radius,coordinates[1]+radius]
    tl_circ = pg.draw.circle(surface,color,tl_coords,radius)
    tr_coords = [coordinates[0]+size[0]-radius,coordinates[1]+radius]
    tr_circ = pg.draw.circle(surface,color,tr_coords,radius)
    bl_coords = [coordinates[0]+radius,coordinates[1]+size[1]-radius]
    bl_circ = pg.draw.circle(surface,color,bl_coords,radius)
    br_coords = [coordinates[0]+size[0]-radius,coordinates[1]+size[1]-radius]
    br_circ = pg.draw.circle(surface,color,br_coords,radius)
    l_rect_length = abs(tl_circ.x-tr_circ.x)+2*radius
    l_rect_width = abs(tl_circ.y-bl_circ.y)
    l_rect = pg.draw.rect(surface,color,[tl_circ.x,tl_circ.center[1],l_rect_length,l_rect_width])
    w_rect_length = abs(tl_circ.x-tr_circ.x)
    w_rect_width = abs(tl_circ.y-bl_circ.y)+2*radius
    w_rect = pg.draw.rect(surface,color,[tl_circ.center[0],tl_circ.y,w_rect_length,w_rect_width])
    return [coordinates[0],coordinates[1],size[0],size[1]]

def draw_round_rect2(surface:object,color:tuple,radius:int,rect:list):
    coordinates = [rect[0],rect[1]]
    size = [rect[2],rect[3]]

    tl_coords = [coordinates[0]+radius,coordinates[1]+radius]
    tl_circ = pg.draw.circle(surface,color,tl_coords,radius)
    tr_coords = [coordinates[0]+size[0]-radius,coordinates[1]+radius]
    tr_circ = pg.draw.circle(surface,color,tr_coords,radius)
    bl_coords = [coordinates[0]+radius,coordinates[1]+size[1]-radius]
    bl_circ = pg.draw.circle(surface,color,bl_coords,radius)
    br_coords = [coordinates[0]+size[0]-radius,coordinates[1]+size[1]-radius]
    br_circ = pg.draw.circle(surface,color,br_coords,radius)

    width_rect = [coordinates[0],coordinates[1]+radius,size[0],size[1]-2*radius]
    width_rectangle = pg.draw.rect(surface,color,width_rect)
    height_rect = [coordinates[0]+radius,coordinates[1],size[0]-2*radius,size[1]]
    height_rectangle = pg.draw.rect(surface,color,height_rect)

def draw_text(surface:object,text:str,coordinates:list,pt:int,color:tuple=BLACK,
              align:str="topleft",font:str="ariel",bold:bool=False,italicize:bool=False,draw:bool=True):
    font_name = pg.font.match_font(font, bold, italicize)
    font = pg.font.Font(font_name, pt)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if align == "topleft":
        text_rect.topleft = coordinates
    elif align == "topright":
        text_rect.topright = coordinates
    elif align == "center":
        text_rect.center = coordinates
    elif align == "midtop":
        text_rect.midtop = coordinates
    elif align == "midbottom":
        text_rect.midbottom = coordinates
    elif align == "midleft":
        text_rect.midleft = coordinates
    elif align == "midright":
        text_rect.midright = coordinates
    elif align == "bottomleft":
        text_rect.bottomleft = coordinates
    elif align == "bottomright":
        text_rect.bottomright = coordinates
    if draw:
        surface.blit(text_surface, text_rect)
    return text_rect

def get_round_image(image:object,radius:int):
    image_rect = image.get_rect()
    length, height = image_rect[2], image_rect[3]
    radius_sq = radius * radius
    rounding_coords = []
    colorkey_coords = []
    for column in range(0,radius):
        column_sq = column * column
        for row in range(0,radius):
            row_sq = row * row
            if row_sq + column_sq >= radius_sq:
                rounding_coords.append([column,row])
    for item in rounding_coords:
        top = (radius - item[1]) - 1
        bottom = ((height - radius) + item[1])
        left = (radius - item[0]) - 1
        right = ((length - radius) + item[0])
        colorkey_coords.append([left,top])
        colorkey_coords.append([right,top])
        colorkey_coords.append([left,bottom])
        colorkey_coords.append([right,bottom])
    found_key = False
    for r in range(0,266):
        if found_key:
            break
        for g in range(0,266):
            if found_key:
                break
            for b in range(0,266):
                colorkey = [r,g,b]
                for column in range(0,length):
                    for row in range(0,height):
                        if [column,row] not in colorkey_coords:
                            if image.get_at([column,row]) != (r,g,b,255):
                                found_key = True
                            else:
                                found_key = False
                if found_key:
                    for item in colorkey_coords:
                        image.set_at(item,colorkey)
                    image.set_colorkey(colorkey)
                    return image 
                