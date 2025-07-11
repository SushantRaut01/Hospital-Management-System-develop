from django.http import JsonResponse
from assistant.models import Patient_Data
from django.http import JsonResponse
from .models import Medicine, Prescription
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MedicineNameSerializer
from uuid import uuid5, NAMESPACE_DNS
from rest_framework import status


def incoming_patients(request):
    patients = Patient_Data.objects.filter(status__in=["In Clinic", "Emergency"]).order_by("created_at")
    data = list(patients.values())  # convert queryset to list of dicts
    return JsonResponse(data, safe=False)


def search_medicine(request):
    query = request.GET.get('q', '')
    if query:
        meds = Medicine.objects.filter(name__istartswith=query).values('uid', 'name')[:15]
    else:
        meds = []
    return JsonResponse(list(meds), safe=False)



@api_view(['GET'])
def autocomplete_medicine_api(request):
    query = request.GET.get("q", "")
    results = []

    if query:
        results = Medicine.objects.filter(name__icontains=query).values("name")[:10]

    return Response(results)

'''
@api_view(['POST'])
def save_prescription(request):
    try:
        data = request.data
        patient_id = data.get('patient_id')
        medicines = data.get('medicines', [])

        patient = Patient_Data.objects.get(pid=patient_id)

        #  Count existing prescriptions for this patient
        previous_count = Prescription.objects.filter(patient__pid=patient_id).values('prescription_round').distinct().count()
        current_round = previous_count + 1  # Next visit number

        #  Save all medicines with the same round number
        for med in medicines:
            Prescription.objects.create(
                patient=patient,
                medicine_name=med['medName'],
                dose=med['dose'],
                frequency=med['freq'],
                time=med['time'],
                remarks=med.get('remarks', ''),
                prescription_round=current_round
            )

        #  Update patient status if needed
        patient.status = 'Done'
        patient.save()

        return Response({'message': f'Prescription Round {current_round} saved.'}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from django.http import FileResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
import os

def generate_prescription(request):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    margin = 2 * cm
    line_height = 0.6 * cm
    y = height - margin

    # ✅ Load local images from static
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logo_path = os.path.join(base_dir, "static", "images", "hospital_logo.png")
    sign_path = os.path.join(base_dir, "static", "images", "doctor_sign.png")

    logo_data = ImageReader(logo_path)
    sign_data = ImageReader(sign_path)

    # 🏥 Header
    c.drawImage(logo_data, margin, y - 3*cm, width=3*cm, height=3*cm, mask='auto')
    c.setFont("Helvetica-Bold", 20)
    c.drawString(6*cm, y - 1*cm, "CityCare Multi-specialty Hospital")
    c.setFont("Helvetica", 10)
    c.drawString(6*cm, y - 1.7*cm, "Reg No: MH-12345678 | ISO 9001:2015 Certified")
    c.drawString(6*cm, y - 2.3*cm, "Contact: +91 9876543210 | www.citycarehospital.in")
    c.drawString(6*cm, y - 2.9*cm, "Address: 123 Wellness Ave, Mumbai, MH - 400001")

    y -= 4.2*cm
    c.setLineWidth(1)
    c.line(margin, y, width - margin, y)
    y -= line_height

    # 🧑‍⚕️ Patient Info
    patient = {
        "Name": "John Doe", "Age": "32", "Gender": "Male",
        "Date": "2025-07-09", "Patient ID": "CCH123456",
        "Blood Group": "B+", "Allergies": "None", "Consultant": "Dr. Priya Sharma"
    }

    c.setFont("Helvetica-Bold", 12)
    for key, val in patient.items():
        c.drawString(margin, y, f"{key}:")
        c.setFont("Helvetica", 12)
        c.drawString(margin + 4*cm, y, val)
        y -= line_height
        c.setFont("Helvetica-Bold", 12)

    y -= 0.3*cm
    c.line(margin, y, width - margin, y)
    y -= line_height

    # 📝 Diagnosis
    c.setFont("Helvetica-Bold", 13)
    c.drawString(margin, y, "Symptoms:")
    c.setFont("Helvetica", 12)
    c.drawString(margin + 4*cm, y, "Fever, sore throat, body ache")
    y -= line_height

    c.setFont("Helvetica-Bold", 13)
    c.drawString(margin, y, "Diagnosis:")
    c.setFont("Helvetica", 12)
    c.drawString(margin + 4*cm, y, "Viral Infection")
    y -= line_height * 1.5

    # 💊 Medicines Table
    c.setFont("Helvetica-Bold", 13)
    c.drawString(margin, y, "Medicine")
    c.drawString(margin + 6*cm, y, "Dosage")
    c.drawString(margin + 12*cm, y, "Frequency")
    y -= 0.3*cm
    c.line(margin, y, width - margin, y)
    y -= line_height

    prescriptions = [
        ("Paracetamol", "500mg", "2x a day"),
        ("Amoxicillin", "250mg", "3x a day"),
        ("Vitamin C", "1000mg", "Once daily"),
        ("Cough Syrup", "10ml", "3x a day"),
        ("ORS Sachet", "1 pkt", "Post loose motion"),
    ]
    c.setFont("Helvetica", 12)
    for med, dose, freq in prescriptions:
        c.drawString(margin, y, med)
        c.drawString(margin + 6*cm, y, dose)
        c.drawString(margin + 12*cm, y, freq)
        y -= line_height
        if y < 3*cm:
            c.showPage()
            y = height - margin

    # 🗣️ Advice
    y -= line_height
    c.setFont("Helvetica-Bold", 13)
    c.drawString(margin, y, "Advice:")
    y -= line_height
    c.setFont("Helvetica", 12)
    advices = [
        "• Take adequate rest and stay hydrated.",
        "• Avoid spicy/cold food and junk.",
        "• Complete the medicine course.",
        "• Consult if symptoms worsen after 3 days."
    ]
    for advice in advices:
        c.drawString(margin + 0.5*cm, y, advice)
        y -= line_height

    # 🖊️ Signature
    y -= 2*cm
    c.drawImage(sign_data, x=width - 6*cm, y=y, width=4*cm, height=1.5*cm, mask='auto')
    c.setFont("Helvetica", 11)
    c.drawString(width - 6*cm, y - 0.5*cm, "Dr. Priya Sharma")
    c.drawString(width - 6*cm, y - 1*cm, "MBBS, MD (General Medicine)")
    c.drawString(width - 6*cm, y - 1.5*cm, "Reg No: MH20205678")

    # 📎 Footer
    c.setFont("Helvetica-Oblique", 9)
    c.setFillGray(0.5)
    c.drawCentredString(width / 2, 1.5*cm, "This is a computer-generated prescription. No signature required if digitally validated.")

    # Finish
    c.save()
    buffer.seek(0)

    return FileResponse(buffer, content_type="application/pdf")
'''

