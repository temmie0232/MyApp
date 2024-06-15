import time
import flet as ft
import requests
import datetime
import pytz  # タイムゾーンのサポート


class TimelinePage(ft.Container):
    def __init__(self, page):
        super().__init__()
        
        self.page = page
        self.padding = 20
        self.bgcolor = "#f2ede7"
        self.border_radius = 20
        self.expand = True
        
        # UIの初期化
        self.initialize_ui()
        
        # UIを画面に配置
        self.content = self.create_main_layout()

        # 過去の投稿を取得して表示
        self.load_posts()  # すべての初期化が完了した後に呼び出す

        # 初期化完了後に呼び出し
        self.page.update()

    # UIの初期化
    def initialize_ui(self):
        self.title = ft.Text("タイムライン", size=28, weight="w800")  # type: ignore
        self.main_lv = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)

    # UIの配置
    def create_main_layout(self):
        return ft.Column([
            ft.Container(self.title, alignment=ft.alignment.center),
            ft.Container(ft.Divider(), alignment=ft.alignment.center),
            ft.Container(content=ft.Row([
                ft.VerticalDivider(),
                self.main_lv,
                ft.VerticalDivider(),
                ],alignment=ft.MainAxisAlignment.CENTER), # type: ignore
                expand=True,
                height=500,  # スクロールエリアの高さを指定
                alignment=ft.alignment.center,
            ),
        ],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    
    def load_posts(self):
        # データベースから投稿を取得するエンドポイントへのリクエストを作成
        response = requests.get("http://localhost:5000/timeline")
        
        if response.status_code == 200:
            print("投稿を取得しました")
            posts = response.json()
            for post in posts:
                # インスタンスを作成
                post_container = PostContainer(post)
                # ListViewにコンテナ(インスタンス)を追加
                self.main_lv.controls.append(post_container)
            self.page.update()  # type: ignore
        else:
            print("投稿を取得できませんでした")
            

# 投稿のコンポーネント
class PostContainer(ft.Container):
    def __init__(self, post_data):
        super().__init__()
        
        self.padding = 10
        self.bgcolor = "#ffffff"
        self.border_radius = 10

        # 外側左右25,上下5
        self.margin = ft.margin.only(25, 5, 25, 5)
        # 内側
        self.padding = ft.padding.only(20, 20, 20, 10)        

        self.width = 500
        
        # post_dataを元にUIを作成
        self.create_ui(post_data)
        
    def create_ui(self, post_data):
        # post_dataを使い、各投稿の内容を表示するUIを構築
        user_name = post_data.get("user_name")
        any_user_id = post_data.get("any_user_id")  # user_id を any_user_id に変更
        content = post_data.get("content")
        created_at_str = post_data.get("created_at")
        
        # created_atをdatetimeオブジェクトに変換
        created_at = self.parse_datetime(created_at_str)
            
        # 現在の日時をUTCで取得
        now = datetime.datetime.now(datetime.timezone.utc)
        
        # 時間差表記の変更
        time_display = self.format_time_diff(created_at, now)

        # ユーザー情報部分
        user_info = ft.Row([ft.Text(f"{user_name}", weight="bold"), ft.Text(f"{any_user_id} ", color="#888888"), ft.Text(time_display)])  # type: ignore

        # 下部のアイコン部分
        action_bar = ft.Container(
            content=ft.Row([
                ft.IconButton(icon=ft.icons.REPLY_OUTLINED, tooltip="返信", icon_size=18, icon_color=ft.colors.BLACK),
                ft.IconButton(icon=ft.icons.SYNC, tooltip="リポスト", selected_icon=ft.icons.SYNC, icon_size=18, icon_color=ft.colors.BLACK, selected_icon_color="#00ba7c", selected=False, on_click=self.toggle_icon_button),
                ft.IconButton(icon=ft.icons.FAVORITE_BORDER, selected_icon=ft.icons.FAVORITE, tooltip="いいね", icon_size=18, icon_color=ft.colors.BLACK, selected_icon_color="#f91880", selected=False, on_click=self.toggle_icon_button),
            ],
                height=29),
        )
        
        # スペース用コンテナ
        divider = ft.Container(height=10)
        
        self.content = ft.Column([
            ft.Container(content=user_info),  # type: ignore
            divider,
            ft.Text(f"{content}", max_lines=5),
            divider,
            ft.Divider(thickness=0.6, height=4),
            action_bar,
        ],
            spacing=5,
        )
        
    def parse_datetime(self, date_str):
        for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%S.%f", "%a, %d %b %Y %H:%M:%S %Z"):
            try:
                return datetime.datetime.strptime(date_str, fmt).replace(tzinfo=datetime.timezone.utc)
            except ValueError:
                continue
        raise ValueError(f"time data '{date_str}' does not match any known format")
    
    def format_time_diff(self, past_time, current_time):
        time_diff = current_time - past_time

        if time_diff.days >= 7:
            return past_time.strftime("%Y/%m/%d")
        elif time_diff.days > 0:
            return f"{time_diff.days}日前"
        elif time_diff.seconds >= 3600:
            hours = time_diff.seconds // 3600
            return f"{hours}時間前" if hours > 1 else "1時間前"
        elif time_diff.seconds >= 60:
            minutes = time_diff.seconds // 60
            return f"{minutes}分前" if minutes > 1 else "1分前"
        else:
            return "たった今"
        
    def toggle_icon_button(self, e):
        e.control.selected = not e.control.selected
        e.control.update()
