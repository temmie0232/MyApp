import flet as ft
from views.home import HomePage
from views.search import SearchPage
from views.notifications import NotificationsPage
from views.messages import MessagesPage
from views.chat import ChatPage
from views.profile import ProfilePage
from views.settings import SettingsPage
from component.post import PostPage


class MainPage(ft.View):
    def __init__(self, page):
        super().__init__(
            route="/flet/home",
            vertical_alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )
        
        self.page = page
        self.bgcolor = "#aaa7a5"
        
        self.mascot = self.create_mascot()
        
        self.post_btn = self.create_post_btn()
        
        self.post_page = self.create_post_page()
        self.post_page_ = self.create_post_page_()
        
        self.rail = self.create_nav_rail()
        self.rail_container = ft.Container(content=self.rail, border_radius=20)
        
        
        
        self.views = self.init_views()
        self.content_view = ft.Container(
            content=self.views[0],
            expand=True,
            border_radius=10,
        )
        
        self.controls = [self.create_main_layout()]
    
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
                icon_content=ft.Container(
                    content=ft.Icon(dest["icon"], size=27),
                    padding=ft.padding.only(bottom=5,top=5)  # 下部にスペースを追加
                ),
                selected_icon_content=ft.Container(
                    content=ft.Icon(dest["selected_icon"], size=27),
                    padding=ft.padding.only(bottom=5,top=5)  # 下部にスペースを追加
                ),
                label=dest["label"],
            ) for dest in destinations
        ]
        
        
        return ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            group_alignment=-0.9,
            bgcolor="#f2ede7",
            destinations=rail_destinations,
            indicator_shape=ft.CircleBorder(),
            indicator_color="#d2d2d2",
            leading=self.mascot,
            trailing=self.post_btn,
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
            border_radius=20,
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

    def create_mascot(self):
        return ft.Container(
            content = ft.IconButton(
                content=ft.Image(
                    src=f"/images/1_64.png",
                    fit=ft.ImageFit.FILL,
                    width = 50,
                    height = 50,
                )
            ),
            padding=ft.margin.only(top=15) # type: ignore
        )
    
    def create_post_btn(self):
        return ft.Container(
            content = ft.IconButton(
                    icon = ft.icons.HISTORY_EDU,
                    width = 40,
                    height = 40,
                    on_click=self.show_post_page,
            )
        )

    def mascot_clicked(self,e):
        pass
        
    def handle_nav_change(self, e):
        selected_index = e.control.selected_index
        self.content_view.content = self.views[selected_index]
        self.update()

    def create_post_page(self):
        post_page = PostPage()
        return post_page

    def create_post_page_(self):
        return ft.AlertDialog(content=ft.Text("Hello"))

    # ダイアログを表示
    def show_post_page(self,e):
        self.page.dialog = self.post_page # type: ignore
        self.post_page.open = True
        self.page.update() # type: ignore
    
    # ダイアログを閉じる
    def close_dlg(self,e):
        self.post_page.open = False
        self.page.update()  # type: ignore
    
        
    
        