################ SAVE PRISCRIPTION ######################
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
import os

from .models import Patient_Data, Prescription

@api_view(['POST'])
def save_and_generate_prescription(request):
    try:
        print("Request received:", request.data)

        data = request.data
        patient_id = data.get('patient_id')
        medicines = data.get('medicines', [])

        if not patient_id or not medicines:
            return Response({'error': 'patient_id and medicines are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            patient = Patient_Data.objects.get(pid=patient_id)
        except Patient_Data.DoesNotExist:
            return Response({'error': 'Patient not found.'}, status=status.HTTP_404_NOT_FOUND)

        previous_count = Prescription.objects.filter(patient__pid=patient_id).values('prescription_round').distinct().count()
        current_round = previous_count + 1

        prescriptions = []
        for med in medicines:
            presc = Prescription.objects.create(
                patient=patient,
                medicine_name=med['medName'],
                dose=med['dose'],
                frequency=med['freq'],
                time=med['time'],
                remarks=med.get('remarks', ''),
                prescription_round=current_round
            )
            prescriptions.append(presc)

        patient.status = 'Done'
        patient.save()

        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        margin = 2 * cm
        line_height = 0.6 * cm
        y = height - margin

        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            logo_path = os.path.join(base_dir, "static", "images", "hospital_logo.png")
            sign_path = os.path.join(base_dir, "static", "images", "doctor_sign.png")
            logo_data = ImageReader(logo_path)
            sign_data = ImageReader(sign_path)
        except Exception as file_error:
            print(f"Static file load error: {file_error}")
            return Response({'error': 'Missing logo or sign image.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        c.drawImage(logo_data, margin, y - 3 * cm, width=3 * cm, height=3 * cm, mask='auto')
        c.setFont("Helvetica-Bold", 20)
        c.drawString(6 * cm, y - 1 * cm, "CityCare Multi-specialty Hospital")

        y -= 4.2 * cm
        c.setLineWidth(1)
        c.line(margin, y, width - margin, y)
        y -= line_height

        c.setFont("Helvetica-Bold", 12)
        patient_info = {
            "Name": patient.name,
            "Age": patient.age,
            "Gender": patient.gender,
            "Date": str(prescriptions[0].date.date()) if prescriptions else "",
            "Patient ID": patient.pid,
            "Consultant": getattr(patient, 'doctor_name', "Dr. Priya Sharma")
        }

        for key, val in patient_info.items():
            c.drawString(margin, y, f"{key}:")
            c.setFont("Helvetica", 12)
            c.drawString(margin + 4 * cm, y, str(val))
            y -= line_height
            c.setFont("Helvetica-Bold", 12)

        y -= 0.3 * cm
        c.line(margin, y, width - margin, y)
        y -= line_height

        c.setFont("Helvetica-Bold", 13)
        c.drawString(margin, y, "Symptoms:")
        c.setFont("Helvetica", 12)
        c.drawString(margin + 4 * cm, y, getattr(patient, 'symptoms', "N/A"))
        y -= line_height

        c.setFont("Helvetica-Bold", 13)
        c.drawString(margin, y, "Diagnosis:")
        c.setFont("Helvetica", 12)
        c.drawString(margin + 4 * cm, y, prescriptions[0].remarks if prescriptions else "N/A")
        y -= line_height * 1.5

        c.setFont("Helvetica-Bold", 13)
        c.drawString(margin, y, "Medicine")
        c.drawString(margin + 6 * cm, y, "Dosage")
        c.drawString(margin + 12 * cm, y, "Frequency")
        y -= 0.3 * cm
        c.line(margin, y, width - margin, y)
        y -= line_height

        c.setFont("Helvetica", 12)
        for pres in prescriptions:
            c.drawString(margin, y, pres.medicine_name)
            c.drawString(margin + 6 * cm, y, pres.dose)
            c.drawString(margin + 12 * cm, y, pres.frequency)
            y -= line_height
            if y < 3 * cm:
                c.showPage()
                y = height - margin

        y -= line_height
        c.setFont("Helvetica-Bold", 13)
        c.drawString(margin, y, "Advice:")
        y -= line_height
        c.setFont("Helvetica", 12)
        advices = [
            "• Take adequate rest and stay hydrated.",
            "• Avoid spicy/cold food and junk.",
            "• Complete the medicine course.",
            "• Consult if symptoms worsen after 3 days."
        ]
        for advice in advices:
            c.drawString(margin + 0.5 * cm, y, advice)
            y -= line_height

        y -= 2 * cm
        c.drawImage(sign_data, x=width - 6 * cm, y=y, width=4 * cm, height=1.5 * cm, mask='auto')
        c.setFont("Helvetica", 11)
        c.drawString(width - 6 * cm, y - 0.5 * cm, "Dr. Priya Sharma")
        c.drawString(width - 6 * cm, y - 1 * cm, "MBBS, MD (General Medicine)")
        c.drawString(width - 6 * cm, y - 1.5 * cm, "Reg No: MH20205678")

        c.setFont("Helvetica-Oblique", 9)
        c.setFillGray(0.5)
        c.drawCentredString(width / 2, 1.5 * cm, "This is a computer-generated prescription. No signature required if digitally validated.")
        c.save()

        buffer.seek(0)
        return FileResponse(buffer, content_type="application/pdf")

    except Exception as e:
        print("Unexpected error occurred:", e)
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
