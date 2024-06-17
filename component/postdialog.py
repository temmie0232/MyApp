import flet as ft
import requests

class PostPage(ft.AlertDialog):
    def __init__(self, page):
        
        self.page = page
        
        self.text_field = self.create_text_field()
        self.text_count = ft.Text("0/200")
        self.dlg = self.create_dlg()
        self.post_btn = self.create_post_btn()
        self.page.snack_bar = ft.SnackBar(content=ft.Text("投稿が完了しました！"), action="OK")
        
        super().__init__(
            content=self.dlg,
            actions=[self.post_btn],
            bgcolor="#f2ede7",
            modal=True
        )
        
    def create_text_field(self):
        return ft.TextField(
            hint_text="何が起きてる？",
            multiline=True,
            filled=True,
            border_radius=ft.border_radius.all(5),
            min_lines=10,
            border_color=ft.colors.GREY,
            bgcolor=ft.colors.WHITE,
            on_change=self.check_text_length,
        )
        
    def create_dlg(self):
        return ft.Container(
            content=ft.Column([
                ft.IconButton(
                    icon=ft.icons.CLOSE,
                    icon_color=ft.colors.BLACK,
                    on_click=self.close_dlg
                ),
                self.text_field,
                self.text_count
            ]),
            height=322,
            width=500,
        )

    def create_post_btn(self):
        return ft.IconButton(
            icon=ft.icons.SEND,
            icon_color=ft.colors.BLACK,
            tooltip="投稿する",
            on_click=self.submit_post
        )
        
    def close_dlg(self, e):
        self.open = False
        self.page.update() # type: ignore

    def reset_post(self):
        self.text_field.value = ""  # テキストフィールドを空白にする
        self.update_text_count(0)
        self.page.update()  # type: ignore # ページを更新して変更を反映

    def check_text_length(self, e):
        length = len(self.text_field.value) # type: ignore
        self.update_text_count(length)
        
        if length >= 200: # type: ignore
            self.post_btn.disabled = True
        else:
            self.post_btn.disabled = False
        
        self.page.update() # type: ignore
            
    def update_text_count(self, length):
        self.text_count.value = f"{length}/200"
        if length > 200:
            self.text_count.color = ft.colors.RED
            self.text_count.weight = ft.FontWeight.BOLD
            self.post_btn.tooltip = "文字数がオーバーしています"
        else:
            self.text_count.color = ft.colors.BLACK
            self.text_count.weight = ft.FontWeight.NORMAL
            self.post_btn.tooltip = "投稿する"
        
        self.page.update() # type: ignore
    
    def submit_post(self, e):
        content = self.text_field.value
        # ログインセッションからユーザーIDを取得
        any_user_id = self.page.session.get("any_user_id") # type: ignore

        if any_user_id is None:
            print("このセッションでユーザーIDが使用できません")
            return ... # エラーハンドリング

        print(f"any_user_id: <{any_user_id}> として投稿") 
        
        response = requests.post("http://127.0.0.1:5000/post", json={"any_user_id": any_user_id, "content": content})
        
        if response.status_code == 201:
            print("投稿が完了しました！")
            self.page.snack_bar.open = True # type: ignore
            self.reset_post()
            self.close_dlg(e)
            self.page.update() # type: ignore
        else:
            print("投稿に失敗しました。")