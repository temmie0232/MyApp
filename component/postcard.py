import flet as ft
import datetime

class PostCard(ft.Container):
    def __init__(self, post_data):
        super().__init__()
        
        # コンテナの基本設定
        self.configure_container()

        # 投稿データを元にUIを作成
        self.create_ui(post_data)

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
            offset=ft.Offset(0, 0),
            blur_style=ft.ShadowBlurStyle.OUTER,
        )
        self.width = 500

    def create_ui(self, post_data):
        """投稿データを使用してUIを構築する"""
        user_info = self.create_user_info(post_data)
        content_text = self.create_content_text(post_data)
        action_bar = self.create_action_bar()
        
        # スペース用コンテナ
        divider = self.create_divider(height=10)
        
        self.content = ft.Column([
            user_info,
            divider,
            content_text,
            divider,
            ft.Divider(thickness=0.6, height=4),
            action_bar,
        ],
            spacing=5,
        )

    def create_user_info(self, post_data):
        """ユーザー情報を表示するコンポーネントを作成"""
        user_name = post_data.get("user_name", "Unknown")
        any_user_id = post_data.get("any_user_id", "unknown_user")
        created_at_str = post_data.get("created_at", "")
        
        created_at = self.parse_datetime(created_at_str)
        
        # 現在のUTC時間を取得
        current_time = datetime.datetime.now(datetime.timezone.utc)

        # JSTに変換
        jst_offset = datetime.timedelta(hours=9)
        jst_current_time = current_time + jst_offset
        
        # 表示する時間差をフォーマット
        time_display = self.format_time_diff(created_at, jst_current_time)
        
        return ft.Row([
            ft.Icon(name=ft.icons.ACCOUNT_CIRCLE, size=26, color="#42474e"),
            ft.Text(f"{user_name}", weight="bold"),
            ft.Text(f"@{any_user_id} ", color="#888888"),
            ft.Text(time_display)
        ])

    def create_content_text(self, post_data):
        """投稿の内容を表示するテキストコンポーネントを作成"""
        content = post_data.get("content", "内容がありません")
        return ft.Text(f"{content}", max_lines=5)

    def create_action_bar(self):
        """アクションバーのコンポーネントを作成"""
        return ft.Container(
            content=ft.Row([
                self.create_icon_button(ft.icons.REPLY_OUTLINED, "返信"),
                self.create_icon_button(ft.icons.SYNC, "リポスト", selected_icon=ft.icons.SYNC, selected_color="#00ba7c"),
                self.create_icon_button(ft.icons.FAVORITE_BORDER, "いいね", selected_icon=ft.icons.FAVORITE, selected_color="#f91880"),
            ], height=29),
        )

    def create_icon_button(self, icon_name, tooltip, selected_icon=None, selected_color=None):
        """アイコンボタンを作成"""
        return ft.IconButton(
            icon=icon_name,
            selected_icon=selected_icon,
            tooltip=tooltip,
            icon_size=18,
            icon_color=ft.colors.BLACK,
            selected_icon_color=selected_color,
            selected=False,
            on_click=self.toggle_icon_button
        )

    def create_divider(self, height=10):
        """スペース用のコンテナを作成"""
        return ft.Container(height=height)

    def parse_datetime(self, date_str):
        """文字列の日付をdatetimeオブジェクトに変換"""
        formats = [
            "%Y-%m-%dT%H:%M:%S.%fZ",
            "%Y-%m-%dT%H:%M:%S.%f",
            "%a, %d %b %Y %H:%M:%S %Z"
        ]
        for fmt in formats:
            try:
                return datetime.datetime.strptime(date_str, fmt).replace(tzinfo=datetime.timezone.utc)
            except ValueError:
                continue
        raise ValueError(f"time data '{date_str}' does not match any known format")
    
    def format_time_diff(self, past_time, current_time):
        """時間の差をフォーマットして表示"""
        time_diff = current_time - past_time

        if time_diff.days >= 7:
            return past_time.strftime("%Y/%m/%d")
        elif time_diff.days > 0:
            return f"{time_diff.days}日前"
        elif time_diff.seconds >= 3600:
            hours = time_diff.seconds // 3600
            return f"{hours}時間前" if hours > 1 else "1時間前"
        elif time_diff.seconds >= 60:
            minutes = time_diff.seconds // 60
            return f"{minutes}分前" if minutes > 1 else "1分前"
        else:
            return "たった今"
        
    def toggle_icon_button(self, e):
        """アイコンボタンの状態を切り替える"""
        e.control.selected = not e.control.selected
        e.control.update()