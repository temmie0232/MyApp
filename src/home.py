import flet as ft
from views.timeline import TimelinePage
from views.search import SearchPage
from views.notifications import NotificationsPage
from views.messages import MessagesPage
from views.chat import ChatPage
from views.profile import ProfilePage
from views.settings import SettingsPage
from component.postdialog import PostPage

class MainPage(ft.View):
    def __init__(self, page):
        super().__init__(
            route="/home",
            vertical_alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )

        self.page = page
        self.bgcolor = "#aaa7a5"
        
        self.init_ui_elements()  # UI要素の初期化
        self.controls = [self.create_main_layout()]  # メインレイアウトの設定
    
    def init_ui_elements(self):
        """UI要素の初期化"""
        self.mascot = self.create_mascot()
        self.post_btn = self.create_post_button()
        
        self.rail = self.create_navigation_rail()
        self.rail_container = ft.Container(content=self.rail, border_radius=20)
        
        self.views = self.init_views()
        self.content_view = self.create_view_container(initial_index=0)
        
        self.post_page = PostPage(self.page)  # ダイアログインスタンスを作成
    
    def create_navigation_rail(self):
        """ナビゲーションレールの作成"""
        destinations = self.get_navigation_destinations()

        rail_destinations = [
            ft.NavigationRailDestination(
                icon_content=self.create_icon_container(dest["icon"]),
                selected_icon_content=self.create_icon_container(dest["selected_icon"]),
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
            on_change=self.handle_navigation_change,
        )

    def get_navigation_destinations(self):
        """ナビゲーションレールの宛先設定"""
        return [
            {"icon": ft.icons.HOME_OUTLINED, "selected_icon": ft.icons.HOME, "label": "ホーム"},
            {"icon": ft.icons.SEARCH_OUTLINED, "selected_icon": ft.icons.SEARCH, "label": "検索"},
            {"icon": ft.icons.NOTIFICATIONS_OUTLINED, "selected_icon": ft.icons.NOTIFICATIONS, "label": "通知"},
            {"icon": ft.icons.MAIL_OUTLINED, "selected_icon": ft.icons.MAIL, "label": "メッセージ"},
            {"icon": ft.icons.SPEAKER_NOTES_OUTLINED, "selected_icon": ft.icons.SPEAKER_NOTES, "label": "AIチャット"},
            {"icon": ft.icons.PERSON_OUTLINED, "selected_icon": ft.icons.PERSON, "label": "プロフィール"},
            {"icon": ft.icons.SETTINGS_OUTLINED, "selected_icon": ft.icons.SETTINGS, "label": "設定"},
        ]

    def create_icon_container(self, icon_name):
        """アイコンを含むコンテナの作成"""
        return ft.Container(
            content=ft.Icon(icon_name, size=27),
            padding=ft.padding.only(bottom=5, top=5)
        )

    def init_views(self):
        """各ページのビューを初期化"""
        any_user_id = self.page.session.get("any_user_id")  

        if any_user_id is None:
            self.page.go("/login")
            return {}

        return {
            0: TimelinePage(self.page),
            1: SearchPage(self.page),
            2: NotificationsPage(self.page),
            3: MessagesPage(self.page),
            4: ChatPage(self.page),
            5: ProfilePage(self.page, any_user_id=any_user_id),
            6: SettingsPage(self.page),
        }

    def display_user_profile(self, any_user_id):
        """ユーザープロファイルを表示"""
        profile_page = ProfilePage(self.page, any_user_id=any_user_id)
        self.content_view.content = profile_page
        self.update()
        
    def create_view_container(self, initial_index):
        """ビューを含むコンテナを作成"""
        return ft.Container(
            content=self.views[initial_index],
            expand=True,
            border_radius=20,
        )

    def create_main_layout(self):
        """メインレイアウトの作成"""
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
        """マスコットアイコンの作成"""
        return ft.Container(
            content=ft.IconButton(
                content=ft.Image(
                    src=f"/images/1_64.png",
                    fit=ft.ImageFit.FILL,
                    width=50,
                    height=50,
                ),
                url="https://github.com/temmie0232/MyApp",
                tooltip="リポジトリを開く"
            ),
            padding=ft.margin.only(top=15) 
        )

    def create_post_button(self):
        """投稿ボタンの作成"""
        return ft.Container(
            content=ft.Column([
                ft.Container(height=5),
                ft.Container(ft.IconButton(
                    icon=ft.icons.RATE_REVIEW_OUTLINED,
                    width=40,
                    height=40,
                    on_click=self.show_post_page,
                    icon_color="#000000",
                    icon_size=25,
                    tooltip="投稿する"),
                    bgcolor="#f2ede7",
                    border=ft.border.all(2, ft.colors.BLACK),
                    border_radius=ft.border_radius.all(10)),
            ])
        )

    def handle_navigation_change(self, e):
        """ナビゲーション変更時のハンドリング"""
        selected_index = e.control.selected_index
        self.content_view.content = self.views[selected_index]
        self.update()

    def show_post_page(self, e):
        """ダイアログを表示"""
        self.page.dialog = self.post_page
        self.post_page.open = True
        self.page.update() 

    def close_dialog(self, e):
        """ダイアログを閉じる"""
        self.post_page.open = False
        self.page.update() 
