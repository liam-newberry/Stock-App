# File created by: Liam Newberry
# External imports
import pygame as pg
# Internal imports
from settings import * 
from draw_funcs import *
from excel import *
from folder_funcs import *
from objects import *

class Main:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        pg.display.set_caption(APP_NAME)
        self.icon_image = get_image("icon.png")
        self.icon_image.set_colorkey(BLACK)
        pg.display.set_icon(self.icon_image)
    def new(self):
        self.running = True
        # {
        self.stock_list = get_tickers() # move to portfolio page
        # }
        self.nav_dict = {"Portfolio":print,
                         "Finance":print,
                         "History":print,
                         "Search":print}
        self.keys_down = []
        self.obj_var_dict = {}
        self.page_list = create_pages(self.screen)
        # self.page = "Portfolio"
        self.page = self.page_list[0]
    def events(self):
        clicked = False
        key_up = ""
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP:
                clicked = True
            if event.type == pg.QUIT:
                self.running = False
            if "unicode" in event.dict:
                key = event.dict["unicode"]
                key = key.upper()
                if key not in self.keys_down:
                    self.keys_down.append(key)
                elif key in self.keys_down:
                    key_up = key
                    self.keys_down.remove(key)
        # update obj_var_dict
        self.obj_var_dict["clicked"] = clicked
        self.obj_var_dict["keys down"] = self.keys_down
        self.obj_var_dict["key up"] = key_up
    def update(self):
        self.now = pg.time.get_ticks()
        
    def draw(self):
        self.screen.fill(PRIMARY_COLOR)
        # update pages
        for page in self.page_list:
            if page.page in ["constant",self.page]:
                page_return_dict = page.update(self.obj_var_dict)
                if page_return_dict["page"] != None:
                    self.page = page_return_dict["page"]
        
        pg.draw.rect(self.screen,(255,0,0),[0,HEIGHT/2,WIDTH,1]) # Temp midline
        pg.display.flip()
    def run(self):
        frames = 0
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            frames += 1
        seconds = pg.time.get_ticks() / 1000
        print("Intended FPS: " + str(FPS) + "\nActual: " + str(frames/seconds))

def app_loop():
    m = Main()
    m.new()
    m.run()
    pg.quit()
    if os.path.exists("temp.xlsx"):
        os.remove("temp.xlsx")