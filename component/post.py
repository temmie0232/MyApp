
import flet as ft

class PostPage(ft.Container):
    def __init__(self):
        super().__init__(
            content=ft.Column([
                ft.Text("投稿を作成",size=20),
                ft.TextField(label="タイトル"),
                ft.TextField(label="内容",multiline=True),
                ft.ElevatedButton("submit")
            ]),
            padding=20
        )
    
    def submit_post(self,e):
        ...
        print("投稿が完了しました！")