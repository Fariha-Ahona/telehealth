from django.urls import path
from . import views

urlpatterns = [
    path("doctor/slots/", views.doctor_slots, name="doctor_slots"),
    path("doctors/", views.doctors_list, name="doctors_list"),
    path("slots/<int:doctor_id>/", views.available_slots, name="available_slots"),
    path("book/<int:slot_id>/", views.book_appointment, name="book_appointment"),

    path("doctor/dashboard/", views.doctor_dashboard, name="doctor_dashboard"),
    path("approve/<int:appointment_id>/", views.approve_appointment, name="approve_appointment"),
    path("reject/<int:appointment_id>/", views.reject_appointment, name="reject_appointment"),
    path("doctor/consultation/start/<int:appointment_id>/", views.start_consultation, name="start_consultation"),
    path("start-consultation/<int:appointment_id>/",views.start_consultation,name="start_consultation"),
    
]