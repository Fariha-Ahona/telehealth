import requests
from datetime import datetime
from django.conf import settings
from .zoom_token import get_zoom_access_token


def create_zoom_meeting(appointment):
    access_token = get_zoom_access_token()

    url = "https://api.zoom.us/v2/users/me/meetings"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    start_time = datetime.combine(
        appointment.slot.date,
        appointment.slot.start_time
    ).isoformat()

    data = {
        "topic": f"Consultation with {appointment.patient.username}",
        "type": 2,
        "start_time": start_time,
        "duration": 30,
        "timezone": "UTC",
        "settings": {
            "join_before_host": False,
            "waiting_room": True,
        },
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    return response.json()
