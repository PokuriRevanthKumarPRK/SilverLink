# SilverLink - Flet Web App

This is the web-based version of the SilverLink application, designed to connect seniors through shared interests. It is built with the Flet framework for Python and uses Supabase for the backend.

## Features
- User sign-up and login
- User profiles with name, age, languages, and interests
- AI-powered matching to connect with other users
- Jitsi-based video calls

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-github-repo-url>
    cd SilverLink_Flet_Web
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Supabase:**
    - Rename `config.py.template` to `config.py`.
    - Open `config.py` and replace the placeholder values with your actual Supabase URL and anon key.

5.  **Run the application:**
    ```bash
    python main.py
    ```
The application will be available at `http://127.0.0.1:8550`.
