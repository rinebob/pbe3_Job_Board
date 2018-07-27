from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
# from django.contrib.messages import get_messages
from .models import *
import bcrypt

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def index(request):
    # context = {

    # }
    return render(request,'belt2_py/index.html')
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def register(request):

    if request.method == "POST":
        errors = User.objects.reg_validator(request.POST)
        print("errors = ",errors)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')

        else:
            password_hash = bcrypt.hashpw(request.POST['password'].encode('utf-8'), bcrypt.gensalt())
            print("password hash = ",password_hash)
            User.objects.create(first_name=request.POST['first_name'],last_name = request.POST['last_name'],email = request.POST['email'],password_hash = password_hash.decode('utf-8'))
            x = User.objects.get(email=request.POST['email'])
            request.session['id'] = x.id
            request.session['first_name'] = x.first_name
            request.session['last_name'] = x.last_name
            print("query set = ",User.objects.all().values())
            print("THE END")
            return redirect('/welcome')
            
    else:
        print("This was supposed to be a post but you're in the else statement...  why???")
        return redirect('/')
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def login(request):
   
    if request.method == "POST":
        login_errors = User.objects.login_validator(request.POST)
        print("login_errors = ",login_errors)
        if len(login_errors):
            for key, value in login_errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')

        else:
            print("THE END")

            x = User.objects.get(email=request.POST['log_eml'])
            request.session['id'] = x.id
            request.session['first_name'] = x.first_name
            request.session['last_name'] = x.last_name
            print("r.s id = ",request.session['id'])
            print("r.s fn = ",request.session['first_name'])

            return redirect('/welcome')
    
    else:

        print("This was supposed to be a post but you're in the else statement...  why???")
        return redirect('/')
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def welcome(request):
    context = {
        "trips" : Trip.objects.filter(travelers=User.objects.get(id=request.session['id'])),
        "otherstrips" : Trip.objects.all().exclude(travelers=request.session['id'])
    }


    # return render(request,'belt2_py/welcome.html')
    return render(request,'belt2_py/welcome.html',context)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def viewtrip(request,trip_id):
    context = {
        "trip" : Trip.objects.get(id=trip_id),
        "othersjoining" : User.objects.filter(id=Trip.traveler_id.traveler)
    }
    
    
    return render(request,"belt2_py/viewtrip.html",context)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def canceltrip(request):
    if request.method == "POST":
        x = User.objects.get(id=request.session['id'])
        y = Trip.objects.get(id=request.POST['canceltrip'])
        print(" remove x = ",x.first_name)
        y.travelers.remove(x)
        return redirect('/welcome')
    else:
        print("This was supposed to be a post but you're in the else statement...  why???")
        return redirect('/welcome')

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def deletetrip(request):
    if request.method == "POST":
        x = User.objects.get(id=request.session['id'])
        y = Trip.objects.get(id=request.POST['canceltrip'])
        print(" remove trip = ",y.name)
        Trip.objects.remove(id=request.POST['canceltrip'])
        return redirect('/welcome')
    else:
        print("This was supposed to be a post but you're in the else statement...  why???")
        return redirect('/welcome')

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def jointrip(request):

    if request.method == "POST":
        x = User.objects.get(id=request.session['id'])
        y = Trip.objects.get(id=request.POST['jointrip'])
        print("x = ",x.first_name)
        y.travelers.add(x)
        return redirect('/welcome')
    else:
        print("This was supposed to be a post but you're in the else statement...  why???")
        return redirect('/addtrip')

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    

def addtrip(request):
    
    return render(request,"belt2_py/addtrip.html")
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def createtrip(request):
    if request.method == "POST":
        date_errors = Trip.objects.date_validator(request.POST)
        print("date_errors = ",date_errors)
        print("len(date_errors) = ",len(date_errors))
        if len(date_errors):
            for key, value in date_errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/addtrip')
        else:

            x = Trip.objects.create(destination=request.POST['destination'], description=request.POST['description'], travel_from=request.POST['travel_from'], travel_to=request.POST['travel_to'],creator_id=request.session['id'])
            print("x = ",x)
            return redirect('/welcome')
    
    else:

        print("This was supposed to be a post but you're in the else statement...  why???")
        return redirect('/addtrip')
    

    
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++





def logout(request):

    request.session.clear()

    return redirect("/")


