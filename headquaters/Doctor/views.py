from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from .models import Doctor, Patient , Appointment , Prescription,User
from .forms import doctor , Creation_user,slot_book,generator
import google.generativeai as genai
from django.http import HttpResponse
import markdown
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login 

def landing(request):
    # sab_doctor = Doctor.objects.all()
    
    return render(request, 'landing.html')

def home(request):
    sab_doctor = Doctor.objects.all()
    booked_doctor = []

    if hasattr(request.user , "patient"):
        booked_doctor = Appointment.objects.filter(patient = request.user.patient).values_list("doctor_id" , flat=True)
    
    return render(request , 'base.html', {"sab_doctor" : sab_doctor , "booked_doctor" : booked_doctor})

def doctors(request):

    all_list = Doctor.objects.all()

    return render(request , 'doctor-list.html' , {'all_list' : all_list})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)   # use Django's built-in login
            return redirect("home")
        else:
            return render(request, "login.html", {"error": "Invalid username or password"})
    
    return render(request, "login.html")


def profile(request):

    user =  request.user
    doctor = Doctor.objects.filter(user=user).first()
    pateint = Patient.objects.filter(user=user).first()


    return render(request , 'profile.html' , {'doctor':doctor , 'patient' : pateint , 'user':user})


def register(request):
    if request.method == "POST":
        form = Creation_user(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    
        else:
            return render(request , 'register.html' , {'form': form , 'error':'something went wrong'})
           
    
    else:
        form = Creation_user() # empty
        return render(request , 'register.html' , {'form':form})
    

def logout_view(request):
    if request.method == "POST":
        user = request.user
        authenticate(user)
        return redirect('landing')
    
    else:
       return redirect('landing')
        

def appointment(request , id):
    doctor  = get_object_or_404(Doctor, id = id)
    if request.method == "POST":
        form = slot_book(request.POST)  # use "form" instead of letter for clarity
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user.patient
            appointment.doctor = doctor
            appointment.save()

            return redirect('thanks')
        else:
            return render(request, 'appointment.html', {'form': form})
    else:
        form = slot_book()
        return render(request, 'appointment.html', {'form': form})


def thanks(request):
    return render(request , 'thanks.html')

def landing(request):
    return render(request , 'landing.html')


def bookings(request):
    book_patient = None
    book_doctor = None

    # If the user is a patient
    if hasattr(request.user, 'patient'):
        book_patient = Appointment.objects.filter(patient=request.user.patient)

    # If the user is a doctor
    if hasattr(request.user, 'doctor'):
        book_doctor = Appointment.objects.filter(doctor=request.user.doctor)

    return render(
        request,
        'bookings.html',
        {'book_patient': book_patient, 'book_doctor': book_doctor}
    )
        

def generator_ai(request):
    ai_output = None
    if request.method == "POST":
        form = generator(request.POST)
        if form.is_valid():
            user_text = form.cleaned_data['textbox']

        genai.configure(api_key=settings.GOOGLE_API_KEY)

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            f"you are a AI assistant instead of generating prescription , create sample prescription template for educational or demo purposr only {user_text}"
        )
        ai_output_raw = response.text

        ai_output = markdown.markdown(ai_output_raw)

        #  markdown is the package for the better output
        
    
    else:
      form = generator()

    return render(request, "parchi.html", {"form": form , "ai_output": ai_output })
    

 
def edit_slots(request,id):
        slots = get_object_or_404(Doctor,id=id)
    # get object ma Model levanu and niche badhe form levanu 
        if slots.user != request.user:
            return HttpResponse("you are not allowed to edit",status = 403)
        
        if request.method =="POST":
            editing = doctor(request.POST , instance = slots)
            if editing.is_valid():
                editing.save()
                return redirect('home')
            
        else:
            editing  = doctor(instance=slots)

        return render(request , "edit.html" , {"editing":editing})
