from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import DoctorAvailableSlot


@login_required
def doctor_slots(request):
    if request.method == "POST":
        DoctorAvailableSlot.objects.create(
            doctor=request.user,
            date=request.POST["date"],
            start_time=request.POST["start_time"],
            end_time=request.POST["end_time"],
        )
        return redirect("doctor_slots")

    slots = DoctorAvailableSlot.objects.filter(doctor=request.user)

    return render(request, "appointments/doctor_slots.html", {
        "slots": slots
    })

@login_required
def available_slots(request, doctor_id):
    slots = DoctorAvailableSlot.objects.filter(
        doctor_id=doctor_id,
        is_booked=False
    )
    return render(request, "appointments/patient_slots.html", {
        "slots": slots
    })
@login_required
def available_slots(request, doctor_id):
    slots = DoctorAvailableSlot.objects.filter(
        doctor__id=doctor_id,
        is_booked=False
    )

    return render(request, "appointments/available_slots.html", {
        "slots": slots
    })



from .models import Appointment


@login_required
def book_appointment(request, slot_id):
    slot = DoctorAvailableSlot.objects.get(id=slot_id)

    Appointment.objects.create(
        slot=slot,
        patient=request.user
    )

    slot.is_booked = True
    slot.save()

    return redirect("patient_dashboard")

