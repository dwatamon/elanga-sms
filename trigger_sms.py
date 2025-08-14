import requests

APP_URL = "https://your-app-name.up.railway.app/send_updates"

response = requests.get(APP_URL)

if response.status_code == 200:
    print("✅ SMS updates sent successfully.")
else:
    print(f"❌ Failed to send SMS. Status code: {response.status_code}")
