# File created by: Liam Newberry
# External imports
import pygame as pg
# Internal imports
from settings import * 
from draw_funcs import *
from excel import *
from folder_funcs import *
from objects import *
from pages import *

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
        self.clicked = False
        self.stock_list = get_tickers()
        self.page = "Portfolio"
        self.page_objects = []
        self.nav_dict = {"Portfolio":print,
                         "Finance":print,
                         "History":print,
                         "Search":print}
        nav_list, self.x_margin = create_nav_bar(self.screen,self.nav_dict,
                                                 50,93,self.page)
        for nav_button in nav_list:
            self.page_objects.append(nav_button)
        self.x_margin += 18
        self.page_objects += nav_list
        self.logo_image = get_image("logo.png")
        self.logo_image_rect = self.logo_image.get_rect()
        self.logo_image.set_colorkey(BLACK)
        self.logo_image = pg.transform.scale(self.logo_image,
                                             (LOGO_SCALE * self.logo_image_rect[2],
                                              LOGO_SCALE * self.logo_image_rect[3]))
        self.sb = SearchBar(self.screen,"Input a Ticker",
                            [self.x_margin + ((WIDTH - self.x_margin) * 0.05),
                            HEIGHT * 0.03,
                            (WIDTH - self.x_margin) * 0.9,
                            70],
                            None,page="Search")
        self.keys_down = []
        self.key_up = ""
        self.stock = get_stock("NVDA","2Y")
        # self.sb = SearchBar(self.screen,"Ticker:",[self.x_margin + ((WIDTH - self.x_margin) * 0.05),
        #                                            HEIGHT * 0.03,
        #                                            800,
        #                                            40],None,page="Search")
    def events(self):
        self.clicked = False
        self.key_up = ""
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP:
                self.clicked = True
            if event.type == pg.QUIT:
                self.running = False
            if "unicode" in event.dict:
                key = event.dict["unicode"]
                key = key.upper()
                if key not in self.keys_down:
                    self.keys_down.append(key)
                elif key in self.keys_down:
                    self.key_up = key
                    self.keys_down.remove(key)
    def update(self):
        self.now = pg.time.get_ticks()
    def draw(self):
        self.screen.fill(PRIMARY_COLOR)
        for obj in self.page_objects:
            obj_type = type(obj)
            if obj.page not in ["constant",self.page]:
                self.page_objects.remove(obj)
            if obj_type in [Button,NavButton]:
                newly_selected = obj.update(self.clicked)
            if obj_type == NavButton and newly_selected:
                for button in self.page_objects:
                    button.selected = False
                obj.selected = True
                self.page = obj.text
                # DELETE ME {
                if self.page == "Search" and self.sb not in self.page_objects:
                    self.page_objects.append(self.sb)
                # }
            if obj_type == SearchBar:
                obj.update(self.clicked,self.key_up)
        pg.draw.rect(self.screen,SECONDARY_COLOR,[self.x_margin,0,3,HEIGHT])
        pg.draw.rect(self.screen,(255,0,0),[0,HEIGHT/2,WIDTH,1]) # Temp midline
        self.screen.blit(self.logo_image,(20,25))
        # for i in range(1,len(self.stock)):
        #     pg.draw.circle(self.screen,(255,0,0),
        #                    [self.x_margin + i*4,HEIGHT - 3 * int(self.stock["NVDA"][i]) + 200],1.5)
        #     pg.draw.circle(self.screen,RED,(i*9 + self.x_margin, HEIGHT/2),3)
        # self.sb.update(self.clicked,self.key_up)
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

app_loop()
