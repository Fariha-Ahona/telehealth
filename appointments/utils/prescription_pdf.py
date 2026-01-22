# appointments/utils/prescription_pdf.py

import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.conf import settings
from django.core.files import File

def generate_prescription_pdf(appointment):
    folder = os.path.join(settings.MEDIA_ROOT, "prescriptions")
    os.makedirs(folder, exist_ok=True)

    file_name = f"prescription_{appointment.id}.pdf"
    file_path = os.path.join(folder, file_name)

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Medical Prescription")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Doctor: Dr. {appointment.slot.doctor.username}")
    c.drawString(50, height - 130, f"Patient: {appointment.patient.username}")
    c.drawString(50, height - 160, f"Date: {appointment.slot.date}")

    text = c.beginText(50, height - 220)
    text.setFont("Helvetica", 11)
    text.textLine("Prescription:")
    text.textLine("-------------------------")

    if appointment.prescription:
        for line in appointment.prescription.split("\n"):
            text.textLine(line)

    c.drawText(text)
    c.showPage()
    c.save()

    return File(open(file_path, "rb"), name=file_name)
