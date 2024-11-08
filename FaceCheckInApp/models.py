# import os

from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    ENROLLMENT_STATUS_CHOICES = (
        ('enrolled', 'Enrolled'),
        ('not_enrolled', 'Not Enrolled'),
    )

    status = models.CharField(
        max_length=20, choices=ENROLLMENT_STATUS_CHOICES, default='not_enrolled')

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Specify a unique related_name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',  # Specify a unique related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username


# Create enrollment model
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/enrollments/<username>/<filename>
    return f'enrollments/{instance.user.username}/{filename}'


class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    photo1 = models.ImageField(upload_to=user_directory_path)
    photo2 = models.ImageField(upload_to=user_directory_path)
    photo3 = models.ImageField(upload_to=user_directory_path)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Check if this is a new enrollment
            self.user.status = 'enrolled'
            self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Enrollment for {self.user.username}"


class ClockIn(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    clock_in_time = models.DateTimeField(default=timezone.now)
    date = models.DateField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f"{self.user.username} clocked in at {self.clock_in_time}"


class Subscription(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
