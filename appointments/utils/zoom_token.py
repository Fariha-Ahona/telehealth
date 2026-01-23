import requests
from django.conf import settings
from base64 import b64encode


def get_zoom_access_token():
    credentials = f"{settings.ZOOM_CLIENT_ID}:{settings.ZOOM_CLIENT_SECRET}"
    encoded_credentials = b64encode(credentials.encode()).decode()

    response = requests.post(
        "https://zoom.us/oauth/token",
        headers={
            "Authorization": f"Basic {encoded_credentials}",
        },
        data={
            "grant_type": "account_credentials",
            "account_id": settings.ZOOM_ACCOUNT_ID,
        },
    )

    response.raise_for_status()
    return response.json()["access_token"]
