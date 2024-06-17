import flet as ft
import requests

class Login(ft.View):
    def __init__(self, page):
        super().__init__(
            route="/login",
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        self.page = page
        self.page.title = "login"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.bgcolor = "#aba7a5"

        # UI要素の初期化
        self.init_ui()

        # メインコンテナの設定
        self.controls = [self.create_main_container()]

        # ページロード時にダイアログを表示
        self.show_greeting_dialog()

    def init_ui(self):
        """UI要素の初期化"""
        self.text_1 = ft.Text("MyAppにログイン", size=20, weight=ft.FontWeight.W_600, font_family="Segoe_UI_BOLD")
        self.input_username = self.create_input_field("メールアドレスの入力", "example@gmail.com")
        self.input_password = self.create_input_field("パスワードの入力", "password", True)
        self.login_btn = ft.ElevatedButton(text="ログイン", color="white", bgcolor="#00608d", on_click=self.handle_login, disabled=True)
        self.register_btn = ft.OutlinedButton(text="新規登録", on_click=self.handle_register)
        self.divider_row = self.create_divider()
        self.dlg_message = self.create_error_dialog()

    def create_input_field(self, label, hint_text, password=False):
        """入力フィールドの作成"""
        return ft.TextField(
            label=label,
            hint_text=hint_text,
            password=password,
            can_reveal_password=password,
            width=310,
            focused_border_width=2,
            border_radius=5,
            on_change=self.validate_login_form,
        )

    def create_divider(self):
        """区切り線の作成"""
        return ft.Row(
            controls=[ft.Container(content=ft.Divider(), width=280, margin=-5)],
            alignment=ft.MainAxisAlignment.CENTER,
        )

    def create_main_container(self):
        """メインコンテナの作成"""
        return ft.Container(
            content=ft.Column([
                self.text_1,
                ft.Container(height=1),
                self.input_username,
                self.input_password,
                self.login_btn,
                self.divider_row,
                self.register_btn,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            bgcolor="#f2ede7",
            width=320,
            height=320,
            border_radius=10,
            padding=20,
            border=ft.border.all(1, "#f5f5f5"),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=5,
                color=ft.colors.GREY_500,
                offset=ft.Offset(0, 0),
                blur_style=ft.ShadowBlurStyle.OUTER,
            )
        )

    def create_error_dialog(self):
        """エラーダイアログの作成"""
        return ft.AlertDialog(
            modal=True,
            title=ft.Text("エラー"),
            content=ft.Text(""),
            actions=[ft.TextButton("閉じる", on_click=self.close_error_dialog)],
            actions_alignment=ft.MainAxisAlignment.END
        )

    def validate_login_form(self, e):
        """ログインフォームのバリデーション"""
        self.login_btn.disabled = not (self.input_username.value and self.input_password.value)
        self.page.update()

    def handle_login(self, e):
        """ログイン処理"""
        email = self.input_username.value
        password = self.input_password.value

        try:
            response = requests.post("http://127.0.0.1:5000/login", json={"email": email, "password": password})

            if response.status_code == 200:
                user_data = response.json()
                print(f"Server response data: {user_data}")

                any_user_id = user_data.get("any_user_id")
                if any_user_id:
                    self.page.session.set("any_user_id", any_user_id)  # セッションにユーザーIDを保存 #type: ignore
                    print(f"Logged in any_user_id: {any_user_id}")
                    self.page.go("/home")
                else:
                    self.show_error("ユーザーIDが取得できませんでした。")

            else:
                self.show_error("メールアドレスまたはパスワードが無効です")
        except requests.RequestException as ex:
            self.show_error(f"サーバーとの通信に失敗しました: {ex}")

    def handle_register(self, e):
        """新規登録ページに遷移"""
        self.page.go("/signup")

    def show_error(self, message):
        """エラーメッセージの表示"""
        self.dlg_message.content = ft.Text(message)
        self.dlg_message.open = True
        self.page.dialog = self.dlg_message
        self.page.update()

    def close_error_dialog(self, e):
        """エラーダイアログを閉じる"""
        self.dlg_message.open = False
        self.page.update()

    def show_greeting_dialog(self):
        """挨拶ダイアログの表示"""
        greeting_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("⚠注意"),
            content=ft.Column([ft.Text("登録が面倒な方のために、以下のメールアドレスと\nパスワードで簡単にログインできるように設定しています\n\nメールアドレス: root\nパスワード: root\n\n登録がPC以外からアクセスするとレイアウトが崩れる可能性あり\n制作途中のため、完成していなページ・バグが存在しています\n"),
                               ft.Container(content=ft.Text(" 大切な情報は入力しないでください！",color=ft.colors.WHITE),bgcolor=ft.colors.RED),
                            ft.TextButton(text="リポジトリを開く"),
                            ft.TextButton(text="Fletのドキュメントを開く\n"),
                            ft.Text("私は、Webアプリ開発(flet)やプログラム全般においてまだ十分慣れていないため、\nコードに誤りや不整合がある場合があります。\nまた、GitHubの使用にも不慣れなため、リポジトリの管理や運用に\n不備があるかもしれません。")]),
            actions=[ft.TextButton("ok", on_click=self.close_greeting_dialog)],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog = greeting_dialog
        greeting_dialog.open = True
        self.page.update()

    def close_greeting_dialog(self, e):
        """挨拶ダイアログを閉じる"""
        self.page.dialog.open = False
        self.page.update()

if __name__ == "__main__":
    ft.app(target=Login)
