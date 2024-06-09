
import flet as ft

class PostPage(ft.AlertDialog):
    def __init__(self):
        super().__init__(
            # 本体
            content = ft.Container(
                content = ft.Column([
                    # 取消ボタン
                    ft.IconButton(icon=ft.icons.CLOSE,icon_color=ft.colors.BLACK,on_click = self.close_dlg),
                    ft.TextField(hint_text="おなかすいたー",multiline=True,filled=True,border_radius=ft.border_radius.all(5),min_lines=10,border_color=ft.colors.GREY,bgcolor=ft.colors.WHITE),
                    
                    
                ]),
                height = 322,
                width = 500,
            ),
            actions=[ft.IconButton(icon=ft.icons.SEND,icon_color=ft.colors.BLACK,tooltip="投稿する")],
            bgcolor="#f2ede7",
        )
    
    def submit_post(self,e):
        ...
        print("投稿が完了しました！")
    
    def close_dlg(self, e):
        self.open = False
        self.update()