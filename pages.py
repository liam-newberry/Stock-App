# File created by: Liam Newberry

class Page:
    def __init__(self,surface:object,rect:list):
        self.surface = surface
        self.rect = rect
        self.coordinates = [rect[0],rect[1]]
        self.size = [rect[2],rect[3]]
        self.x = rect[0]
        self.y = rect[1]
        self.width = rect[2]
        self.height = rect[3]
                

class Portfolio(Page):
    pass

class Finance(Page):
    pass

class History(Page):
    pass

class Search(Page):
    pass