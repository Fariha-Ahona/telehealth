# from django.db import models
# from accounts.models import User


# class DoctorAvailableSlot(models.Model):
#     doctor = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name="slots",
#         null=True,
#         blank=True
#     )
#     date = models.DateField()
#     start_time = models.TimeField()
#     end_time = models.TimeField()
#     is_booked = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.doctor.username} | {self.date} {self.start_time}-{self.end_time}"


# # class Appointment(models.Model):
# #     slot = models.OneToOneField(
# #         DoctorAvailableSlot,
# #         on_delete=models.CASCADE,
# #         related_name="appointment"
# #     )
# #     patient = models.ForeignKey(
# #         User,
# #         on_delete=models.CASCADE,
# #         related_name="appointments"
# #     )
# #     status = models.CharField(
# #         max_length=20,
# #         choices=[
# #             ("PENDING", "Pending"),
# #             ("APPROVED", "Approved"),
# #             ("REJECTED", "Rejected"),
# #         ],
# #         default="PENDING"
# #     )
# #     created_at = models.DateTimeField(auto_now_add=True)

# #     def __str__(self):
# #         return f"{self.patient.username} → {self.slot}"
# # consultation_status = models.CharField(
# #     max_length=20,
# #     choices=[
# #         ("NOT_STARTED", "Not Started"),
# #         ("ONGOING", "Ongoing"),
# #         ("COMPLETED", "Completed"),
# #     ],
# #     default="NOT_STARTED"
# # )
# # meeting_link = models.URLField(blank=True, null=True)
# from django.db import models
# from django.conf import settings

# User = settings.AUTH_USER_MODEL

# class Appointment(models.Model):
#     STATUS_CHOICES = (
#         ("PENDING", "Pending"),
#         ("APPROVED", "Approved"),
#         ("REJECTED", "Rejected"),
#     )

#     CONSULTATION_STATUS = (
#         ("NOT_STARTED", "Not Started"),
#         ("ONGOING", "Ongoing"),
#         ("COMPLETED", "Completed"),
#     )

#     patient = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name="patient_appointments"
#     )
#     doctor = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name="doctor_appointments"
#     )
#     slot = models.OneToOneField(
#         "DoctorAvailableSlot", on_delete=models.CASCADE
#     )

#     status = models.CharField(
#         max_length=20, choices=STATUS_CHOICES, default="PENDING"
#     )

#     # ✅ NEW FIELD
#     consultation_status = models.CharField(
#         max_length=20,
#         choices=CONSULTATION_STATUS,
#         default="NOT_STARTED"
#     )

#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.patient} → {self.doctor} ({self.status})"
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class DoctorAvailableSlot(models.Model):
    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="slots"
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.doctor} | {self.date} {self.start_time}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]

    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="appointments"
    )

    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="doctor_appointments",
        null=True,      # ✅ TEMPORARY
        blank=True      # ✅ TEMPORARY
    )

    slot = models.OneToOneField(
        DoctorAvailableSlot,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    consultation_status = models.CharField(
        max_length=20,
        choices=[("NOT_STARTED","NOT_STARTED"),("ONGOING","ONGOING"),("COMPLETED","COMPLETED")],
        default="NOT_STARTED"
    )

    def __str__(self):
        return f"{self.patient} → {self.doctor} ({self.status})"

