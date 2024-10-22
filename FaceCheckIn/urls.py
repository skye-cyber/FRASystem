"""
URL configuration for FaceCheckIn project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from FaceCheckInApp import views
from django.conf.urls.static import static
from django.conf import settings
from FaceCheckInApp.DetectionAlgorithms.Host_recognizer import FaceMatch

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),

    # get login page
    path('getLoginPage/', views.getLoginPage, name='getLoginPage'),

    # set the login page as the first page
    path('', views.user_login, name='login'),

    # logout user
    path('logout', views.user_logout, name='logout'),

    # permanently delete user account
    path('deleteAccount', views.DeleteUserAccount, name='deleteAccount'),

    # get signup page
    path('getSignupPage/', views.SignupPage, name='getSignupPage'),

    # handle user signup
    path('signup/', views.register, name='signup'),

    # get user profile page
    path('profile/', views.GetProfilePage, name='profile'),

    # handle profile data display
    path('home/', views.index, name='home'),

    # clock_in the user
    path('clock_in/', views.clock_in, name='clock_in'),

    # get user enrollment page
    path('EnrollPage/', views.get_enrollment_page, name='getEnrollPage'),

    # enroll the user
    path('enroll/', views.enroll, name='enroll'),
    path('host_stream/', FaceMatch.match_faces, name='host_stream'),

    # unenroll the user
    path('unenroll/', views.unenroll, name='unenroll'),

    # process face frames from the camera face data
    path('process_frames/', views.process_frames, name='process_frames'),
] + static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)


# Serving static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
