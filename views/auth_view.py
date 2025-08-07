import flet as ft
from supabase_client import supabase

class AuthView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/login")
        self.page = page
        self.page.title = "Welcome to SilverLink"
        self.is_signup = False

        # --- UI Controls ---
        self.title_text = ft.Text("Login", size=40, weight=ft.FontWeight.BOLD, color="#005a9c")
        self.email_field = ft.TextField(label="Email", width=400, height=60, text_size=20, border_radius=10)
        self.password_field = ft.TextField(label="Password", password=True, can_reveal_password=True, width=400, height=60, text_size=20, border_radius=10)
        self.confirm_password_field = ft.TextField(label="Confirm Password", password=True, can_reveal_password=True, width=400, height=60, text_size=20, border_radius=10, visible=False)
        
        # Password Strength Indicator
        self.strength_bar = ft.ProgressBar(width=400, value=0, color="red", bgcolor="#e0e0e0", visible=False)
        self.strength_text = ft.Text("", size=16, visible=False)

        self.submit_button = ft.ElevatedButton(text="Login", width=400, height=60, on_click=self.handle_submit, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
        self.toggle_button = ft.TextButton(text="Don't have an account? Sign Up", on_click=self.toggle_mode)
        self.status_text = ft.Text("", size=18, color="red")

        self.password_field.on_change = self.update_password_strength

        self.controls = [
            ft.Container(
                content=ft.Column(
                    [
                        self.title_text,
                        ft.Text("Connecting seniors, one conversation at a time.", size=20, color="#555"),
                        ft.Divider(height=30, color="transparent"),
                        self.email_field,
                        self.password_field,
                        ft.Column([self.strength_bar, self.strength_text], spacing=5),
                        self.confirm_password_field,
                        ft.Divider(height=10, color="transparent"),
                        self.submit_button,
                        self.status_text,
                        self.toggle_button,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        ]

    def toggle_mode(self, e):
        self.is_signup = not self.is_signup
        self.status_text.value = ""
        if self.is_signup:
            self.title_text.value = "Sign Up"
            self.submit_button.text = "Sign Up"
            self.toggle_button.text = "Already have an account? Login"
            self.confirm_password_field.visible = True
            self.strength_bar.visible = True
            self.strength_text.visible = True
        else:
            self.title_text.value = "Login"
            self.submit_button.text = "Login"
            self.toggle_button.text = "Don't have an account? Sign Up"
            self.confirm_password_field.visible = False
            self.strength_bar.visible = False
            self.strength_text.visible = False
        self.page.update()

    def handle_submit(self, e):
        email = self.email_field.value
        password = self.password_field.value
        self.status_text.value = ""

        try:
            if self.is_signup:
                confirm_password = self.confirm_password_field.value
                if password != confirm_password:
                    raise Exception("Passwords do not match.")
                
                res = supabase.auth.sign_up({"email": email, "password": password})
                self.status_text.color = "green"
                self.status_text.value = "Sign-up successful! Please check your email."
            else:
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                self.page.go("/profile")
        except Exception as err:
            self.status_text.color = "red"
            self.status_text.value = str(err)
        self.page.update()

    def update_password_strength(self, e):
        if not self.is_signup: return
        password = self.password_field.value
        score = 0
        if len(password) >= 8: score += 1
        if any(c.isupper() for c in password): score += 1
        if any(c.islower() for c in password): score += 1
        if any(c.isdigit() for c in password): score += 1
        if any(not c.isalnum() for c in password): score += 1

        if len(password) == 0:
            self.strength_bar.value = 0
            self.strength_text.value = ""
        elif score <= 2:
            self.strength_bar.value = 0.33
            self.strength_bar.color = "red"
            self.strength_text.value = "Weak"
            self.strength_text.color = "red"
        elif score <= 4:
            self.strength_bar.value = 0.66
            self.strength_bar.color = "orange"
            self.strength_text.value = "Medium"
            self.strength_text.color = "orange"
        else:
            self.strength_bar.value = 1.0
            self.strength_bar.color = "green"
            self.strength_text.value = "Strong"
            self.strength_text.color = "green"
        self.page.update()
