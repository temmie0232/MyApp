import time
import flet as ft
from openai import OpenAI

# OpenAI APIの設定
client = OpenAI()

class ChatPage(ft.Container):
    def __init__(self,page):
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

    # UIの初期化
    def initialize_ui(self):
        self.title = ft.Text("会話してみる", size = 28, weight = "w800") # type: ignore
        self.main = self.create_ChatContentDisplay()
        self.divider = ft.Divider(height = 6, color = "transparent")
        self.prompt = self.create_PromptField(self.main.content)

    # チャットが表示されるディスプレイの作成
    def create_ChatContentDisplay(self):
        return ft.Container(
            content = ft.ListView(
                expand = True,
                spacing = 15,
                auto_scroll = True,
            ),
            width = 520,
            height = 580,
            bgcolor = "#e0dfda",
            border_radius = 20,
            padding = 15,
        )

    # プロンプト入力フィールドの作成
    def create_PromptField(self, chat_list_view):
        return Prompt(chat_list_view)
     
    # メインレイアウトを作成
    def create_main_layout(self) -> ft.Column:
        return ft.Column(
            [
                self.title, # 見出し
                self.divider,
                self.main,  # チャット表示
                self.divider,   # スペース
                self.prompt,    # プロンプト入力欄 # type: ignore
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        
# メッセージ生成クラス
class CreateMessage(ft.Column):
    def __init__(self, name: str, message: str) -> None:
        self.name: str = name
        self.message: str = message
        self.text = ft.Text(self.message)
        super().__init__(spacing = 4)
        self.controls = [ft.Text(self.name,opacity = 0.6), self.text]

# ユーザー入力クラス
class Prompt(ft.TextField):
    def __init__(self, chat: ft.ListView) -> None:
        super().__init__(
            width = 520,
            height = 40,
            border_color = "black",
            content_padding = 10,
            cursor_color = "black",
            on_submit = self.run_prompt,
        )
        self.chat: ft.ListView = chat
        
        # テキストの出力アニメーション
    def animate_text_output(self, name: str, prompt: str) -> None:
        word_list: list = []
        msg = CreateMessage(name,"")
        self.chat.controls.append(msg)
        
        for word in list(prompt):
            word_list.append(word)
            msg.text.value = "".join(word_list)
            self.chat.update()
            time.sleep(0.016)
            
    def user_output(self, prompt: str) -> None:
        self.animate_text_output(name = "Me", prompt = prompt)

    def gpt_output(self, prompt: str) -> None:
        completion = client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = [
                {"role": "system", "content": "生意気な子供。何事もめんどくさそうにする。すべてタメ口で返答する。"},
                {"role": "user", "content": prompt}
            ]
        )
        response_text = completion.choices[0].message.content
        self.animate_text_output(name = "^^)", prompt = response_text) # type: ignore
    
    # すべてのメソッドを実行 
    def run_prompt(self, event) -> None:
        text = event.control.value
        self.value = "" # 入力フィールドをクリア
        
        self.user_output(prompt = text) # ユーザーの入力内容の表示
        self.gpt_output(prompt = text) # GPTの応答を表示

        self.value = ""
        self.update()
            
            