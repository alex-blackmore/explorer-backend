from base64 import b64encode
import requests

ACCESS_URL = "https://accounts.spotify.com/api"
ACCESS_TOKEN = "/token"

def get_access_token(client_id: str, client_secret: str) -> str:
    data = {"grant_type": "client_credentials"}
    encoded_details = b64encode(bytes(client_id + ":" + client_secret, encoding="utf-8")).decode("ascii")
    headers = {"Authorization": "Basic " + encoded_details, "Content-Type": "application/x-www-form-urlencoded"}
    
    response = requests.post(ACCESS_URL + ACCESS_TOKEN, data, headers=headers)
    return response.json()['access_token']