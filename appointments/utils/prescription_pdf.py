from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from django.conf import settings

def generate_prescription_pdf(appointment):
    folder = os.path.join(settings.MEDIA_ROOT, "prescriptions")
    os.makedirs(folder, exist_ok=True)

    filename = f"prescription_{appointment.id}.pdf"
    file_path = os.path.join(folder, filename)

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Medical Prescription")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Doctor: {appointment.slot.doctor.username}")
    c.drawString(50, height - 130, f"Patient: {appointment.patient.username}")

    text = c.beginText(50, height - 180)
    for line in appointment.prescription.split("\n"):
        text.textLine(line)

    c.drawText(text)
    c.showPage()
    c.save()

    # 🔥 VERY IMPORTANT
    return f"prescriptions/{filename}"
