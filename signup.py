import datetime
import flet as ft
import requests

class SignupStep1(ft.View):
    def __init__(self, page):
        super().__init__(
            route="/signup",
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.page = page
        self.page.title = "step1"
        self.bgcolor = "#aba7a5"

        # UI要素の初期化
        self.init_ui()

        # メインコンテナの設定
        self.controls = [self.create_main_container()]

    def init_ui(self):
        """UI要素の初期化"""
        self.text_1 = ft.Text(
            "MyAppに新規登録 : STEP1", size=20, weight=ft.FontWeight.W_600, font_family="Segoe_UI_BOLD"
        )
        self.regist_mail = self.create_input_field("メールアドレスを入力", "example@gmail.com")
        self.regist_pass = self.create_input_field("パスワードを入力", "password", True, max_length=20, helper_text="英数字のみ 6~20字")
        self.regist_pass_confirm = self.create_input_field("パスワードの確認", "password", True, max_length=20)
        self.check_mail_wrap = self.create_checkbox("メールの受信を許可する")
        self.next_btn = ft.ElevatedButton(text="次へ", color="white", bgcolor="#00608d", on_click=self.go_to_step2, disabled=True)
        self.help_btn = ft.IconButton(ft.icons.HELP, on_click=self.show_step1_help)
        self.dlg_modal = self.create_alert_dialog()

    def create_input_field(self, label, hint_text, password=False, max_length=None, helper_text=None):
        """入力フィールドの作成"""
        return ft.TextField(
            label=label,
            hint_text=hint_text,
            password=password,
            can_reveal_password=password,
            width=310,
            max_length=max_length,
            helper_text=helper_text,
            on_change=self.validate_step1_form
        )

    def create_checkbox(self, label):
        """チェックボックスの作成"""
        return ft.Row(
            controls=[ft.Checkbox(label=label)],
            alignment=ft.MainAxisAlignment.START
        )

    def create_alert_dialog(self):
        """アラートダイアログの作成"""
        return ft.AlertDialog(
            modal=True,
            title=ft.Text("メッセージ"),
            actions=[ft.TextButton("OK", on_click=self.close_error_dialog)],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def create_main_container(self):
        """メインコンテナの作成"""
        return ft.Container(
            content=ft.Column(
                [
                    self.text_1,
                    ft.Container(height=2),
                    ft.Divider(color="grey", height=8),
                    ft.Container(height=2),
                    self.regist_mail,
                    ft.Container(height=1),
                    ft.Divider(color="transparent", height=-5),
                    self.regist_pass,
                    self.regist_pass_confirm,
                    ft.Divider(color="grey", height=10),
                    self.check_mail_wrap,
                    ft.Row(
                        [ft.Container(width=40), self.next_btn, self.help_btn],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=0,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor="#f2ede7",
            width=360,
            height=510,
            border_radius=10,
            padding=20,
            border=ft.border.all(1, "#f5f5f5"),
        )

    def validate_step1_form(self, e):
        """フォームのバリデーション"""
        valid = (
            self.regist_mail.value.count("@") == 1  
            and self.regist_mail.value.count(".") > 0  
            and 6 <= len(self.regist_pass.value) <= 20  
            and self.regist_pass.value.isalnum()  
            and self.regist_pass.value == self.regist_pass_confirm.value  
        )
        self.next_btn.disabled = not valid
        self.page.update()  

    def go_to_step2(self, e):
        """STEP2に進む"""
        self.page.session.set("email", self.regist_mail.value)  
        self.page.session.set("password", self.regist_pass.value)  
        self.page.session.set("email_opt_in", int(self.check_mail_wrap.controls[0].value))  
        self.page.go("/signup/2")  

    def show_step1_help(self, e):
        """STEP1のヘルプを表示"""
        errors = []
        if self.regist_mail.value.count("@") != 1 or self.regist_mail.value.count(".") == 0:  
            errors.append("・メールアドレスの形式が正しくありません。")
        if not (6 <= len(self.regist_pass.value) <= 20):  
            errors.append("・パスワードは6文字以上20文字以下にしてください。")
        if not self.regist_pass.value.isalnum():  
            errors.append("・パスワードは英数字のみ使用できます。")
        if self.regist_pass.value != self.regist_pass_confirm.value:  
            errors.append("・再入力のパスワードが一致していません。")

        if errors:
            self.dlg_modal.content = ft.Text("\n".join(errors))
        else:
            self.dlg_modal.content = ft.Text("すべての条件を満たしています！")

        self.page.dialog = self.dlg_modal  
        self.dlg_modal.open = True
        self.page.update()  

    def close_error_dialog(self, e):
        """エラーダイアログを閉じる"""
        self.dlg_modal.open = False
        self.page.update()  


class SignupStep2(ft.View):
    def __init__(self, page):
        super().__init__(
            route="/signup/2",
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.page = page
        self.page.title = "step2"
        self.bgcolor = "#aba7a5"

        # UI要素の初期化
        self.init_ui()

        # メインコンテナの設定
        self.controls = [self.create_main_container()]

    def init_ui(self):
        """UI要素の初期化"""
        self.text_1 = ft.Text(
            "MyAppに新規登録 : STEP2", size=20, weight=ft.FontWeight.W_600, font_family="Segoe_UI_BOLD"
        )
        self.regist_user_name = self.create_input_field("表示名", "例 : ゆうた")
        self.regist_any_user_id = self.create_input_field("ユーザーID", "例 : yuta2525", max_length=20, helper_text="英数字 と _ のみ", prefix_text="@")
        self.date_picker = self.create_date_picker()
        self.regist_btn = ft.ElevatedButton(text="登録", color="white", bgcolor="#00608d", on_click=self.register, disabled=True)
        self.help_btn = ft.IconButton(ft.icons.HELP, on_click=self.show_step2_help)
        self.dlg_message = self.create_alert_dialog("メッセージ", self.close_error_dialog)
        self.dlg_success = self.create_alert_dialog("メッセージ", self.close_success_dialog)

    def create_input_field(self, label, hint_text, max_length=None, helper_text=None, prefix_text=None):
        """入力フィールドの作成"""
        return ft.TextField(
            label=label,
            hint_text=hint_text,
            width=310,
            max_length=max_length,
            helper_text=helper_text,
            prefix_text=prefix_text,
            on_change=self.validate_step2_form
        )

    def create_date_picker(self):
        """日付ピッカーの作成"""
        date_picker = ft.DatePicker(
            first_date=datetime.datetime(1900, 1, 1),
            last_date=datetime.datetime(2050, 1, 1),
            date_picker_entry_mode="INPUT",  
            field_label_text="生年月日を入力 (mm/dd/yyyy)",
            error_format_text="mm/dd/yyyy の形で入力してください",
            error_invalid_text="選択された日付は範囲外です",
            field_hint_text="例 : 12/31/2000",
            value=datetime.date.today(),  
            on_change=self.validate_step2_form,
        )
        self.page.overlay.append(date_picker) 
        return date_picker

    def create_alert_dialog(self, title, on_click):
        """アラートダイアログの作成"""
        return ft.AlertDialog(
            modal=True,
            title=ft.Text(title),
            actions=[ft.TextButton("OK", on_click=on_click)],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def create_main_container(self):
        """メインコンテナの作成"""
        return ft.Container(
            content=ft.Column(
                [
                    self.text_1,
                    ft.Container(height=1),
                    ft.Divider(color="grey", height=8),
                    ft.Container(height=2),
                    self.regist_user_name,
                    self.regist_any_user_id,
                    ft.Container(height=1),
                    self.create_date_button(),
                    ft.Container(height=1),
                    ft.Container(height=1),
                    ft.Row(
                        [ft.Container(width=40), self.regist_btn, self.help_btn],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=0,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor="#f2ede7",
            width=360,
            height=440,
            border_radius=10,
            padding=20,
            border=ft.border.all(1, "#f5f5f5"),
        )

    def create_date_button(self):
        """日付選択ボタンの作成"""
        return ft.Container(
            content=ft.OutlinedButton(
                "生年月日を入力",
                icon=ft.icons.CALENDAR_MONTH,
                on_click=lambda _: self.date_picker.pick_date(),
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
            ),
            width=310,
        )

    def validate_step2_form(self, e):
        """フォームのバリデーション"""
        valid = (
            1 <= len(self.regist_user_name.value) <= 20  
            and 1 <= len(self.regist_any_user_id.value) <= 20  
            and self.date_picker.value.strftime("%Y-%m-%d")  
            != datetime.date.today().strftime("%Y-%m-%d")
            and self.regist_any_user_id.value.replace("_", "").isalnum()  
        )
        self.regist_btn.disabled = not valid
        self.page.update()  

    def register(self, e):
        """登録処理"""
        user_name = self.regist_user_name.value
        any_user_id = self.regist_any_user_id.value  
        email = self.page.session.get("email")  
        password = self.page.session.get("password")  
        email_opt_in = self.page.session.get("email_opt_in")  
        birth_date = self.date_picker.value

        birth_date_str = birth_date.strftime("%Y-%m-%d")  

        response = requests.post(
            "http://127.0.0.1:5000/register",
            json={
                "user_name": user_name,
                "any_user_id": any_user_id,
                "email": email,
                "password": password,
                "email_opt_in": email_opt_in,
                "birth_date": birth_date_str,
            },
        )

        if response.status_code == 201:
            self.dlg_success.content = ft.Text("登録に成功しました！")
            self.dlg_success.open = True
            self.page.dialog = self.dlg_success  
            self.page.update()  
        else:
            try:
                error_message = response.json().get("error", "Unknown error")
            except json.JSONDecodeError:  
                error_message = "サーバーからの無効な応答"

            self.dlg_message.content = ft.Text(f"登録に失敗しました。エラー: {error_message}")
            self.dlg_message.open = True
            self.page.dialog = self.dlg_message  
            self.page.update()  

    def show_step2_help(self, e):
        """STEP2のヘルプを表示"""
        errors = []

        if not (1 <= len(self.regist_user_name.value) <= 20):  
            errors.append("・表示名は1文字以上20文字以下にしてください")
        if not (1 <= len(self.regist_any_user_id.value) <= 20 and self.regist_any_user_id.value.replace("_", "").isalnum()):  
            errors.append("・ユーザーIDは英数字とアンダーバーのみ、1文字以上20文字以下にしてください")
        if self.date_picker.value.strftime("%Y-%m-%d") == datetime.date.today().strftime("%Y-%m-%d"):  
            errors.append("・正しい生年月日を入力してください")

        if errors:
            self.dlg_message.content = ft.Text("\n".join(errors))
        else:
            self.dlg_message.content = ft.Text("すべての条件を満たしています！")

        self.page.dialog = self.dlg_message  
        self.dlg_message.open = True
        self.page.update()  

    def close_success_dialog(self, e):
        """成功ダイアログを閉じる"""
        self.dlg_success.open = False
        self.page.update()  
        self.page.go("/login")  

    def close_error_dialog(self, e):
        """エラーダイアログを閉じる"""
        self.dlg_message.open = False
        self.page.update()  


if __name__ == "__main__":
    ft.app(target=SignupStep1)
    ft.app(target=SignupStep2)
