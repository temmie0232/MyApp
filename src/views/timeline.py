import time
import flet as ft
import requests
import datetime
import pytz 
from component.postcard import PostCard


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
        self.reload_button = ft.IconButton(icon=ft.icons.REFRESH,icon_color="#43474e", on_click=self.reload_posts)

        self.title = ft.Text("タイムライン", size=28, weight="w800")  
        self.main_lv = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)

        self.top_bar = ft.Row([self.title,self.reload_button],alignment=ft.MainAxisAlignment.CENTER)
        
    # UIの配置
    def create_main_layout(self):
        return ft.Column([
            ft.Container(self.top_bar, alignment=ft.alignment.center, height = 58),
            ft.Container(ft.Divider(), alignment=ft.alignment.center),
            ft.Container(content=ft.Row([
                ft.VerticalDivider(),
                self.main_lv,
                ft.VerticalDivider(),
                ],alignment=ft.MainAxisAlignment.CENTER), 
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
                post_container = PostCard(post)
                # ListViewにコンテナ(インスタンス)を追加
                self.main_lv.controls.append(post_container)
            self.page.update()  
        else:
            print("投稿を取得できませんでした")
            
    # 投稿をリロードするメソッド
    def reload_posts(self, e):
        self.main_lv.controls.clear()  # 現在の投稿をクリア
        self.load_posts()  # 再度投稿を読み込む

    def update_timeline(self):
        """タイムラインを更新するメソッド"""
        self.main_lv.controls.clear()  # 現在の投稿をクリア
        self.load_posts()  # 再度投稿を読み込む