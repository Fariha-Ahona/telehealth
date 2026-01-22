from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class DoctorAvailableSlot(models.Model):
    doctor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="slots"
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.doctor} | {self.date} {self.start_time}-{self.end_time}"


class Appointment(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    )

    CONSULTATION_STATUS = (
        ("NOT_STARTED", "Not Started"),
        ("ONGOING", "Ongoing"),
        ("COMPLETED", "Completed"),
    )

    slot = models.ForeignKey(
        DoctorAvailableSlot,
        on_delete=models.CASCADE,
        related_name="appointments"
    )
    patient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="appointments"
    )

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="PENDING"
    )
    consultation_status = models.CharField(
        max_length=20,
        choices=CONSULTATION_STATUS,
        default="NOT_STARTED"
    )
    prescription = models.TextField(blank=True, null=True)

    prescription_pdf = models.FileField(
        upload_to="prescriptions/",
        blank=True,
        null=True
    )

    zoom_start_url = models.URLField(blank=True, null=True)
    zoom_join_url = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} → {self.slot}"
