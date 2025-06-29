from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from .models import UserProfile

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            profile = UserProfile.objects.get(user=user)
            if profile.user_type == 'doctor':
                return redirect('doctor_dashboard')
            else:
                return redirect('patient_dashboard')
        else:
            error = "Invalid credentials"
    return render(request, 'login.html', {'error': error})

@login_required
def doctor_dashboard(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'doctor_dashboard.html', {'profile': profile})

@login_required
def patient_dashboard(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'patient_dashboard.html', {'profile': profile})
