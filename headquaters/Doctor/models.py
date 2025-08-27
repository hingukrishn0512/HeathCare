from django.db import models
from django.contrib.auth.models import User

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    address = models.TextField(max_length=200)
    phone_number = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    clinic_name = models.CharField(max_length=100)
    experience_years = models.PositiveIntegerField()
    available_days = models.CharField(max_length=100)
    consulting_fees = models.DecimalField(max_digits=6, decimal_places=2)
    bio = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Dr. {self.user.username} - {self.specialization}"


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    address = models.TextField(max_length=200)
    phone_number = models.CharField(max_length=15)
    blood_group = models.CharField(max_length=10, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ])  
    medical_history = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField(max_length=100)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ], default='pending')

    def __str__(self):
        return f"{self.patient.user.username} -> {self.doctor.user.username} on {self.date} at {self.time}" 


class Prescription(models.Model):
    # appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    textbox = models.TextField(max_length=100)
    # prescribed_medicines = models.TextField()
    # created_at = models.DateTimeField(auto_now_add=True)



    