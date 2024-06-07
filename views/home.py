import flet as ft

class HomePage(ft.Container):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.padding = 20
        self.bgcolor = ft.colors.WHITE
        self.border_radius = 10
        self.expand = True