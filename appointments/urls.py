from django.urls import path
from . import views

urlpatterns = [
    path("doctor/slots/", views.doctor_slots, name="doctor_slots"),
    path("available/<int:doctor_id>/", views.available_slots, name="available_slots"),
    path("book/<int:slot_id>/", views.book_appointment, name="book_appointment"),
]
