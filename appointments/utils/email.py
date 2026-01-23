from django.core.mail import send_mail
from django.conf import settings


def send_zoom_link_email(appointment):
    subject = "Your Zoom Consultation Link"

    message = f"""
Hello {appointment.patient.username},

Kindly find below the Zoom link for your upcoming consultation:

Doctor: Dr. {appointment.slot.doctor.username}
Date: {appointment.slot.date}
Time: {appointment.slot.start_time} - {appointment.slot.end_time}

Zoom Join Link:
{appointment.zoom_join_url}

Regards,
ECare Team
"""

    print("SENDING EMAIL TO:", appointment.patient.email)

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [appointment.patient.email, appointment.slot.doctor.email],
        fail_silently=False,
    )
