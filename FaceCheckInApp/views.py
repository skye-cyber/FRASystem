import base64
import json
import os
import shutil

import cv2
import face_recognition
import numpy as np
from django.conf import settings
# from pathlib import Path
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout  # get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.files.base import ContentFile
from django.db import IntegrityError
# from .middleware.rate_limit_middleware import RateLimitMiddleware as custom_ratelimit
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden, HttpResponseRedirect,
                         JsonResponse, StreamingHttpResponse)
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.http import urlencode
from django.views.decorators import gzip
from django.views.decorators.csrf import csrf_exempt
from django_ratelimit.decorators import ratelimit

from .DetectionAlgorithms import encoder
from .DetectionAlgorithms.recog0 import FaceMatch
from .forms import CustomRegistrationForm  # Make sure to import your form
from .forms import LoginForm
from .models import Subscription  # Assuming there's a Subscription model
from .models import ClockIn, CustomUser, Enrollment

# sudo apt-get install webkit2gtk-4.0 gtk+-3.0
# pip install pywebview
# reg_path = os.path.join(Path(__file__).resolve().parent, 'templates/registration')


def csrf_failure(request, reason=""):
    return JsonResponse({'error': 'CSRF token missing or incorrect', 'reason': reason}, status=403)


# Register View


def register(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)

        if form.is_valid():
            # Form data is valid, save the user
            user = form.save()  # Save the user

            # Log the user in
            login(request, user)  # Log the user in after registration
            return redirect('home')  # Redirect to a home page or desired view

        else:
            # If the form is not valid, it will automatically retain the data
            messages.error(
                request, f'Please correct the errors below.\n {form.errors}')
            return render(request, 'registration/signup.html', {'form': form})

    else:
        form = CustomRegistrationForm()

    return render(request, 'registration/signup.html', {'form': form})


