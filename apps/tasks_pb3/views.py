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
    return render(request,'tasks_pb3/index.html')
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

def logout(request):
    request.session.clear()
    return redirect("/")

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def welcome(request):
    context = {
        "jobs" : Job.objects.all(),
        # "myjobs" : Job.objects.filter(worker=request.session['id'])
        # "myjobs" : Job.objects.filter(worker=User.objects.get(request.session['id'])
        "myjobs" : Job.objects.filter(creator=request.session['id'])
    }
    # print("myjobs = ",context['myjobs'])


    # return render(request,'tasks_pb3/welcome.html')
    return render(request,'tasks_pb3/welcome.html',context)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def display_addjob(request):
    
    return render(request,"tasks_pb3/addjob.html")
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def display_viewjob(request):
    context = {
        "job" : Job.objects.get(id=request.POST['display_viewjob']),
    }
    print("job = ",context['job'])
    # return render(request,"tasks_pb3/viewjob.html")
    return render(request,"tasks_pb3/viewjob.html",context)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def display_viewjob2(request):
    context = {
        "job" : Job.objects.get(id=request.POST['display_viewjob2']),
    }
    print("job = ",context['job'])
    # return render(request,"tasks_pb3/viewjob.html")
    return render(request,"tasks_pb3/viewjob.html",context)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def display_editjob(request):
    context = {
        "job" : Job.objects.get(id=request.POST['display_editjob']),
    }
    print("job = ",context['job'])
    
    
    # return render(request,"tasks_pb3/editjob.html")
    return render(request,"tasks_pb3/editjob.html",context)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def execute_createjob(request):
    if request.method == "POST":
        job_errors = Job.objects.job_validator(request.POST)
        print("job_errors = ",job_errors)
        print("len(job_errors) = ",len(job_errors))
        if len(job_errors):
            for key, value in job_errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/display_addjob')
        else:

            x = Job.objects.create(title=request.POST['job_title'], description=request.POST['job_description'], address=request.POST['job_address'], creator=User.objects.get(id=request.session['id']))

            print("x = ",x)

            # return redirect('/display_addjob')
            return redirect('/welcome')
    
    else:

        print("This was supposed to be a post but you're in the else statement...  why???")
        return redirect('/display_addjob')
    

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def execute_dojob(request):
    if request.method == "POST":
        x = User.objects.get(id=request.session['id'])
        y = Job.objects.get(id=request.POST['addtomyjobs'])
        print(" add x = ",x.first_name)
        print(" job = ",y.title)
        y.worker=x
        print("y.worker = x = ",y.worker)
        print("my worker jobs = ",Job.objects.filter(worker=User.objects.get(request.session['id'])))
        # Job.objects.get(id=request.POST['addtomyjobs']).add(x)
        return redirect('/welcome')
    else:
        print("This was supposed to be a post but you're in the else statement...  why???")
        return redirect('/welcome')

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def execute_updatejob(request):
    if request.method == "POST":
        job_errors = Job.objects.job_validator(request.POST)
        print("job_errors = ",job_errors)
        print("len(job_errors) = ",len(job_errors))
        if len(job_errors):
            for key, value in job_errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/display_addjob')
        else:

            x = Job.objects.get(id=request.POST['updatejob'])
            print("****************************")
            print("job = ",x)
            x.title = request.POST['job_title']
            x.description = request.POST['job_description']
            x.address = request.POST['job_address']
            x.save()

            # return redirect('/display_editjob')
            return redirect('/welcome')
    
    else:

        print("This was supposed to be a post but you're in the else statement...  why???")
        return redirect('/display_addjob')

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def execute_canceljob(request):
    if request.method == "POST":
        # job_errors = Job.objects.job_validator(request.POST)
        # print("job_errors = ",job_errors)
        # print("len(job_errors) = ",len(job_errors))
        # if len(job_errors):
        #     for key, value in job_errors.items():
        #         messages.error(request, value, extra_tags=key)
        #     return redirect('/display_addjob')
        # else:

        x = Job.objects.get(id=request.POST['canceljob'])
        print("--------------------------------")
        print("cancel job = ",x)
        Job.objects.get(id=request.POST['canceljob']).delete()

        # return redirect('/display_editjob')
        return redirect('/welcome')
    
    else:

        print("This was supposed to be a post but you're in the else statement...  why???")
        return redirect('/display_addjob')


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    


def execute_jobdone(request):
    if request.method == "POST":
        
        x = Job.objects.get(id=request.POST['jobdone'])
        print("--------------------------------")
        print("job done = ",x)
        Job.objects.get(id=request.POST['jobdone']).delete()

        # return redirect('/display_editjob')
        return redirect('/welcome')
    
    else:

        print("This was supposed to be a post but you're in the else statement...  why???")
        return redirect('/display_addjob')
    

    
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++








