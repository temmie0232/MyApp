import flet as ft
from login import Login
from signup import SignupStep1, SignupStep2
from home import MainPage

def main(page: ft.Page) -> None:
    print("プログラムが開始しました")
    
    page.title = "MyApp"
    page.theme_mode = ft.ThemeMode.LIGHT

    def navigate(route, view_class):
        view_instance = view_class(page)
        page.views.append(view_instance)
        print(f"{route} に移動しました")

    def route_handler(route):
        page.views.clear()
        routes = {
            "/flet/login": Login,
            "/flet/signup": SignupStep1,
            "/flet/signup/2": SignupStep2,
            "/flet/home": MainPage,
        }
        if page.route in routes:
            navigate(page.route, routes[page.route]) # type: ignore
        page.update()
    
    page.on_route_change = route_handler
    page.go("/flet/home")

if __name__ == "__main__":
    ft.app(
        name="MyApp",
        view=ft.AppView.WEB_BROWSER,
        target=main,
        assets_dir="assets",
        port=44444,
        host="0.0.0.0"
    )
