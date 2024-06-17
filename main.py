import flet as ft
from login import Login
from signup import SignupStep1, SignupStep2
from home import MainPage
from views.profile import ProfilePage  

def main(page: ft.Page) -> None:
    print("プログラムが開始しました")
    
    page.title = "MyApp"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # ページ移動用ルーター
    def router(route):
        page.views.clear()
        
        if page.route == "/" or page.route == "/login":
            print(f" / に移動しました")
            login = Login(page)
            page.views.append(login)

        elif page.route == "/signup":
            print(f" /signup に移動しました")
            signup1 = SignupStep1(page)
            page.views.append(signup1)

        elif page.route == "/signup/2":
            print(f" /signup/2 に移動しました")
            signup2 = SignupStep2(page)
            page.views.append(signup2)

        elif page.route == "/home":
            print(f" /home に移動しました")
            mainpage = MainPage(page)
            page.views.append(mainpage)

        elif page.route.startswith("/profile"): 
            any_user_id = page.route.split("/")[-1] 
            print(f" /profile に移動しました - ユーザーID: {any_user_id}")
            profile_page = ProfilePage(page, any_user_id=any_user_id)  # user_idをany_user_idに変更
            page.views.append(profile_page) 

        page.update()
    
    page.on_route_change = router
    
    #初期は"/"からスタート
    page.go("/")


if __name__ == "__main__":
    ft.app(
        name="flet",
        view=ft.AppView.WEB_BROWSER,
        target=main,
        assets_dir="assets",
        port=44444,
        host="0.0.0.0"
    )

