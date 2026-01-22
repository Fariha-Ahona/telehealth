import requests
from django.conf import settings
import base64

def get_zoom_access_token():
    url = "https://zoom.us/oauth/token"
    auth = base64.b64encode(
        f"{settings.ZOOM_CLIENT_ID}:{settings.ZOOM_CLIENT_SECRET}".encode()
    ).decode()

    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "grant_type": "account_credentials",
        "account_id": settings.ZOOM_ACCOUNT_ID,
    }

    r = requests.post(url, headers=headers, data=data)
    return r.json()["access_token"]


def create_zoom_meeting(topic):
    token = get_zoom_access_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    data = {
        "topic": topic,
        "type": 2,
        "settings": {
            "join_before_host": True,
            "waiting_room": False,
        },
    }

    r = requests.post(
        "https://api.zoom.us/v2/users/me/meetings",
        headers=headers,
        json=data,
    )

    return r.json()
