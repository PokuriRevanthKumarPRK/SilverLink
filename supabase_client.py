import os
from supabase import create_client, Client

# Get Supabase credentials from environment variables
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

# Initialize Supabase client
# Add a check to ensure the app doesn't crash if keys are missing
if not url or not key:
    print("ERROR: SUPABASE_URL and SUPABASE_KEY environment variables are not set.")
    # You might want to handle this more gracefully
    supabase: Client = None
else:
    supabase: Client = create_client(url, key)
