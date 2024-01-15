from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import requests
import os
from dotenv import load_dotenv
from helpers import get_access_token

load_dotenv()
REDIRECT_URI = "http://localhost:5173/callback";
GRANT_TYPE = "authorization_code"
ACCESS_URL = "https://accounts.spotify.com/api"
ACCESS_TOKEN = "/token"

# Create your views here.
def login(request: HttpRequest):
    try:
        access_code = request.GET['access_code']
    except KeyError:
        return HttpResponse("No access code", status=400)
    access_token = get_access_token(os.environ["client_id"], os.environ["client_secret"])
    headers = {"Authorization": "Bearer " + access_token, "content-type": "application/x-www-form-urlencoded"}
    body = {"code": access_code, "grant_type": GRANT_TYPE, "redirect_uri": REDIRECT_URI}
    response = requests.post(ACCESS_URL + ACCESS_TOKEN, body, headers=headers)