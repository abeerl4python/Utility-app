import requests
import base64

# Your client_id and client_secret
client_id = '15b7295fa22a4ee1ae8340c3d2506cb6'
client_secret = '9d7ed2fde08b404eb41ed5e4141a7006'

# Base64 encode client_id:client_secret
auth = f"{client_id}:{client_secret}"
base64_auth = base64.b64encode(auth.encode('utf-8')).decode('utf-8')

# Spotify token URL
url = 'https://accounts.spotify.com/api/token'

# Headers
headers = {
    'Authorization': f'Basic {base64_auth}',
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Data to request the token
data = {
    'grant_type': 'client_credentials'
}

# Send POST request
response = requests.post(url, headers=headers, data=data)

# Get the access token from the response
if response.status_code == 200:
    access_token = response.json()['access_token']
    print(f"Access Token: {access_token}")
else:
    print(f"Failed to get token: {response.status_code} - {response.text}")
