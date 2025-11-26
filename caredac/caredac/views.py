# from django.http import HttpResponse

# # Simple home page view
# def home(request):
#     return HttpResponse("Welcome to Caredac API! Connected Successfully!!")

# def caregiver_login(request):
#     return HttpResponse("Caregiver Login Page")

# def patient_login(request):
#     return HttpResponse("Patient Login Page")

# def admin_login(request):
#     return HttpResponse("Admin Login Page")

# def otp_verification(request):
#     return HttpResponse("OTP Verification Page")

from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from django.utils import timezone
import random
from caredac_admin.models import EmailOTP


# ----------------------------
# FUNCTION TO GENERATE OTP
# ----------------------------
def generate_otp():
    return str(random.randint(1000, 9999))


# ----------------------------
# YOUR ORIGINAL SIMPLE VIEWS
# ----------------------------
def home(request):
    return HttpResponse("Welcome to Caredac API! Connected Successfully!!")

def caregiver_login(request):
    return HttpResponse("Caregiver Login Page")

def patient_login(request):
    return HttpResponse("Patient Login Page")

def admin_login(request):
    return HttpResponse("Admin Login Page")

@api_view(['POST'])
def otp_verification(request):
    email = request.data.get("email")
    otp_input = request.data.get("otp")  # Optional: only present when verifying

    if not email:
        return Response({"error": "Email is required"}, status=400)

    # ------------------------------------
    # CASE 1 → VERIFY OTP
    # ------------------------------------
    if otp_input:
        try:
            otp_record = EmailOTP.objects.get(email=email)
        except EmailOTP.DoesNotExist:
            return Response({"error": "OTP not found"}, status=400)

        # Check expiration
        if timezone.now() > otp_record.created_at + timezone.timedelta(minutes=5):
            otp_record.delete()
            return Response({"error": "OTP expired"}, status=400)

        # Check OTP match
        if otp_record.otp != otp_input:
            return Response({"error": "Invalid OTP"}, status=400)

        otp_record.delete()
        return Response({"message": "OTP verified successfully"})


    # ------------------------------------
    # CASE 2 → SEND OTP
    # ------------------------------------
    otp = generate_otp()

    EmailOTP.objects.update_or_create(
        email=email,
        defaults={"otp": otp, "created_at": timezone.now()}
    )

    send_mail(
        subject="Your OTP Code",
        message=f"Your OTP is {otp}. It expires in 5 minutes.",
        from_email=None,
        recipient_list=[email],
        fail_silently=False,
    )

    return Response({"message": "OTP sent successfully to " + email})
