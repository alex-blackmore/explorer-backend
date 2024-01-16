from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
import requests
import os
from base64 import b64encode
from dotenv import load_dotenv

load_dotenv()
REDIRECT_URI = "http://localhost:5173/callback";
GRANT_TYPE = "authorization_code"
ACCESS_URL = "https://accounts.spotify.com/api"
ACCESS_TOKEN = "/token"
EXPECTED_SCOPE = "streaming playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public"
# Create your views here.
def login(request: HttpRequest):
    try:
        print(request.GET)
        access_code = request.GET["access_code"]
    except KeyError:
        return JsonResponse({"error": "No access code"}, status=400)
    encoded_details = b64encode(bytes(os.environ["CLIENT_ID"] + ":" + os.environ["CLIENT_SECRET"], encoding="utf-8")).decode("ascii")
    headers = {"Authorization": "Basic " + encoded_details, "Content-Type": "application/x-www-form-urlencoded"}
    body = {"code": access_code, "grant_type": GRANT_TYPE, "redirect_uri": REDIRECT_URI}
    response = requests.post(ACCESS_URL + ACCESS_TOKEN, body, headers=headers)
    if response.status_code != 200:
        return JsonResponse({"error": "Bad access code"}, status=400)
    result = response.json()
    if sorted(result["scope"].split()) != sorted(EXPECTED_SCOPE.split()):
        return JsonResponse({"error": "Could not authenticate with expected scope"}, status=400)
    user_access_token = result["access_token"]
    refresh_token = result["refresh_token"]
    response = JsonResponse({"access_token": user_access_token}, status=200)
    # update database with refresh token etc... TODO
    return response

