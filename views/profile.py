import time
import flet as ft
import requests
from datetime import datetime
from dateutil import parser

class ProfilePage(ft.Container):
    def __init__(self, page, any_user_id):  # user_id を any_user_id に変更
        super().__init__()

        self.page = page
        self.any_user_id = any_user_id  # user_id を any_user_id に変更
        self.user = None
        self.padding = 20
        self.bgcolor = "#f2ede7"
        self.border_radius = 20
        self.expand = True

        print(f"ProfilePage initialized with any_user_id: {self.any_user_id}")  # 出力メッセージも修正

        # 初期状態では空のコンテンツを設定
        self.content = ft.Column(spacing=20, alignment=ft.MainAxisAlignment.START)
        
        # ユーザーデータをロード
        self.load_user_data()

    def load_user_data(self):
        try:
            response = requests.get(f"http://localhost:5000/user/{self.any_user_id}")  # API URLも修正
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
                src=self.user.get('icon_path', 'uploads/icons/default/icon.png'),  # デフォルトの画像パスを指定
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
                # ユーザ名
                ft.Text(f"{self.user['user_name']}", size=24, weight=ft.FontWeight.BOLD),
                # ユーザID
                ft.Text(f"{self.user['any_user_id']}", size=14, color="#888888", weight=ft.FontWeight.NORMAL)  
            ],
            alignment=ft.MainAxisAlignment.START,
        )

    def create_bio(self):
        return ft.Container(
            # 自己紹介
            content=ft.Text(f"自己紹介: {self.user['bio']}", size=16, weight=ft.FontWeight.NORMAL),
            padding=ft.padding.all(10),
            border_radius=10,
            bgcolor="#ffffff"
        )

    def create_account_info(self):
        created_at = parser.parse(self.user['created_at'])
        # アカウント作成日
        return ft.Text(f"アカウント作成日: {created_at.strftime('%Y-%m-%d')}", size=14, color="#888888", weight=ft.FontWeight.NORMAL)

    def create_edit_button(self):
        return ft.ElevatedButton(
            text="編集",
            on_click=self.show_edit_dialog,
            bgcolor="#1976d2",
            color="#ffffff",
        )

    def show_edit_dialog(self, e):
        self.icon_input = ft.FilePicker(on_result=self.icon_selected)
        self.page.overlay.append(self.icon_input)
        
        self.edit_user_name = ft.TextField(label="ユーザー名", bgcolor=ft.colors.WHITE, value=self.user['user_name'])
        self.edit_bio = ft.TextField(label="自己紹介", multiline=True, bgcolor=ft.colors.WHITE, value=self.user['bio'])
        
        self.edit_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("プロフィールを編集"),
            content=ft.Column(
                [
                    ft.Text("アイコン画像をアップロード"),
                    ft.ElevatedButton(text="ファイルを選択", on_click=lambda _: self.icon_input.pick_files(allow_multiple=False)),
                    self.edit_user_name,
                    self.edit_bio,
                ],
                spacing=20,
                height=400,
                width=300,
            ),
            actions=[
                ft.TextButton("キャンセル", on_click=self.close_dialog),
                ft.ElevatedButton("保存", on_click=self.save_profile)
            ],
            bgcolor="#f2ede7",
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = self.edit_dialog
        self.edit_dialog.open = True
        self.page.update()

    def icon_selected(self, e: ft.FilePickerResultEvent):
        if e.files:
            self.selected_icon_file = e.files[0]
            print(f"Selected file: {self.selected_icon_file.name}")

    def close_dialog(self, e):
        self.edit_dialog.open = False
        self.page.update()

    def save_profile(self, e):
        # 新しいデータを収集
        new_user_name = self.edit_user_name.value
        new_bio = self.edit_bio.value
        
        data = {
            "user_name": new_user_name,
            "bio": new_bio,
        }
        # サーバーにデータを送信して更新
        response = requests.post(f"http://localhost:5000/update_user/{self.any_user_id}", json=data)
        
        if response.status_code == 200:
            print(f"・{new_user_name}\n・{new_bio}\nに更新しました")
            self.user['user_name'] = new_user_name
            self.user['bio'] = new_bio
            self.display_user_profile()
            self.close_dialog(e)
        else:
            print(f"Error updating profile: {response.text}")
