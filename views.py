from django.shortcuts import render
from .models import Service
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http.response import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import csv
from django.http import HttpResponse
from django.conf import settings
import os
from pathlib import Path


# Create your views here.
def index(request):
    services = Service.objects.all()

    context = {
        "services" : services
    }

    return render(request, 'website/index.html', context)


def services(request):
    services = Service.objects.all()

    context = {
        "services" : services
    }

    return render(request, 'website/services.html', context)

from vehicle.models import Car

def cars(request):
    cars_list = Car.objects.all()

    context = {
        'cars_list': cars_list
    }

    return render(request, 'website/cars.html', context)


def car_detail(request, car_id):
    
    try:
        car = Car.objects.get(id=car_id)
    except Car.DoesNotExist:        
        return render(request, '404.html')  # Render a 404 page or any other error handling
    
    
    return render(request, 'website/car_detail.html', {'car': car})

def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == "POST":
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            confirmPassword = request.POST.get('confirmPassword')
            phone = request.POST.get('phone')

            if username and email and password:
                if password == confirmPassword:
                    user = User.objects.create(
                        email=email,
                        username=username,
                        password=password,
                        phone=phone,
                    )
                    user.save()
                    save_to_csv([username, email, phone])
                    login(request, user)
                    return redirect('/success_page')
                else:
                    messages.error(request, "The two password fields didn't match.")
                    return HttpResponseRedirect('/signup')
            else:
                messages.error(request, "All fields are required.")
                return HttpResponseRedirect('/signup')
  
    return render(request, 'website/signup.html')

    
def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/success_page')
            else:
                messages.info(request, 'Username or password is incorrect.')
    return render(request, 'website/login.html')


def save_to_csv(data):
    base_dir = Path(__file__).resolve().parent.parent
    csv_file_path = base_dir / 'data' / 'user_data.csv'


    with open(csv_file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)