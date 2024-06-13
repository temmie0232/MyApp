import flet as ft
from login import Login
from signup import SignupStep1, SignupStep2
from home import MainPage

def main(page: ft.Page) -> None:
    print("プログラムが開始しました")
    
    page.title = "MyApp"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # ページ移動用ルーター
    def router(route):
        page.views.clear()
        
        if page.route == "/" or page.route == "/login":
            print(f"{route} に移動しました")
            login = Login(page)
            page.views.append(login)

        if page.route == "/signup":
            print(f"{route} に移動しました")
            signup1 = SignupStep1(page)
            page.views.append(signup1)

        if page.route == "/signup/2":
            print(f"{route} に移動しました")
            signup2 = SignupStep2(page)
            page.views.append(signup2)

        if page.route == "/home":
            print(f"{route} に移動しました")
            mainpage = MainPage(page)
            page.views.append(mainpage)

        if page.route.startswith("/profile"):
            user_id = page.route.split("/")[-1]
            print(f"{route} に移動しました - ユーザーID: {user_id}")
            profile_page = ProfilePage(page, user_id=user_id)
            page.views.append(profile_page)

        page.update()
    
    page.on_route_change = router
    
    #初期は"/"からスタート
    page.go("/")
    
    """
    def navigate(route, view_class):
        view_instance = view_class(page)
        page.views.append(view_instance)
        print(f"{route} に移動しました")

    def route_handler(route):
        page.views.clear()
        routes = {
            "/login": Login,
            "/signup": SignupStep1,
            "/signup/2": SignupStep2,
            "/home": MainPage,
        }
        if page.route in routes:
            navigate(page.route, routes[page.route]) # type: ignore
        page.update()

    page.on_route_change = route_handler
    page.go("/")
    """

if __name__ == "__main__":
    ft.app(
        name="flet",
        view=ft.AppView.WEB_BROWSER,
        target=main,
        assets_dir="assets",
        port=44444,
        host="0.0.0.0"
    )
