import flet as ft
import requests


class TimelinePage(ft.Container):
    def __init__(self, page):
        super().__init__()
        
        self.page = page
        self.padding = 20
        self.bgcolor = "#f2ede7"
        self.border_radius = 20
        self.expand = True
        self.page.scroll = "auto"
        
        # UIの初期化
        self.initialize_ui()
        
        # UIを画面に配置
        self.content = self.create_main_layout()

        # 過去の投稿を取得して表示
        self.load_posts()        # すべての初期化が完了した後に呼び出す

        # 初期化完了後に呼び出し
        self.page.update()

    # UIの初期化
    def initialize_ui(self):
        self.title = ft.Text("タイムライン", size = 28, weight = "w800") # type: ignore
        self.main_lv= ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

    # UIの配置
    def create_main_layout(self):
        return ft.Column([
            self.title,
            ft.Divider(),
            self.main_lv
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
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
            self.page.update() # type: ignore
        else:
            print("投稿を取得できませんでした")
            
# 投稿のコンポーネント
class PostContainer(ft.Container):
    def __init__(self,post_data):
        super().__init__()
        
        self.padding = 10
        self.bgcolor = "#ffffff"
        self.border_radius = 10
        self.margin = ft.Margin(10,0,10,0)
        
        # post_dataを元にUIを作成
        self.create_ui(post_data)
        
    def create_ui(self, post_data):
        # post_dataを使い、各投稿の内容を表示するUIを構築
        user_name = post_data.get("user_name")
        user_id = post_data.get("user_id")
        content = post_data.get("content")
        created_at = post_data.get("created_at")

        user_info = ft.Row([ft.Text(f"{user_name}",weight="bold"),ft.Text(user_id,color="#888888")]) # type: ignore

        self.content = ft.Column([
                ft.Container(content=user_info), # type: ignore
                ft.Text(f"{content}"),
                ft.Text(f"{created_at}",size=10,color="#888888")
            ],
            spacing=5,
        )