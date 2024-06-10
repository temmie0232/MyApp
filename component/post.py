
import flet as ft
class PostPage(ft.AlertDialog):
    def __init__(self,page):
        super().__init__(
            # 本体
            content = ft.Container(
                content = ft.Column([
                    # 取消ボタン
                    ft.IconButton(icon=ft.icons.CLOSE,icon_color=ft.colors.BLACK,on_click = self.close_dlg),
                    ft.TextField(hint_text="投稿内容 : おなかすいたー",
                                 multiline=True,
                                 filled=True,
                                 border_radius=ft.border_radius.all(5),
                                 min_lines=10,
                                 border_color=ft.colors.GREY,
                                 bgcolor=ft.colors.WHITE,
                                 on_change=self.text_field_changed),
                ]),
                height = 322,
                width = 500,
            ),
            actions=[ft.IconButton(icon=ft.icons.SEND,icon_color=ft.colors.BLACK,tooltip="投稿する",on_click=self.submit_post)],
            bgcolor="#f2ede7",
        )
        
        self.page = page

        
    def text_field_changed(self,e):
        print("テキストフィールドが変更されました")
        # テキストフィールドに変更があった場合、フラグを更新
        self.text_modified = bool(e.control.value.strip())
        print(self.text_modified)
    

    def close_dlg(self, e):
        # テキストフィールドが変更されている場合、確認ダイアログを表示
        if self.text_modified:
            self.open = False
            self.page.update()
            #self.show_confirmation_dialog()
        # 変更がない場合、そのまま閉じる
        else:
            #
            self.open = False
            self.page.update()
            
    def reset_post(self):
        pass
    
    def submit_post(self,e):
        print("投稿が完了しました！")
        self.reset_post()