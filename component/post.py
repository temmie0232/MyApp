
import flet as ft

class PostPage(ft.AlertDialog):
    def __init__(self):
        super().__init__(
            # 本体
            content = ft.Container(
                content = ft.Column([
                    # 取消ボタン
                    ft.IconButton(icon=ft.icons.CLOSE,on_click = self.close_dlg),
                    ft.Text("i")
                ]),
                height = 200
            )
        )
    
    def submit_post(self,e):
        ...
        print("投稿が完了しました！")
    
    def close_dlg(self, e):
        self.open = False
        self.update()