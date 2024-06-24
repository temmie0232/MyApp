import flet as ft
import requests
from dateutil import parser
from component.postcard import PostCard
from component.ui_utils import update_banner

class ProfilePage(ft.Container):
    def __init__(self, page, any_user_id, logged_in_user_id):
        super().__init__()

        self.page = page
        self.any_user_id = any_user_id
        self.logged_in_user_id = logged_in_user_id
        self.user = None
        self.selected_icon_file = None
        self.padding = 20
        self.bgcolor = "#f2ede7"
        self.border_radius = 20
        self.expand = True

        print(f"ProfilePage が any_user_id <{self.any_user_id}> で初期化されました")

        self.initialize_ui()
        self.setup_file_picker()
        self.load_user_data()
        self.load_posts()

    def initialize_ui(self):
        """UIコンポーネントの初期化"""
        self.profile_image = ft.Container()
        self.user_id = ft.Column()
        self.bio = ft.Container()
        self.account_info = ft.Text()
        self.edit_button = ft.ElevatedButton()

        self.reload_button = ft.IconButton(icon=ft.icons.REFRESH, icon_color="#42474e", on_click=self.reload_posts)

        self.title = ft.Container(
            content=ft.Text("過去の投稿", size=28, weight="w800"),
            alignment=ft.alignment.center
        )

        self.top_bar = ft.Row([self.title, self.reload_button], alignment=ft.MainAxisAlignment.CENTER)

        self.main_lv = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)

        self.timeline = ft.Column(
            [
                self.top_bar,
                ft.Container(content=ft.Divider(), alignment=ft.alignment.center),
                ft.Container(
                    content=self.main_lv,
                    expand=True,
                    height=500,
                    alignment=ft.alignment.center,
                ),
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def create_main_layout(self):
        """メインレイアウトを作成する"""
        return ft.Row(
            [
                ft.Container(self.profile_component, alignment=ft.alignment.center, expand=True),
                ft.VerticalDivider(),
                ft.Container(self.timeline, alignment=ft.alignment.center, expand=True),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )

    def create_profile_component(self):
        """プロフィールコンポーネントを作成する"""
        profile_image = self.create_profile_image()
        user_info = self.create_user_info()
        bio = self.create_bio()
        account_info = self.create_account_info()

        # 編集ボタンまたはメッセージ送信ボタンの表示
        if self.any_user_id == self.logged_in_user_id:
            action_button = self.create_edit_button()
        else:
            action_button = self.create_message_button()

        return ft.Container(
            content=ft.Column(
                controls=[
                    profile_image,
                    user_info,
                    bio,
                    account_info,
                    ft.Divider(),
                    action_button
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
            border_radius=20,
            bgcolor="#ffffff",
            width=400,
            height=375,
            alignment=ft.alignment.center,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=5,
                color=ft.colors.GREY_500,
                offset=ft.Offset(0, 0),
                blur_style=ft.ShadowBlurStyle.OUTER,
            )
        )

    def setup_file_picker(self):
        """ファイルピッカーの設定"""
        self.icon_input = ft.FilePicker(on_result=self.icon_selected)
        self.page.overlay.append(self.icon_input)

    def load_user_data(self):
        """ユーザーデータをサーバーから取得して表示"""
        try:
            response = requests.get(f"http://localhost:5000/user/{self.any_user_id}")
            if response.status_code == 200:
                self.user = response.json()
                self.profile_component = self.create_profile_component()
                self.content = self.create_main_layout()
            else:
                self.show_error_message(f"エラー: ユーザー情報が見つかりません（ステータスコード: {response.status_code}）")
        except Exception as e:
            self.show_error_message(f"エラー: ユーザー情報を取得できませんでした: {e}")

    def load_posts(self):
        """ユーザーの投稿をロード"""
        try:
            response = requests.get(f"http://localhost:5000/user/{self.any_user_id}/posts")
            if response.status_code == 200:
                print("投稿を取得しました")
                posts = response.json()
                for post in posts:
                    post_container = PostCard(post)
                    self.main_lv.controls.append(post_container)
                self.page.update()
            else:
                self.show_error_message("投稿を取得できませんでした")
        except Exception as e:
            self.show_error_message(f"エラー: 投稿を取得できませんでした: {e}")

    def display_user_profile(self):
        """ユーザープロフィールの表示または更新"""
        print("ユーザープロフィールを表示します")

        self.profile_component = self.create_profile_component()
        self.content = self.create_main_layout()
        self.page.update()

    def show_error_message(self, message):
        """エラーメッセージを表示"""
        print(message)

    def create_profile_image(self):
        """プロフィール画像コンポーネントを作成する"""
        return ft.Container(
            content=ft.Icon(name=ft.icons.ACCOUNT_CIRCLE, size=100, color="#42474e"),
            alignment=ft.alignment.center
        )

    def create_user_info(self):
        """ユーザー情報の表示コンテナを作成"""
        return ft.Column(
            controls=[
                ft.Text(f"{self.user['user_name']}", size=32, weight=ft.FontWeight.BOLD),
                ft.Text(f"@{self.user['any_user_id']}", size=14, color="#888888", weight=ft.FontWeight.NORMAL)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def create_bio(self):
        """自己紹介のコンテナを作成"""
        return ft.Container(
            content=ft.Text(f"{self.user['bio']}", size=16, weight=ft.FontWeight.NORMAL),
            padding=ft.padding.all(10),
            border_radius=10,
            bgcolor="#F3F2F4",
            alignment=ft.alignment.center,
        )

    def create_account_info(self):
        """アカウント作成日情報の表示コンテナを作成"""
        created_at = parser.parse(self.user['created_at'])
        return ft.Text(f"アカウント作成日: {created_at.strftime('%Y-%m-%d')}", size=12, color="#888888", weight=ft.FontWeight.NORMAL)

    def create_edit_button(self):
        """編集ボタンを作成"""
        return ft.OutlinedButton(
            text="編集",
            on_click=self.show_edit_dialog,
            style=ft.ButtonStyle(color=ft.colors.BLACK, overlay_color="#e2e2e2")
        )

    def create_message_button(self):
        """メッセージ送信ボタンを作成"""
        return ft.OutlinedButton(
            text="メッセージを送信",
            on_click=self.send_message,
            style=ft.ButtonStyle(color=ft.colors.BLACK, overlay_color="#e2e2e2")
        )

    def show_edit_dialog(self, e):
        """編集ダイアログを表示"""
        self.icon_input = ft.FilePicker(on_result=self.icon_selected)
        self.page.overlay.append(self.icon_input)

        self.edit_user_name = ft.TextField(label="ユーザー名", bgcolor=ft.colors.WHITE, value=self.user['user_name'])
        self.edit_bio = ft.TextField(label="自己紹介", multiline=True, bgcolor=ft.colors.WHITE, value=self.user['bio'])

        self.upload_status_container = ft.Row(controls=[])

        self.edit_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Column([ft.Text("プロフィールを編集")], horizontal_alignment=ft.CrossAxisAlignment.CENTER,),
            content=ft.Column(
                [
                    ft.Divider(),
                    ft.Text("アイコン画像をアップロード\n(この機能はまだ実装してないです)"),
                    ft.ElevatedButton(text="ファイルを選択", on_click=lambda _: self.icon_input.pick_files(allow_multiple=False, file_type=ft.FilePickerFileType.IMAGE)),
                    self.upload_status_container,
                    ft.Divider(),
                    self.edit_user_name,
                    self.edit_bio,
                ],
                height=400,
                width=300,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
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
        """アイコンが選択されたときの処理"""
        if e.files:
            selected_file = e.files[0]
            print(f"選択されたファイル: {selected_file.name}")

            # ファイルのアップロード
            path = f"http://localhost:5000/upload_icon/{self.any_user_id}"
            files = {'file': (selected_file.name, selected_file.size)}

            response = requests.post(path, files=files)

            if response.status_code == 200:
                save_path = response.json().get('save_path')
                print(f"ファイルが保存されました: {save_path}")

                self.user['icon_path'] = save_path

                self.upload_status_container.controls.clear()
                self.upload_status_container.controls.append(
                    ft.Row(
                        [
                            ft.Icon(name=ft.icons.CHECK_CIRCLE_OUTLINE, color=ft.colors.GREEN),
                            ft.Text(selected_file.name, size=12, color="#888888", weight=ft.FontWeight.NORMAL),
                        ],
                        spacing=10,
                    )
                )
                self.page.update()

            else:
                print(f"ファイルのアップロード中にエラーが発生しました: {response.text}")

    def close_dialog(self, e):
        """ダイアログを閉じる"""
        self.edit_dialog.open = False
        self.page.update()

    def save_profile(self, e):
        """プロフィールの変更を保存"""
        new_user_name = self.edit_user_name.value
        new_bio = self.edit_bio.value

        data = {
            "user_name": new_user_name,
            "bio": new_bio,
            "icon_path": self.user.get('icon_path')
        }

        response = requests.post(f"http://localhost:5000/update_user/{self.any_user_id}", json=data)

        if response.status_code == 200:
            print(f"・{new_user_name}\n・{new_bio}\n・{self.user['icon_path']}\nに更新しました")
            self.user['user_name'] = new_user_name
            self.user['bio'] = new_bio

            update_banner(self.page, message="プロフィールが正常に更新されました！", action_text="了解")

            self.display_user_profile()
            self.close_dialog(e)
        else:
            print(f"ファイルの更新中にエラーが発生しました: {response.text}")

    def reload_posts(self, e):
        """投稿をリロードするメソッド"""
        self.main_lv.controls.clear()  # 現在の投稿をクリア
        self.load_posts()  # 再度投稿を読み込む

    def send_message(self, e):
        """メッセージ送信処理（仮）"""
        print("メッセージを送信する処理")

    def update_timeline(self):
        """プロフィールページの投稿リストを更新するメソッド"""
        self.main_lv.controls.clear()  # 現在の投稿をクリア
        self.load_posts()  # 再度投稿を読み込む