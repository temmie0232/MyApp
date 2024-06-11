import flet as ft
import requests

class Login(ft.View):
    def __init__(self, page):
        super().__init__(
            route="/flet/login",
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        self.page = page
        self.page.title = "login"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.bgcolor = "#f0f4f9"
        
        self.initialize_ui()
        self.controls = [self.login_container]
    
    def initialize_ui(self):
        self.text_1 = ft.Text("MyAppにログイン", size=20, weight=ft.FontWeight.W_600, font_family="Segoe_UI_BOLD")
        self.input_username = self.create_input_field("メールアドレスの入力", "example@gmail.com")
        self.input_password = self.create_input_field("パスワードの入力", "password", True)
        self.login_btn = ft.ElevatedButton(text="ログイン", color="white", bgcolor="#00608d", on_click=self.handle_login, disabled=True)
        self.register_btn = ft.OutlinedButton(text="新規登録", on_click=self.handle_register)
        self.divider_row = self.create_divider()
        self.login_container = self.create_container()
        self.dlg_message = self.create_error_dialog()

    def create_input_field(self, label, hint_text, password=False):
        return ft.TextField(
            label=label,
            hint_text=hint_text,
            password=password,
            can_reveal_password=password,
            width=310,
            on_change=self.validate_login_form
        )

    def create_divider(self):
        return ft.Row(
            controls=[ft.Container(content=ft.Divider(), width=280, margin=-5)],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    
    def create_container(self):
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
            bgcolor="#ffffff",
            width=320,
            height=330,
            border_radius=10,
            padding=20,
            border=ft.border.all(1, "#f5f5f5"),
        )

    def create_error_dialog(self):
        return ft.AlertDialog(
            modal=True,
            title=ft.Text("エラー"),
            content=ft.Text(""),
            actions=[ft.TextButton("閉じる", on_click=self.close_error_dialog)],
            actions_alignment=ft.MainAxisAlignment.END
        )
    
    def validate_login_form(self, e):
        self.login_btn.disabled = not (self.input_username.value and self.input_password.value)
        self.page.update() # type: ignore

    def handle_login(self, e):
        email = self.input_username.value
        password = self.input_password.value
        
        response = requests.post("http://127.0.0.1:5000/login", json={"email": email, "password": password})

        if response.status_code == 200:     
            # ログイン成功時のユーザー情報   
            user_data = response.json()
            # サーバーからのレスポンスを確認
            print(f"Server response data: {user_data}")
            # ユーザーIDを取得
            user_id = user_data.get("user_id")
            
            # ユーザーIDをセッションに保存
            if user_id:
                self.page.session.set("user_id", user_id)
                print(f"Logged in user_id: {user_id}")  # デバッグ用
                self.page.go("/flet/home")  # type: ignore
            else:
                print("ユーザーIDが取得できませんでした。")
                self.dlg_message.content = ft.Text("ユーザーIDが取得できませんでした。")
                self.dlg_message.open = True
                self.page.dialog = self.dlg_message  # type: ignore
                self.page.update()  # type: ignore

        else:
            self.dlg_message.content = ft.Text("メールアドレスまたはパスワードが無効です")
            self.dlg_message.open = True
            self.page.dialog = self.dlg_message # type: ignore
            self.page.update() # type: ignore

    def handle_register(self, e):
        self.page.go("/flet/signup") # type: ignore
        
    def close_error_dialog(self, e):
        self.dlg_message.open = False
        self.page.update() # type: ignore

if __name__ == "__main__":
    ft.app(target=Login)
