from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm
from .models import User
import logging

logger = logging.getLogger(__name__)

def login_view(request):
    """
    User login view - supports Active Directory authentication.
    Domain: KCBLTZ.CRDBBANKPLC.COM
    Users login with their sAMAccountName (e.g., JLugome, MMalopa)
    """
    if request.user.is_authenticated:
        if not getattr(request.user, 'profile_completed', True):
            return redirect('accounts:complete_profile')
        return redirect('courses:dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Try AD authentication first with entered username
            user = authenticate(request, username=username, password=password)
            
            # If AD fails with entered case, try with stored username case
            if user is None:
                try:
                    local_user = User.objects.get(username__iexact=username)
                    # Try AD with the stored username (correct case)
                    if local_user.username != username:
                        logger.info(f"Retrying AD auth with stored username: {local_user.username}")
                        user = authenticate(request, username=local_user.username, password=password)
                    
                    # If AD still fails, try local password authentication
                    if user is None:
                        # Try with email (since USERNAME_FIELD is 'email')
                        user = authenticate(request, username=local_user.email, password=password)
                        if user:
                            logger.info(f"Local password authentication for: {username}")
                except User.DoesNotExist:
                    pass
            
            if user is not None:
                login(request, user)
                logger.info(f"User logged in: {user.username} - {user.get_full_name()} (Role: {user.role})")
                messages.success(request, f'Welcome, {user.get_full_name() or user.username}!')

                if not getattr(user, 'profile_completed', True):
                    return redirect('accounts:complete_profile')
                
                # Redirect based on role
                if user.is_risk_admin():
                    return redirect('content:dashboard')
                return redirect('courses:dashboard')
            else:
                # Authentication failed
                messages.error(request, 'Invalid username or password. Please use your domain credentials.')
                logger.warning(f"Failed login attempt for: {username}")
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        if not getattr(request.user, 'profile_completed', True):
            return redirect('accounts:complete_profile')
        return redirect('courses:dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Risk LMS.')
            return redirect('accounts:complete_profile')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('accounts:login')

@login_required
def profile_view(request):
    """User profile view"""
    return render(request, 'accounts/profile.html', {'user': request.user})


@login_required
def complete_profile_view(request):
    """First-time login onboarding - capture department and designation."""
    if getattr(request.user, 'profile_completed', False):
        return redirect('courses:dashboard')

    if request.method == 'POST':
        department = (request.POST.get('department') or '').strip()
        designation = (request.POST.get('designation') or '').strip()

        if department and designation:
            request.user.department = department
            request.user.designation = designation
            request.user.profile_completed = True
            request.user.save(update_fields=['department', 'designation', 'profile_completed', 'updated_at'])
            messages.success(request, 'Welcome! Your profile has been completed.')
            return redirect('courses:dashboard')

        messages.error(request, 'Please select both department and designation.')

    context = {
        'designation_choices': User.DESIGNATION_CHOICES,
    }
    return render(request, 'accounts/complete_profile.html', context)
