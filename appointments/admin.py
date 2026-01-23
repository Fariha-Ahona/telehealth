from django.contrib import admin
from .models import Appointment, DoctorAvailableSlot


@admin.register(DoctorAvailableSlot)
class DoctorAvailableSlotAdmin(admin.ModelAdmin):
    list_display = ("doctor", "date", "start_time", "end_time", "is_booked")
    list_filter = ("doctor", "date")
    search_fields = ("doctor__username",)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "patient",
        "get_doctor",
        "status",
        "consultation_status",
        "created_at",
    )
    list_filter = ("status", "consultation_status")
    search_fields = ("patient__username", "slot__doctor__username")

    def get_doctor(self, obj):
        return obj.slot.doctor
    get_doctor.short_description = "Doctor"
