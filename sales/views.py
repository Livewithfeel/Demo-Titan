from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User

# Login View (Person 1)
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')

    return render(request, 'login.html')


# Forgot Password View (Person 2)
def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            request.session['reset_username'] = user.username  # Store username in session
            messages.success(request, 'Reset link simulated. Now reset your password.')
            return redirect('reset_password')
        except User.DoesNotExist:
            messages.error(request, 'Email not found.')
            return redirect('forgot_password')

    return render(request, 'forgot_password.html')


# Reset Password View (Person 3)
def reset_password_view(request):
    username = request.session.get('reset_username')

    if not username:
        messages.error(request, 'No reset request found. Please start again.')
        return redirect('forgot_password')

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('reset_password')

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()

            # Clear session after reset
            del request.session['reset_username']

            messages.success(request, 'Password reset successful! You can now log in.')
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('reset_password')

    return render(request, 'reset_password.html')
