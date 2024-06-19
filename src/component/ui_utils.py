import flet as ft

def update_banner(page: ft.Page, message: str = "更新しました！", action_text: str = "OK"):
    """
    バナーを作成して表示する。

    この関数は、ページ上にスナックバーを作成し、更新メッセージを表示する。
    バナーはデフォルトで「更新しました！」というメッセージと「OK」というアクションボタンを持ちますが、これらは引数を通じてカスタマイズ可能できる。

    Args:
        page (ft.Page): スナックバーを表示するFletのページオブジェクト。
        message (str, optional): バナーに表示するメッセージ。デフォルトは「プロフィールを更新しました！」。
        action_text (str, optional): バナーのアクションボタンに表示するテキスト。デフォルトは「OK」。

    Example:
        ```python
        from ui_utils import show_profile_update_banner
        import flet as ft

        # ページオブジェクトを作成
        page = ft.Page()

        # バナーを表示する
        show_profile_update_banner(page, message="プロファイルが正常に更新されました！", action_text="了解")
        ```

    """
    snack_bar = ft.SnackBar(content=ft.Text(message), action=action_text)
    page.snack_bar = snack_bar
    page.snack_bar.open = True
    page.update()
