from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

def home(request):
    return render(request, 'home.html')
def about(request):
    return render(request, 'about.html')
def doctors_diary(request):
    return render(request, 'dashboards/doctors_diary.html')

def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])

        if user.role == 'doctor':
            user.is_approved = False
        else:
            user.is_approved = True

        user.save()
        return redirect('login')
    return render(request, 'register.html', {'form': form})


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user:
            login(request, user)

            if user.role == 'admin':
                return redirect('admin_dashboard')
                message = "Welcome Admin"
            elif user.role == 'doctor' and user.is_approved:
                return redirect('doctor_dashboard')
                message = "Welcome Doctor"
            else:
                return redirect('patient_dashboard')
                message = "Welcome Patient"

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')
@login_required
def doctor_dashboard(request):
    if request.user.role != 'doctor' or not request.user.is_approved:
        return HttpResponseForbidden("Not allowed")
    return render(request, 'dashboards/doctor.html')



@login_required
def patient_dashboard(request):
    doctor = User.objects.filter(role="doctor", is_approved=True).first()

    return render(request, "dashboards/patient.html", {
        "doctor": doctor
    })


from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

User = get_user_model()

@staff_member_required
def admin_dashboard(request):
    pending_doctors = User.objects.filter(role='doctor', is_approved=False)
    approved_doctors = User.objects.filter(role='doctor', is_approved=True)

    return render(request, 'dashboards/admin.html', {
        'pending_doctors': pending_doctors,
        'approved_doctors': approved_doctors
    })


@staff_member_required
def approve_doctor(request, user_id):
    doctor = User.objects.get(id=user_id, role='doctor')
    doctor.is_approved = True
    doctor.save()
    return redirect('admin_dashboard')
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage

def contact_page(request):
    if request.method == "POST":
        ContactMessage.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            message=request.POST.get("message"),
        )
        messages.success(request, "Your message has been sent successfully!")
        return redirect("contact")

    return render(request, "contact.html")
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_messages(request):
    messages_list = ContactMessage.objects.order_by("-created_at")
    return render(request, "dashboards/admin_messages.html", {
        "messages": messages_list
    })
from django.contrib.auth.decorators import login_required
from .models import ContactMessage, User

@login_required
def admin_dashboard(request):
    pending_doctors = User.objects.filter(role='doctor', is_approved=False)
    approved_doctors = User.objects.filter(role='doctor', is_approved=True)

    contact_messages = ContactMessage.objects.order_by('-created_at')

    context = {
        'pending_doctors': pending_doctors,
        'approved_doctors': approved_doctors,
        'contact_messages': contact_messages,
    }
    return render(request, 'dashboards/admin.html', context)
