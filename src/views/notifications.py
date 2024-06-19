import flet as ft

class NotificationsPage(ft.Container):
    def __init__(self,page):
        super().__init__()
        
        self.page = page
        self.padding = 200
        self.bgcolor = "#f2ede7"
        self.border_radius = 20
        self.expand = True

        self.content=ft.Image(src="/images/m.png")