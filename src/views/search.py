import flet as ft
import requests
from component.postcard import PostCard
from component.usercard import UserCard
from component.ui_utils import update_banner 

class SearchPage(ft.Container):
    def __init__(self, page):
        super().__init__()
        
        self.page = page
        self.padding = 20
        self.bgcolor = "#f2ede7"
        self.border_radius = 20
        self.expand = True
        
        # 検索ターゲットのフラグを初期化
        self.search_target_post = True  # デフォルトで投稿がTrue
        self.search_target_user = False

        # UIの初期化
        self.initialize_ui()
        
        # UIを画面に配置
        self.content = self.create_main_layout()

        # 初期のデータをロード
        self.all_posts = []
        self.all_users = []
        self.load_initial_data()

        # 初期化完了後に更新
        self.page.update()

    def initialize_ui(self):
        """UIの要素を初期化"""
        self.reload_button = self.create_reload_button()
        self.search_field = self.create_search_field()
        self.popup_menu = self.create_popup_menu()
        self.top_bar = self.create_top_bar()
        self.main_lv = self.create_main_lv()

        # 初期ラベルの設定
        self.update_search_label()

    def create_reload_button(self):
        """リロードボタンを作成"""
        return ft.IconButton(
            icon=ft.icons.REFRESH,
            icon_color="#43474e",
            on_click=self.reload_posts
        )

    def create_search_field(self):
        """検索バーを作成"""
        return ft.TextField(
            label="XXを検索",
            hint_text="検索...",
            border_color=ft.colors.BLACK,
            cursor_color=ft.colors.BLACK,
            cursor_width=2,
            border_width=1,
            focused_border_width=2,
            border_radius=5,
            color=ft.colors.BLACK,
            width=400,
            on_change=self.on_search_change  # 変更イベントを監視
        )

    def create_popup_menu(self):
        """ポップアップメニューを作成"""
        return ft.PopupMenuButton(
            items=[
                ft.PopupMenuItem(text="検索対象 : 投稿", checked=self.search_target_post, on_click=self.check_post_item_clicked),
                ft.PopupMenuItem(text="検索対象 : ユーザー", checked=self.search_target_user, on_click=self.check_user_item_clicked),
            ],
            icon_color=ft.colors.BLACK45,
            icon=ft.icons.SETTINGS_APPLICATIONS,
            icon_size=25,
            bgcolor=ft.colors.WHITE,
            surface_tint_color=ft.colors.WHITE
        )

    def create_top_bar(self):
        """トップバーを作成"""
        return ft.Row(
            [
                ft.Container(
                    ft.Row(
                        [
                            self.popup_menu,
                            self.search_field,
                            self.reload_button,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    expand=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.START
        )

    def create_main_lv(self):
        """メインリストビューを作成"""
        return ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)

    def create_main_layout(self):
        """メインレイアウトの作成"""
        return ft.Column([
            ft.Container(self.top_bar, alignment=ft.alignment.center),
            ft.Container(ft.Divider(), alignment=ft.alignment.center),
            ft.Container(content=ft.Row([
                ft.VerticalDivider(),
                self.main_lv,
                ft.VerticalDivider(),
            ], alignment=ft.MainAxisAlignment.CENTER), 
            expand=True,
            height=500,
            alignment=ft.alignment.center),
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def load_initial_data(self):
        """初期データをロードする"""
        # 投稿データをロード
        self.load_posts()
        # ユーザーデータをロード
        self.load_users()

    def load_posts(self):
        """投稿データをロードする"""
        response = requests.get("http://localhost:5000/timeline")
        
        if response.status_code == 200:
            print("投稿を取得しました")
            self.all_posts = response.json()
            self.display_filtered_data()
        else:
            print("投稿を取得できませんでした")

    def load_users(self):
        """ユーザーデータをロードする"""
        response = requests.get("http://localhost:5000/users")
        
        if response.status_code == 200:
            print("ユーザーを取得しました")
            self.all_users = response.json()
            self.display_filtered_data()
        else:
            print("ユーザーを取得できませんでした")

    def reload_posts(self, e):
        """投稿をリロードする"""
        self.load_posts()

    def check_post_item_clicked(self, e):
        """投稿検索クリックハンドリング"""
        self.search_target_post = not self.search_target_post
        if self.search_target_post:
            self.search_target_user = False  # 投稿が選択されたらユーザーチェックをはずす
        self.update_popup_menu()

        # バナーを表示
        update_banner(self.page, message="検索対象が '投稿' に設定されました", action_text="OK")

        # ラベルを更新
        self.update_search_label()

        # 検索対象が変更されたらすぐにフィルタリング
        self.display_filtered_data()

    def check_user_item_clicked(self, e):
        """ユーザー検索クリックハンドリング"""
        self.search_target_user = not self.search_target_user
        if self.search_target_user:
            self.search_target_post = False  # ユーザーが選択されたら投稿チェックをはずす
        self.update_popup_menu()

        # バナーを表示
        update_banner(self.page, message="検索対象が 'ユーザー' に設定されました", action_text="OK")

        # ラベルを更新
        self.update_search_label()

        # 検索対象が変更されたらすぐにフィルタリング
        self.display_filtered_data()

    def update_popup_menu(self):
        """ポップアップメニューの状態を更新"""
        for item in self.popup_menu.items: # type: ignore
            if item.text == "検索対象 : 投稿":
                item.checked = self.search_target_post
            elif item.text == "検索対象 : ユーザー":
                item.checked = self.search_target_user
        self.page.update()

    def update_search_label(self):
        """検索バーのラベルを更新"""
        if self.search_target_post:
            self.search_field.label = "投稿を検索"
        elif self.search_target_user:
            self.search_field.label = "ユーザーを検索"
        else:
            self.search_field.label = "左のアイコンから検索条件を指定"
        self.page.update()

    def on_search_change(self, e):
        """検索バーの変更イベントをハンドル"""
        self.display_filtered_data()

    def display_filtered_data(self):
        """検索フィールドの内容に基づいてフィルタリングされたデータを表示"""
        keyword = self.search_field.value.lower()
        self.main_lv.controls.clear()

        if self.search_target_post:
            filtered_posts = [post for post in self.all_posts if keyword in post['content'].lower()]
            for post in filtered_posts:
                post_container = PostCard(post)
                self.main_lv.controls.append(post_container)

        elif self.search_target_user:
            filtered_users = [user for user in self.all_users if keyword in user['any_user_id'].lower()]
            for user in filtered_users:
                user_container = UserCard(user, on_click=self.show_user_profile)
                self.main_lv.controls.append(user_container)

        self.page.update()

    def show_user_profile(self, any_user_id):
        """ユーザープロファイルを表示"""
        main_page = self.page.views[0]  # MainPageのインスタンスを取得
        main_page.display_user_profile(any_user_id)