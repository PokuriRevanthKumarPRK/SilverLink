import flet as ft
from supabase_client import supabase

class ProfileView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/profile")
        self.page = page
        self.page.title = "Your Profile"
        self.user = None

        # --- UI Controls ---
        self.name_field = ft.TextField(label="Name", width=400, height=60, text_size=20, border_radius=10)
        self.age_field = ft.TextField(label="Age", width=400, height=60, text_size=20, keyboard_type=ft.KeyboardType.NUMBER, border_radius=10)
        self.languages_field = ft.TextField(label="Languages (e.g., English, Mandarin)", width=400, height=60, text_size=20, border_radius=10)
        
        self.interests_field = ft.TextField(
            label="Your Interests",
            hint_text="e.g., gardening, cooking, playing mahjong",
            width=400, 
            text_size=20, 
            border_radius=10,
            multiline=True,
            min_lines=3
        )

        self.save_button = ft.ElevatedButton(text="Save & Continue", width=400, height=60, on_click=self.save_profile)
        self.logout_button = ft.ElevatedButton(text="Logout", width=400, height=60, on_click=self.logout, bgcolor="#6c757d", color="white")
        self.status_text = ft.Text("", size=18)

        self.controls = [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Your Profile", size=40, weight=ft.FontWeight.BOLD, color="#005a9c"),
                        ft.Text("Tell us a little about yourself.", size=20, color="#555"),
                        ft.Divider(height=20, color="transparent"),
                        self.name_field,
                        self.age_field,
                        self.languages_field,
                        self.interests_field,
                        ft.Divider(height=20, color="transparent"),
                        self.save_button,
                        self.logout_button,
                        self.status_text,
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
        # This method is called when the view is shown
        self.load_profile()

    def load_profile(self):
        try:
            self.user = supabase.auth.get_user().user
            if not self.user:
                self.page.go("/login")
                return

            # Load profile data
            profile_res = supabase.table("profiles").select("*").eq("id", self.user.id).execute()
            if profile_res.data:
                profile = profile_res.data[0]
                self.name_field.value = profile.get("name", "")
                self.age_field.value = str(profile.get("age", ""))
                self.languages_field.value = ", ".join(profile.get("languages", []))

            # Load interests data
            interests_res = supabase.table("interests").select("interest_tag").eq("user_id", str(self.user.id)).execute()
            if interests_res.data:
                user_interests = [item['interest_tag'] for item in interests_res.data]
                self.interests_field.value = ", ".join(user_interests)
            self.page.update()
        except Exception as e:
            self.status_text.value = f"Error loading profile: {e}"
            self.page.update()

    def save_profile(self, e):
        self.status_text.value = ""
        try:
            age_value = self.age_field.value
            if not age_value or not age_value.isdigit():
                raise ValueError("Age must be a valid number.")

            # Upsert profile data
            profile_data = {
                "id": str(self.user.id),
                "name": self.name_field.value,
                "age": int(age_value),
                "languages": [lang.strip() for lang in self.languages_field.value.split(",") if lang.strip()]
            }
            supabase.table("profiles").upsert(profile_data).execute()

            # Update interests by processing the text field
            interest_text = self.interests_field.value or ""
            # Simple AI-like processing: split by comma, trim whitespace, and filter out empty strings
            processed_interests = [interest.strip().lower() for interest in interest_text.split(",") if interest.strip()]
            
            # Delete old interests
            supabase.table("interests").delete().eq("user_id", str(self.user.id)).execute()
            
            # Insert new interests if any
            if processed_interests:
                interest_data = [
                    {"user_id": str(self.user.id), "interest_tag": interest}
                    for interest in set(processed_interests) # Use set to avoid duplicates
                ]
                supabase.table("interests").insert(interest_data).execute()

            self.page.go("/connect")
        except Exception as err:
            # Provide a clearer error message
            error_message = str(err.message) if hasattr(err, 'message') else str(err)
            self.status_text.value = f"Error saving: {error_message}"
            self.page.update()

    def toggle_interest(self, e):
        e.control.selected = not e.control.selected
        self.page.update()

    def logout(self, e):
        supabase.auth.sign_out()
        self.page.go("/login")
