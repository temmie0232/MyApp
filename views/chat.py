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
        self.bgcolor = ft.colors.WHITE
        self.border_radius = 10
        self.expand = True
        
        self.initialize_ui()
        self.content = ft.Text("テスト") #controls = [self.chat_container]
    
    def initialize_ui(self):
        # メインコンテンツ
        self.main_content = self.create_main_content_area()
        self.chat_list = self.main_content.content  # ft.ListView へのアクセスを取得
    
        # プロンプトフィールド
        self.prompt = self.create_prompt_field(chat = self.chat_list)

        self.chat_container = self.create_container()

    def create_main_content_area(self) -> ft.Container:
        chat = ft.ListView(
            expand=True,
            spacing=15,
            auto_scroll=True,
        )
        return ft.Container(
            content = chat,
            width = 420,
            height = 500,
            bgcolor = "#131518",
            border_radius = 10,
            padding = 15,
        )
        
    def create_prompt_field(self,chat: ft.ListView) -> ft.TextField:
        prompt = ft.TextField(
            width = 420,
            height = 40,
            border_color = "white",
            content_padding = 10,
            cursor_color = "white",
            on_submit = lambda event: self.run_prompt(event, chat)
        )
        return prompt

    def animate_text_output(self, chat: ft.ListView, name: str, prompt: str) -> None:
        word_list: list = []
        msg = CreateMessage(name,"")
        chat.controls.append(msg)

        for word in list(prompt):
            word_list.append(word)
            msg.text.value = "".join(word_list)
            chat.update()
            time.sleep(0.016)
            
    def create_container(self):
        return ft.Container(
            content=ft.Column([
                ft.Text("話しかけてみよう", size=28, weight = "w800"), # type: ignore
                self.main_content,
                ft.Divider(height = 6, color = "transparent"),
                self.prompt,
            ])
        )
            
    def user_output(self, chat: ft.ListView, prompt: str) -> None:
        self.animate_text_output(chat, name="Me", prompt=prompt)

    def gpt_output(self, chat: ft.ListView, prompt: str) -> None:
        completion = client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = [
                {"role":"system","content":"大阪弁のロボット"},
                {"role":"user","content":prompt}
            ]
        )
        response_text = completion.choices[0].message.content
        self.animate_text_output(chat, name="ChatGPT", prompt = response_text)
        
    def run_prompt(self, event, chat: ft.ListView) -> None:
        text = event.control.value
        event.control.value = ""    # 入力フィールドのクリア

        self.user_output(chat, prompt = text)   # ユーザーの入力を表示
        self.gpt_output(chat, prompt = text)    # GPTの応答を表示

        event.control.update()

# メッセージ生成クラス
class CreateMessage(ft.Column):
    def __init__(self, name: str, message: str) -> None:
        self.name: str = name   # メッセージの送信者名
        self.message: str = message
        self.text = ft.Text(self.message)
        super().__init__(spacing = 4)
        self.controls = [ft.Text(self.name, opacity = 0.6), self.text]
    