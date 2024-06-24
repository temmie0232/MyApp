import flet as ft
import requests
from component.ui_utils import update_banner

class PostPage(ft.AlertDialog):
    def __init__(self, page, on_post_success=None):
        self.page = page
        self.on_post_success = on_post_success
        
        # テキストフィールドとカウント表示の作成
        self.text_field = self.create_text_field()
        self.text_count = ft.Text("0/200")
        
        # ダイアログと投稿ボタンの作成
        self.dlg = self.create_dlg()
        self.post_btn = self.create_post_btn()
        
        super().__init__(
            content=self.dlg,
            actions=[self.post_btn],
            bgcolor="#f2ede7",
            modal=True
        )
        
    def create_text_field(self):
        """テキストフィールドを作成"""
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
        """ダイアログを作成"""
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
        """投稿ボタンを作成"""
        return ft.IconButton(
            icon=ft.icons.SEND,
            icon_color=ft.colors.BLACK,
            tooltip="投稿する",
            on_click=self.submit_post
        )
        
    def close_dlg(self, e):
        """ダイアログを閉じる"""
        self.open = False
        self.page.update()  # ダイアログの状態を更新

    def reset_post(self):
        """投稿後の状態をリセットする"""
        self.text_field.value = ""  # テキストフィールドを空白にする
        self.update_text_count(0)  # テキストカウントをリセット
        self.page.update()  # ページを更新して変更を反映

    def check_text_length(self, e):
        """テキストの長さをチェックして表示"""
        length = len(self.text_field.value)  # テキストの長さを取得
        self.update_text_count(length)
        
        if length >= 200:  # 文字数が200を超えた場合の処理
            self.post_btn.disabled = True
        else:
            self.post_btn.disabled = False
        
        self.page.update()  # ページの状態を更新
            
    def update_text_count(self, length):
        """テキストのカウントを更新"""
        self.text_count.value = f"{length}/200"
        if length > 200:
            self.text_count.color = ft.colors.RED
            self.text_count.weight = ft.FontWeight.BOLD
            self.post_btn.tooltip = "文字数がオーバーしています"
        else:
            self.text_count.color = ft.colors.BLACK
            self.text_count.weight = ft.FontWeight.NORMAL
            self.post_btn.tooltip = "投稿する"
        
        self.page.update()  # ページの状態を更新
    
    def submit_post(self, e):
        """投稿をサーバーに送信"""
        content = self.text_field.value
        any_user_id = self.page.session.get("any_user_id")

        if any_user_id is None:
            print("このセッションでユーザーIDが使用できません")
            return

        print(f"any_user_id: <{any_user_id}> として投稿") 
        
        response = requests.post("http://127.0.0.1:5000/post", json={"any_user_id": any_user_id, "content": content})
        
        if response.status_code == 201:
            print("投稿が完了しました！")
            update_banner(self.page, message="投稿が完了しました！", action_text="OK")
            self.reset_post()
            self.close_dlg(e)
            
            # 投稿成功時にコールバック関数を呼び出す
            if self.on_post_success:
                self.on_post_success()
        else:
            print("投稿に失敗しました。")
            update_banner(self.page, message="投稿に失敗しました。", action_text="ok")