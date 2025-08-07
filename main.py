import flet as ft
from views.auth_view import AuthView
from views.profile_view import ProfileView
from views.connect_view import ConnectView
from supabase_client import supabase

def main(page: ft.Page):
    page.title = "SilverLink"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT

    # --- App Routes ---
    app_routes = {
        "/": AuthView(page), # Default route for web
        "/login": AuthView(page),
        "/profile": ProfileView(page),
        "/connect": ConnectView(page),
    }

    def route_change(route):
        page.views.clear()
        # Get the view for the current route, default to '/' if not found
        view = app_routes.get(page.route, app_routes["/"])
        page.views.append(view)
        page.go(page.route)

    page.on_route_change = route_change

    # --- Initial Route ---
    # Check if a user session exists to redirect
    try:
        session = supabase.auth.get_session()
        if session and session.user:
            page.go("/profile")
        else:
            page.go("/") # Go to the default login/auth view
    except Exception as e:
        print(f"Error checking session: {e}")
        page.go("/")

# This tells Flet to run the app in a web browser
if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
