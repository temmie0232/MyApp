import time
import flet as ft
from openai import OpenAI

# OpenAI APIの設定
client = OpenAI()

class ChatPage(ft.Container):
    def __init__(self,page):
        super().__init__()
        
        self.page = page
        self.padding = 20
        self.bgcolor = ft.colors.YELLOW
        self.border_radius = 30
        self.expand = True
        
        self.content = self.create_main_layout()

    
    def create_main_layout(self) -> ft.Column:
        return ft.Column([
            ft.Text("おしゃべりできます", size = 28, weight = "w800"), # type: ignore
            #self.main,
            ft.Divider(height = 6, color = "transparent"),
            #self.prompt,
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )