from django.shortcuts import render, redirect
from mocenti.models import Signup, UserActivity  # Import correctly
from django.utils.timezone import now
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout as auth_logout

def index(request):
    return render(request, 'index.html')  # Or your desired template

def url(request):
    return render(request, 'url.html')

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Signup.objects.get(email=email)
            
            # Check if the provided password matches the stored hashed password
            if check_password(password, user.password):
                # Store login time
                UserActivity.objects.create(user=user, login_time=now())

                request.session['user_id'] = user.id  # Store user ID in session
                return redirect('url')  # Redirect to the URL input page after login
            else:
                messages.error(request, "Invalid email or password")
        except Signup.DoesNotExist:
            messages.error(request, "Invalid email or password")
    
    return render(request, 'login.html')

def logout(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = Signup.objects.get(id=user_id)
            
            # Update logout time for the latest login session
            latest_activity = UserActivity.objects.filter(user=user).latest('login_time')
            latest_activity.logout_time = now()
            latest_activity.save()

            # Use Django's auth_logout for better security
            auth_logout(request)

            # Clear session manually
            request.session.flush()

        except Signup.DoesNotExist:
            messages.error(request, "User session error.")
    
    return redirect('index')  # Redirect to homepage after logout

def signup_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        youtube = request.POST.get('youtube', "No YouTube Link")
        twitter = request.POST.get('twitter', "No Twitter Link")
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'signup.html')

        if Signup.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return render(request, 'signup.html')

        # Hash the password before saving
        hashed_password = make_password(password)
        signup_obj = Signup(name=name, email=email, youtube=youtube, twitter=twitter, password=hashed_password)

        try:
            signup_obj.save()
        except Exception as e:
            messages.error(request, f"Error saving user: {e}")

        return redirect('url')

    return render(request, 'signup.html')
