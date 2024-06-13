import flet as ft
import requests
from datetime import datetime
from dateutil import parser

class ProfilePage(ft.Container):
    def __init__(self, page, user_id):
        super().__init__()

        self.page = page
        self.user_id = user_id
        self.user = None
        self.padding = 20
        self.bgcolor = "#f2ede7"
        self.border_radius = 20
        self.expand = True

        print(f"ProfilePage initialized with user_id: {self.user_id}")

        # 初期状態では空のコンテンツを設定
        self.content = ft.Column(spacing=20, alignment=ft.MainAxisAlignment.START)
        
        # ユーザーデータをロード
        self.load_user_data()

    def load_user_data(self):
        try:
            response = requests.get(f"http://localhost:5000/user/{self.user_id}")
            if response.status_code == 200:
                self.user = response.json()
                self.display_user_profile()
            else:
                self.content.controls.append(ft.Text(f"エラー: ユーザー情報が見つかりません（ステータスコード: {response.status_code}）"))
        except Exception as e:
            self.content.controls.append(ft.Text(f"エラー: ユーザー情報を取得できませんでした: {e}"))

        self.page.update()

    def display_user_profile(self):
        if not self.user:
            return
        
        # プロフィールの表示要素を作成
        self.profile_image = self.create_profile_image()
        self.user_info = self.create_user_info()
        self.bio = self.create_bio()
        self.account_info = self.create_account_info()
        self.edit_button = self.create_edit_button()

        # コンテナに要素を追加
        self.content.controls.clear()
        self.content.controls.extend([
            self.profile_image,
            self.user_info,
            self.bio,
            self.account_info,
            self.edit_button
        ])

    def create_profile_image(self):
        return ft.Container(
            content=ft.Image(
                src=self.user.get('icon_url', '/path/to/default/icon.png'),  # デフォルトの画像パスを指定
                fit=ft.ImageFit.CONTAIN,
                width=100,
                height=100,
            ),
            border_radius=50,
            padding=10,
            bgcolor="#e0e0e0",
            alignment=ft.alignment.center
        )

    def create_user_info(self):
        return ft.Column(
            controls=[
                ft.Text(f"ユーザー名: {self.user['user_name']}", size=20, weight=ft.FontWeight.BOLD),
                ft.Text(f"ユーザーID: {self.user['user_id']}", size=16, weight=ft.FontWeight.NORMAL)
            ],
            alignment=ft.MainAxisAlignment.START,
        )

    def create_bio(self):
        return ft.Container(
            content=ft.Text(f"自己紹介: {self.user['bio']}", size=16, weight=ft.FontWeight.NORMAL),
            padding=ft.padding.all(10),
            border_radius=10,
            bgcolor="#ffffff"
        )

    def create_account_info(self):
        # `dateutil.parser` を使用して日付文字列をパース
        created_at = parser.parse(self.user['created_at'])
        return ft.Text(f"アカウント作成日: {created_at.strftime('%Y-%m-%d')}", size=14, weight=ft.FontWeight.NORMAL)

    def create_edit_button(self):
        return ft.ElevatedButton(
            text="編集",
            on_click=self.edit_profile,
            bgcolor="#1976d2",
            color="#ffffff",
        )

    def edit_profile(self, e):
        self.page.go(f"/profile/edit/{self.user['user_id']}")
