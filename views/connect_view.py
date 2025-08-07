import flet as ft
from supabase_client import supabase
import uuid

class ConnectView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/connect")
        self.page = page
        self.page.title = "Connect with Others"
        self.user = None

        # --- UI Controls ---
        self.connect_button = ft.ElevatedButton(
            text="Find a Match", 
            width=400, 
            height=80, 
            on_click=self.find_match,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15))
        )
        self.status_text = ft.Text("", size=22, text_align=ft.TextAlign.CENTER)
        self.profile_button = ft.TextButton("Edit Profile", on_click=lambda _: self.page.go("/profile"))

        self.controls = [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Connect with Others", size=40, weight=ft.FontWeight.BOLD, color="#005a9c"),
                        ft.Text("Find a friend who shares your interests.", size=20, color="#555"),
                        ft.Divider(height=50, color="transparent"),
                        self.connect_button,
                        ft.Divider(height=30, color="transparent"),
                        self.status_text,
                        self.profile_button,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        ]

    def did_mount(self):
        # Check for logged-in user
        try:
            self.user = supabase.auth.get_user().user
            if not self.user:
                self.page.go("/login")
        except Exception:
            self.page.go("/login")

    def find_match(self, e):
        self.status_text.value = "Searching for a match..."
        self.connect_button.disabled = True
        self.page.update()

        try:
            # Call the Supabase RPC function to find a match
            res = supabase.rpc('match_user', {'current_user_id': self.user.id}).execute()
            
            if res.data:
                matched_user = res.data[0]
                matched_user_id = matched_user['profile_id']
                matched_user_name = matched_user['name']
                self.status_text.value = f"Matched with {matched_user_name}!\nLaunching video call..."
                self.page.update()

                # Generate a unique, consistent room name
                user_ids = sorted([str(self.user.id), str(matched_user_id)])
                room_name = f"SilverLink-{'-'.join(user_ids)}"

                # Launch Jitsi video call in the browser
                self.page.launch_url(f"https://meet.jit.si/{room_name}")
            else:
                self.status_text.value = "No matches found right now.\nPlease try again later!"

        except Exception as err:
            self.status_text.value = f"An error occurred: {err}"
        
        self.connect_button.disabled = False
        self.page.update()
