import time
import flet as ft
from openai import OpenAI

# OpenAI APIの設定
client = OpenAI()

class ChatPage(ft.Container):
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

    def initialize_ui(self):
        """UIの初期化"""
        self.title = ft.Text("会話してみる", size=28, weight="w800")  # type: ignore
        self.chat_display = ChatContentDisplay()
        self.prompt = PromptField(self.chat_display.list_view)

    def create_main_layout(self) -> ft.Column:
        """メインレイアウトの作成"""
        return ft.Column(
            [
                self.title,  # 見出し
                ft.Divider(height=6, color="transparent"),  # スペース
                self.chat_display,  # チャット表示
                ft.Divider(height=6, color="transparent"),  # スペース
                self.prompt,  # プロンプト入力欄
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

class ChatContentDisplay(ft.Container):
    def __init__(self):
        super().__init__()
        self.list_view = ft.ListView(
            expand=True,
            spacing=15,
            auto_scroll=True,
        )
        self.setup_ui()

    def setup_ui(self):
        """チャットが表示されるディスプレイの設定"""
        self.width = 520
        self.height = 580
        self.bgcolor = "#e0dfda"
        self.border_radius = 20
        self.padding = 15
        self.content = self.list_view

class Message(ft.Column):
    def __init__(self, name: str, message: str) -> None:
        super().__init__(spacing=4)
        self.controls = [
            ft.Text(name, opacity=0.6), 
            ft.Text(message)
        ]

class PromptField(ft.TextField):
    def __init__(self, chat_list_view: ft.ListView) -> None:
        super().__init__(
            width=520,
            height=40,
            border_color="black",
            content_padding=10,
            cursor_color="black",
            on_submit=self.run_prompt,
        )
        self.chat_list_view = chat_list_view

    def animate_text_output(self, name: str, prompt: str) -> None:
        """テキストの出力アニメーション"""
        msg = Message(name, "")
        self.chat_list_view.controls.append(msg)
        self.chat_list_view.update()

        for char in prompt:
            msg.controls[1].value += char  # メッセージのテキストを更新
            self.chat_list_view.update()
            time.sleep(0.016)

    def display_user_message(self, prompt: str) -> None:
        """ユーザーのメッセージを表示"""
        self.animate_text_output(name="Me", prompt=prompt)

    def display_gpt_response(self, prompt: str) -> None:
        """GPTの応答を表示"""
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "生意気な子供。何事もめんどくさそうにする。すべてタメ口で返答する。"},
                {"role": "user", "content": prompt}
            ]
        )
        response_text = completion.choices[0].message.content
        self.animate_text_output(name="^^)", prompt=response_text)  # type: ignore

    def run_prompt(self, event) -> None:
        """プロンプトを実行"""
        text = event.control.value
        self.value = ""  # 入力フィールドをクリア

        self.display_user_message(prompt=text)  # ユーザーの入力内容を表示
        self.display_gpt_response(prompt=text)  # GPTの応答を表示

        self.value = ""
        self.update()
