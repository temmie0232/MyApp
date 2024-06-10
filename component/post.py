import flet as ft

class PostPage(ft.AlertDialog):
    def __init__(self, page):
        self.text_field = ft.TextField(
            hint_text="何が起きてる？",
            multiline=True,
            filled=True,
            border_radius=ft.border_radius.all(5),
            min_lines=10,
            border_color=ft.colors.GREY,
            bgcolor=ft.colors.WHITE
        )
        
        super().__init__(
            # 本体
            content=self.create_dlg(),
            actions=[self.create_post_btn()],
            bgcolor="#f2ede7",
            modal=True
        )
        
        self.page = page

    # 投稿用ダイアログの作成
    def create_dlg(self):
        return ft.Container(
            content=ft.Column([
                # 取消ボタン
                ft.IconButton(
                    icon=ft.icons.CLOSE,
                    icon_color=ft.colors.BLACK,
                    on_click=self.close_dlg
                ),
                self.text_field
            ]),
            height=322,
            width=500,
        )

    # 内容を投稿するボタンを作成
    def create_post_btn(self):
        return ft.IconButton(
            icon=ft.icons.SEND,
            icon_color=ft.colors.BLACK,
            tooltip="投稿する",
            on_click=self.submit_post
        )

    # ダイアログを閉じる
    def close_dlg(self, e):
        self.open = False
        self.page.update()

    # 投稿内容(フィールド)をリセット
    def reset_post(self):
        self.text_field.value = ""  # テキストフィールドを空白にする
        self.page.update()  # ページを更新して変更を反映

    # 投稿する
    def submit_post(self, e):
        print("投稿が完了しました！")
        self.reset_post()