# Ebrollment view
@login_required
def enroll(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        photos = data['photos']

        if Enrollment.objects.filter(user=request.user).exists():
            messages.info(request, 'You have already enrolled')
            print("You have already enrolled")
            return render(request, 'profile.html')
        if len(photos) >= 3:
            enrollment = Enrollment(user=request.user)
            valid_photos = []

            user_folder = os.path.join(
                settings.MEDIA_ROOT, 'enrollments', str(request.user.username))
            os.makedirs(user_folder, exist_ok=True)

            for i, photo in enumerate(photos):
                format, imgstr = photo.split(';base64,')
                ext = format.split('/')[-1]
                photo_data = base64.b64decode(imgstr)

                # Convert photo to a numpy array for face detection
                nparr = np.frombuffer(photo_data, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(rgb_frame)

                if face_locations:  # If faces are detected
                    valid_photos.append(ContentFile(
                        photo_data, name=f'photo_{i + 1}.{ext}'))

                else:
                    print('No face detected in photo {i + 1}')
                    messages.error(
                        request, F"No face detected in photo {i + 1}")
                    return JsonResponse({'status': 'error', 'message': f'No face detected in photo {i + 1}'}, status=400)

            if len(valid_photos) >= 3:
                enrollment.photo1 = valid_photos[0]
                enrollment.photo2 = valid_photos[1]
                enrollment.photo3 = valid_photos[2]
                enrollment.save()
                encoder.encode_faces(user_folder)
                return JsonResponse({'status': 'success'})
            else:
                messages.error(request, 'Not enough valid photos with faces')
                return JsonResponse({'status': 'error', 'message': 'Not enough valid photos with faces'}, status=400)
        else:
            messages.error(request, 'Not enough photos provided')
            return JsonResponse({'status': 'error', 'message': 'Not enough photos provided'}, status=400)

    messages.error(request, 'Invalid request method')
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


# unenroll the user
@login_required
def unenroll(request):
    # if request.method == 'POST':
    try:
        # Find the user's enrollment
        enrollments = Enrollment.objects.filter(user=request.user)
        # enrollments = Enrollment.objects.get(user=request.user)
        for enrollment in enrollments:
            # Remove photos from the filesystem
            user_folder = os.path.join(
                settings.MEDIA_ROOT, 'enrollments', str(request.user.username))
            if os.path.exists(user_folder):
                shutil.rmtree(user_folder)

            # Remove references to the photos in the database
            enrollment.photo1.delete(save=False)
            enrollment.photo2.delete(save=False)
            enrollment.photo3.delete(save=False)

            # Delete the enrollment record if necessary
            enrollment.delete()

            # logout the user after unenrolling
            logout(request)

        messages.success(request, "User unenrolled successfully")
        return HttpResponseRedirect(reverse('login'))

    except Enrollment.DoesNotExist:
        messages.error(request, 'User is not enrolled')
        return render(request, 'profile.html')
    # else:
    #  messages.error(request, 'Invalid request method')
    # return HttpResponse(request, 'Invalid request method', status=405)


# Delete user account
@login_required
def DeleteUserAccount(request):
    # if request.method == 'POST':
    try:
        # Find the user's enrollment
        # alternatively ```enrollments = Enrollment.objects.filter(user=user)```
        enrollments = Enrollment.objects.filter(user=request.user)

        for enrollment in enrollments:
            # Remove photos from the filesystem
            user_folder = os.path.join(
                settings.MEDIA_ROOT, 'enrollments', str(request.user.username))
            if os.path.exists(user_folder):
                shutil.rmtree(user_folder)

            # Remove references to the photos in the database
            enrollment.photo1.delete(save=False)
            enrollment.photo2.delete(save=False)
            enrollment.photo3.delete(save=False)

            # Delete the enrollment record
            enrollment.delete()

        # Get the user instance
        user = request.user

        # Log out the user
        logout(request)

        # Delete the user account
        user.delete()

        messages.success(
            request, "User unenrolled and account deleted successfully.")
        return HttpResponseRedirect(reverse('login'))
        # return JsonResponse({'status': 'success', 'message': 'User unenrolled and account deleted successfully'})
        # HttpResponseRedirect('getSignupPage')
    except Enrollment.DoesNotExist:
        messages.error(request, 'User is not enrolled.')
        return render(request, 'profile.html')
    else:
        messages.error(request, 'Invalid request method')
        return render(request, 'profile.html')


# clock_in view
@login_required
def clock_in(request):
    return render(request, 'clock_in.html')


@login_required
def index(request):
    return render(request, 'index.html')


@login_required
def GetProfilePage(request):
    # Fetch clock-in records for the logged-in user
    attendance_records = ClockIn.objects.filter(
        user=request.user).order_by('-clock_in_time')

    # Fetch enrollment data for the logged-in user
    enrollment_records = Enrollment.objects.filter(
        user=request.user).order_by('-enrolled_at')

    # Prepare data for rendering in the template
    clock_in_data = [{'name': record.user.get_full_name(), 'clock_in_time': record.clock_in_time}
                     for record in attendance_records]

    # Include photo1 in the enrollment_data (add checks if needed)
    enrollment_data = [{
        'name': record.user.get_full_name(),
        'enrolled_at': record.enrolled_at,
        'photo1_url': record.photo1.url if record.photo1 else None,
        'photo2_url': record.photo2.url if record.photo2 else None,
        'photo3_url': record.photo3.url if record.photo3 else None  # Add the URL for photo1
    } for record in enrollment_records]

    context = {
        'clock_in_data': clock_in_data,
        'enrollment_data': enrollment_data,
    }

    return render(request, 'profile.html', context)


def getLoginPage(request):
    form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def SignupPage(request):
    form = CustomRegistrationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def subscribe(request):
    user = request.user
    name = user.get_full_name()  # Assuming the user model has a method to get full name
    email = user.email  # Fetch the user's email

    # Check if the user is already subscribed
    if Subscription.objects.filter(user=user).exists():
        messages.info(request, 'You are already subscribed!')
        return redirect('home')  # Or any page you want to redirect to

    # Create a new subscription
    new_subscription = Subscription.objects.create(
        user=user, name=name, email=email)
    new_subscription.save()

    messages.success(request, 'Subscription successful!')
    return redirect('subscribed')  # Redirect to a success page


@csrf_exempt
@login_required
def get_enrollment_page(request):
    return render(request, 'registration/enroll.html')


# login view
@ratelimit(key='ip', rate='5/m', method='ALL', block=True)
def user_login(request):
    if getattr(request, 'limited', False):
        return render('ratelimit.html')
    if request.method == "POST":
        # Instantiate the form with submitted data
        form = AuthenticationForm(request, data=request.POST)
        # form = LoginForm(request.POST)
        # Check wether the form is valid
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd['username'], password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    # messages.success(request, f'Welcome, {cd["username"]}. You are now logged in.')
                    return redirect('home')

                else:
                    messages.error(request, 'Account is disabled❌')
                    # HttpResponse('<script>alert("Account is disabled❌")</script>')

            else:
                messages.error(request, 'Incorrect login credentials')
                print('Incorrect username or password.')
                form = LoginForm()
                return render(request, 'registration/login.html', {'form': form})

        else:
            messages.error(request, 'Invalid username or password.')
            form = LoginForm()
            print('Invalid username or password.')
            return render(request, 'registration/login.html', {'form': form})

    # When the user_login view is submitted via GET request a new login form is Instantiated with for = LoginForm() to display it in the template.
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


# Logout the user
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


@gzip.gzip_page
def client_stream_video(request):
    return StreamingHttpResponse(FaceMatch().match_faces(), content_type='multipart/x-mixed-replace; boundary=frame')


@csrf_exempt
def process_frames(request):
    if request.method == 'POST':
        try:
            frame = None
            # Receive frame data from POST request
            data = json.loads(request.body)
            frame_data = data.get('photo', '')

            if not frame_data:
                return JsonResponse({'status': 'error', 'message': 'No frame data received'})

            # Validate the base64 data
            if ',' in frame_data:
                frame_bytes = frame_data.split(',')[1].encode()
            else:
                frame_bytes = frame_data.encode()

            try:
                nparr = np.frombuffer(base64.b64decode(frame_bytes), np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            except Exception:
                return JsonResponse({'status': 'error', 'message': "Decoding error"})

            if frame is None:
                raise ValueError("Decoded frame is None")

            # Initialize FaceMatch instance
            init = FaceMatch()

            # Process frame for facial recognition
            processed_frame, recognized, username, face_data = init.match_faces(
                frame)

            if processed_frame is None:
                return JsonResponse({'status': 'error', 'message': 'No match found'})

            response_data = {
                'status': 'failure',
                'processed_frame': '',
                'employee': None,
                'face_data': face_data  # Include face data for drawing boxes
            }

            if recognized:
                # Retrieve the user based on the recognized username
                try:
                    user = CustomUser.objects.get(username=username)
                except CustomUser.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'User not found'})

                # Check if a ClockIn entry already exists for today
                today = timezone.now().date()
                existing_clock_in = ClockIn.objects.filter(
                    user=user, date=today).first()

                if existing_clock_in:
                    return JsonResponse({'status': 'error', 'message': 'You have already clocked in today'})

                # Record the clock-in time
                ClockIn.objects.create(
                    user=user, clock_in_time=timezone.now(), date=timezone.now().date())

                # Encode processed frame to base64 JPEG
                _, encoded_image = cv2.imencode('.jpg', processed_frame)
                encoded_image_data = base64.b64encode(
                    encoded_image).decode('utf-8')

                response_data = {
                    'status': 'success',
                    'processed_frame': encoded_image_data,
                    'employee': user.get_full_name(),
                    'face_data': face_data
                }

            return JsonResponse(response_data)

        except Exception as e:
            print(e)
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    else:
        return HttpResponseBadRequest('Invalid request method')
