import flet as ft
import requests

class PostPage(ft.AlertDialog):
    def __init__(self, page):
        super().__init__(
            content=self.create_dialog_content(),
            actions=[self.create_post_button()],
            bgcolor="#f2ede7",
            modal=True
        )
        
        self.page = page
        
        # 投稿フィールドと文字数カウンター
        self.text_field = self.create_text_field()
        self.text_count = ft.Text("0/200")
        
        # SnackBar for post completion
        self.page.snack_bar = ft.SnackBar(content=ft.Text("投稿が完了しました！"), action="OK")
        
    def create_text_field(self):
        """投稿フィールドを作成"""
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
        
    def create_dialog_content(self):
        """ダイアログのコンテンツを作成"""
        return ft.Container(
            content=ft.Column([
                ft.IconButton(
                    icon=ft.icons.CLOSE,
                    icon_color=ft.colors.BLACK,
                    on_click=self.close_dialog
                ),
                self.text_field,
                self.text_count
            ]),
            height=322,
            width=500,
        )

    def create_post_button(self):
        """投稿ボタンを作成"""
        return ft.IconButton(
            icon=ft.icons.SEND,
            icon_color=ft.colors.BLACK,
            tooltip="投稿する",
            on_click=self.submit_post
        )
        
    def close_dialog(self, e):
        """ダイアログを閉じる"""
        self.open = False
        self.page.update()  # type: ignore

    def reset_post(self):
        """投稿フィールドをリセット"""
        self.text_field.value = ""  # テキストフィールドを空白にする
        self.update_text_count(0)
        self.page.update()  # type: ignore

    def check_text_length(self, e):
        """投稿内容の文字数をチェック"""
        length = len(self.text_field.value)  # type: ignore
        self.update_text_count(length)
        
        self.post_btn.disabled = length > 200  # type: ignore
        self.page.update()  # type: ignore
            
    def update_text_count(self, length):
        """文字数カウンターを更新"""
        self.text_count.value = f"{length}/200"
        if length > 200:
            self.text_count.color = ft.colors.RED
            self.text_count.weight = ft.FontWeight.BOLD
            self.post_btn.tooltip = "文字数がオーバーしています"  # type: ignore
        else:
            self.text_count.color = ft.colors.BLACK
            self.text_count.weight = ft.FontWeight.NORMAL
            self.post_btn.tooltip = "投稿する"  # type: ignore
        
        self.page.update()  # type: ignore
    
    def submit_post(self, e):
        """投稿をサーバーに送信"""
        content = self.text_field.value
        any_user_id = self.page.session.get("any_user_id")  # type: ignore

        if any_user_id is None:
            print("このセッションでユーザーIDが使用できません")
            return ... # エラーハンドリングを追加する
        
        print(f"Posting as any_user_id: {any_user_id}") 
        
        response = requests.post("http://127.0.0.1:5000/post", json={"any_user_id": any_user_id, "content": content})
        
        if response.status_code == 201:
            print("投稿が完了しました！")
            self.page.snack_bar.open = True  # type: ignore
            self.reset_post()
            self.close_dialog(e)
            self.page.update()  # type: ignore
        else:
            print("投稿に失敗しました。")
