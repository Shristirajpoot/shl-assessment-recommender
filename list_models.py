import requests
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GOOGLE_API_KEY}"
resp = requests.get(url)
print(resp.status_code)
if resp.status_code == 200:
    models = resp.json()
    for m in models.get('models', []):
        print(m['name'])
else:
    print(resp.text)
