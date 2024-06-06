import flet as ft
from views.home import HomePage
from views.search import SearchPage
from views.notifications import NotificationsPage
from views.messages import MessagesPage
from views.chat import ChatPage
from views.profile import ProfilePage
from views.settings import SettingsPage


class MainPage(ft.View):
    def __init__(self, page):
        super().__init__(
            route="/flet/home",
            vertical_alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            bgcolor=ft.colors.WHITE,
        )
        
        self.page = page
        self.bgcolor = "#f0f4f9"
        
        self.rail = self.create_nav_rail()
        self.rail_container = ft.Container(content=self.rail, border_radius=10)
        
        self.views = self.init_views()
        self.content_view = ft.Container(
            content=self.views[0],
            expand=True,
            bgcolor="#ffffff",
            border_radius=10,
        )
        
        
        self.controls = [self.create_main_layout()]
    
    def toggle_extended(self,e):
        self.extended = not self.extended
        self.update()
    
    def create_nav_rail(self):
        destinations = [
            {"icon": ft.icons.HOME_OUTLINED, "selected_icon": ft.icons.HOME, "label": "ホーム"},
            {"icon": ft.icons.SEARCH_OUTLINED, "selected_icon": ft.icons.SEARCH, "label": "検索"},
            {"icon": ft.icons.NOTIFICATIONS_OUTLINED, "selected_icon": ft.icons.NOTIFICATIONS, "label": "通知"},
            {"icon": ft.icons.MAIL_OUTLINED, "selected_icon": ft.icons.MAIL, "label": "メッセージ"},
            {"icon": ft.icons.SPEAKER_NOTES_OUTLINED, "selected_icon": ft.icons.SPEAKER_NOTES, "label": "AIチャット"},
            {"icon": ft.icons.PERSON_OUTLINED, "selected_icon": ft.icons.PERSON, "label": "プロフィール"},
            {"icon": ft.icons.SETTINGS_OUTLINED, "selected_icon": ft.icons.SETTINGS, "label": "設定"},
        ]
        
        rail_destinations = [
            ft.NavigationRailDestination(
                icon_content=ft.Icon(dest["icon"]), 
                selected_icon_content=ft.Icon(dest["selected_icon"]), 
                label=dest["label"]
            ) for dest in destinations
        ]
        
        return ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=80,
            group_alignment=-0.8,
            bgcolor="#ffffff",
            destinations=rail_destinations,
            leading=ft.Container(content=ft.IconButton(icon=ft.icons.MENU,icon_size=30, on_click=lambda e: print("")),padding=ft.margin.only(top=20)), # type: ignore
            on_change=self.handle_nav_change,
        )
    
    def init_views(self):
        return {
            0: HomePage(self.page),
            1: SearchPage(self.page),
            2: NotificationsPage(self.page),
            3: MessagesPage(self.page),
            4: ChatPage(self.page),
            5: ProfilePage(self.page),
            6: SettingsPage(self.page),
        }
    
    def create_view_container(self, index):
        return ft.Container(
            content=self.views[index],
            expand=True,
            bgcolor="#ffffff",
            border_radius=10,
        )
    
    def create_main_layout(self):
        return ft.Row(
            controls=[
                self.rail_container, 
                ft.VerticalDivider(width=1),
                self.content_view,
            ],
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.STRETCH,
        )
        
    def handle_nav_change(self, e):
        selected_index = e.control.selected_index
        self.content_view.content = self.views[selected_index]
        self.update()
