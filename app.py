# File created by: Liam Newberry
# External imports
import pygame as pg
# Internal imports
from app_settings import * 
from draw_funcs import *
from excel import *
from objects import *
from pages import *

class Main:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        pg.display.set_caption("Stocks")
        # self.logo_image = pg.image.load(os.path.join(main_folder,"logo.png")).convert()
        # self.logo_image = pg.transform.scale(self.logo_image,(70,70))
        # pg.display.set_icon(self.logo_image)
    def new(self):
        self.running = True
        self.clicked = False
        self.stock_list = get_tickers()
        self.page = "Portfolio"
        self.button_list = []
        self.nav_dict = {"Portfolio":print,
                         "Finance":print,
                         "History":print,
                         "Search":print}
        nav_list, self.x_margin = create_nav_bar(self.screen,self.nav_dict,
                                                 50,0,self.page)
        self.button_list += nav_list
    def events(self):
        self.clicked = False
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP:
                self.clicked = True
            if event.type == pg.QUIT:
                self.running = False
    def update(self):
        self.now = pg.time.get_ticks()
    def draw(self):
        self.screen.fill(PRIMARY_COLOR)
        for button in self.button_list:
            newly_selected = button.update(self.clicked)
            if str(type(button)) == "<class 'objects.NavButton'>" and newly_selected:
                for b in self.button_list:
                    b.selected = False
                button.selected = True
                self.page = button.text
        pg.draw.rect(self.screen,SECONDARY_COLOR,[self.x_margin,0,3,HEIGHT])
        pg.draw.rect(self.screen,(255,0,0),[0,HEIGHT/2,WIDTH,1]) # Temp midline
        # for i in range(1,len(self.stock)):
        #     pg.draw.circle(self.screen,(255,0,0),[i*3,HEIGHT - 3 * int(self.stock[i])],1.5)
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
