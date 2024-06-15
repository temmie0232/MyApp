import datetime
import flet as ft
from flask import json
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

        self.text_1 = ft.Text(
            "MyAppに新規登録 : STEP1", size=20, weight=ft.FontWeight.W_600, font_family="Segoe_UI_BOLD"
        )

        self.regist_mail = ft.TextField(
            label="メールアドレスを入力",
            hint_text="example@gmail.com",
            width=310,
            on_change=self.validate_step1_form,
        )

        self.regist_pass = ft.TextField(
            label="パスワードを入力",
            hint_text="password",
            password=True,
            can_reveal_password=True,
            width=310,
            on_change=self.validate_step1_form,
            max_length=20,
            helper_text="英数字のみ 6~20字",
        )

        self.regist_pass_confirm = ft.TextField(
            label="パスワードの確認",
            hint_text="password",
            password=True,
            can_reveal_password=True,
            width=310,
            on_change=self.validate_step1_form,
            max_length=20,
        )

        self.check_mail_wrap = ft.Row(
            controls=[ft.Checkbox(label="メールの受信を許可する")], alignment=ft.MainAxisAlignment.START
        )

        self.next_btn = ft.ElevatedButton(
            text="次へ", color="white", bgcolor="#00608d", on_click=self.go_to_step2, disabled=True
        )

        self.help_btn = ft.IconButton(ft.icons.HELP, on_click=self.show_step1_help)

        self.next_help = ft.Row(
            [ft.Container(width=40), self.next_btn, self.help_btn],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0,
        )

        self.register_ct = ft.Container(
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
                    self.next_help,
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

        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("メッセージ"),
            actions=[ft.TextButton("OK", on_click=self.close_error_dialog)],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.controls = [self.register_ct]

    def validate_step1_form(self, e):
        valid = (
            self.regist_mail.value.count("@") == 1 # type: ignore
            and self.regist_mail.value.count(".") > 0 # type: ignore
            and 6 <= len(self.regist_pass.value) <= 20 # type: ignore
            and self.regist_pass.value.isalnum() # type: ignore
            and self.regist_pass.value == self.regist_pass_confirm.value
        )

        self.next_btn.disabled = not valid
        self.page.update() # type: ignore

    def go_to_step2(self, e):
        self.page.session.set("email", self.regist_mail.value) # type: ignore
        self.page.session.set("password", self.regist_pass.value) # type: ignore
        self.page.session.set("email_opt_in", int(self.check_mail_wrap.controls[0].value))  # type: ignore
        self.page.go("/signup/2") # type: ignore

    def show_step1_help(self, e):
        errors = []
        if self.regist_mail.value.count("@") != 1 or self.regist_mail.value.count(".") == 0: # type: ignore
            errors.append("・メールアドレスの形式が正しくありません。")
        if not (6 <= len(self.regist_pass.value) <= 20): # type: ignore
            errors.append("・パスワードは6文字以上20文字以下にしてください。")
        if not self.regist_pass.value.isalnum(): # type: ignore
            errors.append("・パスワードは英数字のみ使用できます。")
        if self.regist_pass.value != self.regist_pass_confirm.value:
            errors.append("・再入力のパスワードが一致していません。")

        if errors:
            self.dlg_modal.content = ft.Text("\n".join(errors))
        else:
            self.dlg_modal.content = ft.Text("すべての条件を満たしています！")

        self.page.dialog = self.dlg_modal # type: ignore
        self.dlg_modal.open = True
        self.page.update() # type: ignore

    def close_error_dialog(self, e):
        self.dlg_modal.open = False
        self.page.update() # type: ignore


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

        self.text_1 = ft.Text(
            "MyAppに新規登録 : STEP2", size=20, weight=ft.FontWeight.W_600, font_family="Segoe_UI_BOLD"
        )

        self.regist_user_name = ft.TextField(
            label="表示名",
            hint_text="例 : ゆうた",
            width=310,
            on_change=self.validate_step2_form,
            max_length=20,
        )

        self.regist_any_user_id = ft.TextField(
            label="ユーザーID",
            hint_text="例 : yuta2525",
            width=310,
            on_change=self.validate_step2_form,
            max_length=20,
            helper_text="英数字 と _ のみ",
            prefix_text="@"
        )

        self.date_picker = ft.DatePicker(
            first_date=datetime.datetime(1900, 1, 1),
            last_date=datetime.datetime(2050, 1, 1),
            date_picker_entry_mode="INPUT", # type: ignore
            field_label_text="生年月日を入力 (mm/dd/yyyy)",
            error_format_text="mm/dd/yyyy の形で入力してください",
            error_invalid_text="選択された日付は範囲外です",
            field_hint_text="例 : 12/31/2000",
            value=datetime.date.today(), # type: ignore
            on_change=self.validate_step2_form,
        )

        page.overlay.append(self.date_picker)

        self.date_btn = ft.Container(
            content=ft.OutlinedButton(
                "生年月日を入力",
                icon=ft.icons.CALENDAR_MONTH,
                on_click=lambda _: self.date_picker.pick_date(),
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
            ),
            width=310,
        )

        self.regist_btn = ft.ElevatedButton(
            text="登録", color="white", bgcolor="#00608d", on_click=self.register, disabled=True
        )

        self.help_btn = ft.IconButton(ft.icons.HELP, on_click=self.show_step2_help)

        self.next_help = ft.Row(
            [ft.Container(width=40), self.regist_btn, self.help_btn],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0,
        )

        self.dlg_message = ft.AlertDialog(
            modal=True,
            title=ft.Text("メッセージ"),
            actions=[ft.TextButton("OK", on_click=self.close_error_dialog)],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.dlg_success = ft.AlertDialog(
            modal=True,
            title=ft.Text("メッセージ"),
            actions=[ft.TextButton("OK", on_click=self.close_success_dialog)],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.controls = [
            ft.Container(
                content=ft.Column(
                    [
                        self.text_1,
                        ft.Container(height=1),
                        ft.Divider(color="grey", height=8),
                        ft.Container(height=2),
                        self.regist_user_name,
                        self.regist_any_user_id,
                        ft.Container(height=1),
                        self.date_btn,
                        ft.Container(height=1),
                        ft.Container(height=1),
                        self.next_help,
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
        ]

    def validate_step2_form(self, e):
        valid = (
            1 <= len(self.regist_user_name.value) <= 20 # type: ignore
            and 1 <= len(self.regist_any_user_id.value) <= 20 # type: ignore
            and self.date_picker.value.strftime("%Y-%m-%d") # type: ignore
            != datetime.date.today().strftime("%Y-%m-%d")
            and self.regist_any_user_id.value.replace("_", "").isalnum() # type: ignore
        )

        self.regist_btn.disabled = not valid
        self.page.update() # type: ignore

    def register(self, e):
        user_name = self.regist_user_name.value
        any_user_id = "@" + self.regist_any_user_id.value.lstrip("@") # type: ignore
        email = self.page.session.get("email") # type: ignore
        password = self.page.session.get("password") # type: ignore
        email_opt_in = self.page.session.get("email_opt_in") # type: ignore
        birth_date = self.date_picker.value

        birth_date_str = birth_date.strftime("%Y-%m-%d") # type: ignore

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
            self.page.dialog = self.dlg_success # type: ignore
            self.page.update() # type: ignore
        else:
            try:
                error_message = response.json().get("error", "Unknown error")
            except json.JSONDecodeError: # type: ignore
                error_message = "サーバーからの無効な応答"

            self.dlg_message.content = ft.Text(f"登録に失敗しました。エラー: {error_message}")
            self.dlg_message.open = True
            self.page.dialog = self.dlg_message # type: ignore
            self.page.update() # type: ignore

    def show_step2_help(self, e):
        errors = []

        if not (1 <= len(self.regist_user_name.value) <= 20): # type: ignore
            errors.append("・表示名は1文字以上20文字以下にしてください")
        if not (1 <= len(self.regist_any_user_id.value) <= 20 and self.regist_any_user_id.value.replace("_", "").isalnum()): # type: ignore
            errors.append("・ユーザーIDは英数字とアンダーバーのみ、1文字以上20文字以下にしてください")
        if self.date_picker.value.strftime("%Y-%m-%d") == datetime.date.today().strftime("%Y-%m-%d"): # type: ignore
            errors.append("・正しい生年月日を入力してください")

        if errors:
            self.dlg_message.content = ft.Text("\n".join(errors))
        else:
            self.dlg_message.content = ft.Text("すべての条件を満たしています！")

        self.page.dialog = self.dlg_message # type: ignore
        self.dlg_message.open = True
        self.page.update() # type: ignore

    def close_success_dialog(self, e):
        self.dlg_success.open = False
        self.page.update() # type: ignore
        self.page.go("/login") # type: ignore

    def close_error_dialog(self, e):
        self.dlg_message.open = False
        self.page.update() # type: ignore


if __name__ == "__main__":
    ft.app(target=SignupStep1)
    ft.app(target=SignupStep2)
