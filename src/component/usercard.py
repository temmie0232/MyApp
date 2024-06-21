import flet as ft

class UserCard(ft.Container):
    def __init__(self, post_data, on_click):
        super().__init__()
        
        self.post_data = post_data
        self.on_click_handler = on_click 
        self.configure_container()
        self.create_ui(post_data)
        
        self.on_click = self.handle_click
        
    def configure_container(self):
        """コンテナの基本設定を行う"""
        self.padding = ft.padding.only(20, 20, 20, 10)
        self.margin = ft.margin.only(25, 5, 25, 5)
        self.bgcolor = "#ffffff"
        self.border_radius = 10
        self.shadow = ft.BoxShadow(
            spread_radius=0,
            blur_radius=5,
            color=ft.colors.GREY_400,
            offset=ft.Offset(0, 2),
            blur_style=ft.ShadowBlurStyle.OUTER,
        )
        self.width = 500

    def create_ui(self, post_data):
        """ユーザー情報からUIを構築する"""
        user_info = self.create_user_info(post_data)
        
        # UIコンポーネントを配置
        self.content = ft.Column([
            user_info,
        ],
        )

    def create_user_info(self, post_data):
        """ユーザー情報を表示するコンポーネントを作成"""
        user_name = post_data.get("user_name", "Unknown")
        any_user_id = post_data.get("any_user_id", "unknown_user")
        
        
        return ft.Row([
            ft.Icon(name=ft.icons.ACCOUNT_CIRCLE, size=26, color="#42474e"),
            ft.Text(f"{user_name}", weight="bold"), # type: ignore
            ft.Text(f"@{any_user_id}", color="#888888"),
        ])

    def handle_click(self, e):
        """クリックされたときの処理"""
        any_user_id = self.post_data.get("any_user_id", "unknown_user")
        if self.on_click_handler:
            self.on_click_handler(any_user_id)