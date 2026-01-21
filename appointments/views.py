from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import DoctorAvailableSlot, Appointment


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
        slot__doctor=request.user,
        status="PENDING"
    ).select_related("patient", "slot")

    return render(request, "dashboards/doctor.html", {
        "appointments": appointments
    })


# =========================
# DOCTOR: APPROVE APPOINTMENT
# =========================
@login_required
def approve_appointment(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        slot__doctor=request.user
    )

    if appointment.status != "PENDING":
        messages.warning(request, "This appointment is already processed.")
        return redirect("doctor_dashboard")

    appointment.status = "APPROVED"
    appointment.save()

    # Now lock the slot
    appointment.slot.is_booked = True
    appointment.slot.save()

    messages.success(request, "Appointment approved successfully ✅")
    return redirect("doctor_dashboard")


# =========================
# DOCTOR: REJECT APPOINTMENT
# =========================
@login_required
def reject_appointment(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        slot__doctor=request.user
    )

    if appointment.status != "PENDING":
        messages.warning(request, "This appointment is already processed.")
        return redirect("doctor_dashboard")

    appointment.status = "CANCELLED"
    appointment.save()

    # Slot stays available for others
    appointment.slot.is_booked = False
    appointment.slot.save()

    messages.success(request, "Appointment rejected ❌")
    return redirect("doctor_dashboard")
# =========================
# PATIENT: DASHBOARD (VIEW APPOINTMENTS)    
@login_required
def patient_dashboard(request):
    appointments = Appointment.objects.filter(
        patient=request.user
    ).select_related("slot", "slot__doctor").order_by("-created_at")

    return render(request, "dashboards/patient.html", {
        "appointments": appointments
    })
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def doctors_list(request):
    doctors = User.objects.filter(is_staff=True)
    return render(request, "appointments/doctors_list.html", {
        "doctors": doctors
    })
