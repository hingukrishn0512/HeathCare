from django import forms
from .models import Doctor,Appointment,Prescription
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class doctor(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['address','experience_years','consulting_fees','available_days','phone_number']

class Creation_user(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username' , 'email' , 'password1' , 'password2')  # fort he built in function we used tuple
        
class slot_book(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'date', 'time', 'reason']

class generator(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['textbox']

