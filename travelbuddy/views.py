from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from travelbuddy.models import *
from datetime import date, datetime
import re

def main(request):
    if 'profile' in request.session and request.session['profile']:
        return redirect('/travels/')
    return render(request, "main.html")

def travels(request):
    if not request.user.is_authenticated:
        return redirect("/")
    context = {}
    profile = Profile.objects.get(user=request.user)
    authored_plans = TravelPlan.objects.filter(author=profile)
    joined_plans = profile.travel_plans.all()
    context['your_plans'] = []
    for plan in authored_plans:
        context['your_plans'].append(plan)
    for plan in joined_plans:
        context['your_plans'].append(plan)
    context['all_travel_plans'] = TravelPlan.objects.exclude(author=profile).exclude(id__in=[o.id for o in joined_plans])
    return render(request, "travels.html", context)

def destination(request, number):
    if not request.user.is_authenticated:
        return redirect("/")
    context = {}
    plan = TravelPlan.objects.get(id=number)
    passengersX = plan.passengers.all()
    passengers = []
    for passenger in passengersX:
        passengers.append(passenger.user.first_name)
    print passengers
    context['destination'] = {
        'name': plan.name,
        'author': plan.author.user.first_name,
        'description': plan.description,
        'from_date': plan.from_date,
        'to_date': plan.to_date,
        'passengers': passengers
    }
    return render(request, "destination.html", context)

def join(request, number):
    if not request.user.is_authenticated:
        return redirect("/")
    profile = Profile.objects.get(user=request.user)
    profile.travel_plans.add(TravelPlan.objects.get(id=number))
    return redirect("/travels/")

def add(request):
    if not request.user.is_authenticated:
        return redirect("/")
    return render(request, "add.html")

def processadd(request):
    if not request.user.is_authenticated:
        return redirect("/")
    valid = True
    if len(request.POST['name']) < 1:
        messages.add_message(request, messages.INFO, "*Destination name cannot be blank")
        valid = False
    if len(request.POST['description']) < 1:
        messages.add_message(request, messages.INFO, "*Description cannot be blank")
        valid = False
    try:
        fromdate = datetime.strptime(request.POST['from_date'], '%Y-%m-%d').date()
        todate = datetime.strptime(request.POST['to_date'], '%Y-%m-%d').date()
        if fromdate < date.today():
            messages.add_message(request, messages.INFO, "*Start date must be in the future")
            valid = False
        if todate < fromdate:
            messages.add_message(request, messages.INFO, "*End date must take place after Start date")
            valid = False
    except ValueError:
        messages.add_message(request, messages.INFO, "*Date fields must be filled out")
        valid = False
    if valid:
        profile = Profile.objects.get(user=request.user)
        plan = TravelPlan(name=request.POST['name'], author=profile, description=request.POST['description'], from_date=fromdate, to_date=todate)
        plan.save()
        return redirect("/travels/")
    return redirect("/travels/add/")

def processlogin(request):
    if request.user.is_authenticated:
        return redirect("/travels/")
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect("/travels/")
    messages.add_message(request, messages.INFO, "*Username and password do not match")
    return redirect("/main/")

def processlogout(request):
    logout(request)
    return redirect("/")

def register(request):
    PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d$@$!%*?&]{8,}')
    valid = True
    if len(request.POST['name']) < 3:
        messages.add_message(request, messages.INFO, "*Name must be at least 3 characters long.")
        valid = False
    if len(request.POST['username']) < 3:
        messages.add_message(request, messages.INFO, "*Username must be at least 3 characters long.")
        valid = False
    if not PASSWORD_REGEX.match(request.POST['password']):
        messages.add_message(request, messages.INFO, "*Password must contain at least 1 capital letter and at least 1 number, and be at least 8 characters long.")
    if request.POST['password'] != request.POST['confirm_password']:
        messages.add_message(request, messages.INFO, "*Password inputs must match.")
        valid = False
    try:
        u = User.objects.get(username=request.POST['username'])
        messages.add_message(request, messages.INFO, "*That username is already taken")
        valid = False
    except:
        pass       
    if valid:
        u = User.objects.create_user(request.POST['username'], "a@a.a", request.POST['password'])
        u.first_name = request.POST['name']
        u.save()
        profile = Profile(user=u)
        profile.save()
        login(request, u)
        return redirect("/travels/")
    else:
        return redirect("/main/")
