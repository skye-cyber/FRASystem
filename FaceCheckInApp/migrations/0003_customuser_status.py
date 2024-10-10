# Generated by Django 4.2.13 on 2024-07-13 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FaceCheckInApp', '0002_clockin_customuser_enrollment_delete_attendance_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='status',
            field=models.CharField(choices=[('enrolled', 'Enrolled'), ('not_enrolled', 'Not Enrolled')], default='not_enrolled', max_length=20),
        ),
    ]