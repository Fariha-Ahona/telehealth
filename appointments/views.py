from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import DoctorAvailableSlot, Appointment
from .utils.prescription_pdf import generate_prescription_pdf
from .utils.email import send_zoom_link_email


# =========================
# DOCTOR: CREATE & VIEW SLOTS
# =========================
@login_required
def doctor_slots(request):
    if request.method == "POST":
        DoctorAvailableSlot.objects.create(
            doctor=request.user,
            date=request.POST["date"],
            start_time=request.POST["start_time"],
            end_time=request.POST["end_time"],
        )
        messages.success(request, "Slot added successfully ✅")
        return redirect("doctor_slots")
    slots = DoctorAvailableSlot.objects.filter(doctor=request.user)

    return render(request, "appointments/doctor_slots.html", {
        "slots": slots
    })


# =========================
# PATIENT: VIEW AVAILABLE SLOTS
# =========================
@login_required
def available_slots(request, doctor_id):
    slots = DoctorAvailableSlot.objects.filter(
        doctor_id=doctor_id,
        is_booked=False
    )

    return render(request, "appointments/available_slots.html", {
        "slots": slots
    })


# =========================
# PATIENT: BOOK APPOINTMENT
# =========================
@login_required
def book_appointment(request, slot_id):
    slot = get_object_or_404(
        DoctorAvailableSlot,
        id=slot_id,
        is_booked=False
    )

    # Prevent duplicate booking by same patient
    if Appointment.objects.filter(slot=slot).exists():
        messages.warning(request, "This slot is already requested.")
        return redirect("patient_dashboard")

    Appointment.objects.create(
        slot=slot,
        patient=request.user,
        status="PENDING"
    )

    # ❗ Slot is NOT booked yet (wait for doctor approval)
    messages.success(request, "Appointment request sent ✅")
    return redirect("patient_dashboard")


# =========================
# DOCTOR: DASHBOARD (VIEW PENDING APPOINTMENTS)
# =========================
@login_required
def doctor_dashboard(request):
    appointments = Appointment.objects.filter(
    slot__doctor=request.user
).select_related("patient", "slot").order_by("-created_at")


    return render(request, "dashboards/doctor.html", {
        "appointments": appointments
    })
 
@login_required
def patient_dashboard(request):
    appointments = (
        Appointment.objects
        .filter(patient=request.user)
        .select_related("slot", "slot__doctor")
        .order_by("-created_at")
    )

    return render(
        request,
        "dashboards/patient.html",
        {
            "appointments": appointments
        }
    )

from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def doctors_list(request):
    doctors = User.objects.filter(is_staff=True)
    return render(request, "appointments/doctors_list.html", {
        "doctors": doctors
    })
@login_required
def approve_appointment(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        slot__doctor=request.user
    )

    appointment.status = "APPROVED"
    appointment.save()

    # 🔥 FIX: slot booked করে দাও
    slot = appointment.slot
    slot.is_booked = True
    slot.save()

    return redirect("doctor_dashboard")


@login_required
def reject_appointment(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        slot__doctor=request.user
    )

    appointment.status = "REJECTED"
    appointment.save()

    return redirect("doctor_dashboard")


from .utils.zoom import create_zoom_meeting
def start_consultation(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        slot__doctor=request.user
    )

    if not appointment.zoom_start_url:
        zoom_data = create_zoom_meeting(appointment)

        appointment.zoom_start_url = zoom_data["start_url"]
        appointment.zoom_join_url = zoom_data["join_url"]
        appointment.consultation_status = "ONGOING"
        appointment.save()

        send_zoom_link_email(appointment)

    return render(
        request,
        "appointments/start_consultation.html",
        {"appointment": appointment}
    )

# @login_required
# def start_consultation(request, appointment_id):
#     appointment = get_object_or_404(
#         Appointment,
#         id=appointment_id,
#         slot__doctor=request.user
#     )

#     # status update
#     if appointment.consultation_status == "NOT_STARTED":
#         appointment.consultation_status = "ONGOING"
#         appointment.save()

#     return render(
#         request,
#         "appointments/start_consultation.html",
#         {"appointment": appointment}
#     )

#     appointment = get_object_or_404(
#         Appointment,
#         id=appointment_id,
#         slot_doctor=request.user
#     )

#     if not appointment.zoom_join_url:
#         meeting = create_zoom_meeting(
#             f"Consultation with {appointment.patient.username}"
#         )

#         appointment.zoom_join_url = meeting["join_url"]
#         appointment.zoom_start_url = meeting["start_url"]
#         appointment.consultation_status = "ONGOING"
#         appointment.save()

#     return render(
#         request,
#         "appointments/start_consultation.html",
#         {"appointment": appointment}
#     )

# @login_required
# def write_prescription(request, appointment_id):
#     appointment = get_object_or_404(
#         Appointment,
#         id=appointment_id,
#         slot__doctor=request.user
#     )

#     if request.method == "POST":
#         appointment.prescription = request.POST.get("prescription")
#         appointment.consultation_status = "COMPLETED"

#         pdf_file = generate_prescription_pdf(appointment)
#         appointment.prescription_pdf = pdf_file

#         appointment.save()
#         return redirect("doctor_dashboard")

    # return render(
    #     request,
    #     "appointments/write_prescription.html",
    #     {"appointment": appointment}
    # )
from django.core.mail import EmailMessage
from django.conf import settings

import os
from django.core.mail import EmailMessage
from django.conf import settings

@login_required
def write_prescription(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        slot__doctor=request.user
    )

    if request.method == "POST":
        appointment.prescription = request.POST.get("prescription")
        appointment.consultation_status = "COMPLETED"

        # generate PDF
        pdf_relative_path = generate_prescription_pdf(appointment)
        appointment.prescription_pdf = pdf_relative_path
        appointment.save()

        # ✅ FIXED PATH
        pdf_full_path = os.path.join(settings.MEDIA_ROOT, pdf_relative_path)

        # send email to patient
        email = EmailMessage(
            subject="Your Prescription",
            body=(
                f"Dear {appointment.patient.username},\n\n"
                f"Your consultation is completed.\n"
                f"Prescription is attached.\n\n"
                f"Doctor: {appointment.slot.doctor.username}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[appointment.patient.email],
        )

        email.attach_file(pdf_full_path)
        email.send(fail_silently=True)

        return redirect("doctor_dashboard")

    return render(
        request,
        "appointments/write_prescription.html",
        {"appointment": appointment}
    )
