import flet as ft

class TimelinePage(ft.Container):
    def __init__(self,page):
        super().__init__()
        
        self.page = page
        self.padding = 20
        self.bgcolor = "#f2ede7"
        self.border_radius = 20
        self.expand = True