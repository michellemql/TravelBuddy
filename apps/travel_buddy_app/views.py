from django.shortcuts import render,HttpResponse,redirect,reverse
from django.contrib import messages
from .models import User, Travel 
from django.core.urlresolvers import reverse

# Create your views here.

def flash_errors(request,errors,tag):
    for error in errors:
        messages.error(request, error, extra_tags = tag)

def index(request):
    return render(request,'travel_buddy_app/index.html')

def register(request):
    if request.method == "POST":
        errors = User.objects.validate_registration(request.POST)
        if not errors:
            user = User.objects.create_user(request.POST)
            request.session["id"] = user.id        
        flash_errors(request, errors, "register")
    return redirect('/travels')

def login(request):
    if request.method == "POST":
        result = User.objects.validate_login(request.POST)
        if "user" in result :
            request.session["id"] = result["user"].id
            return redirect(reverse("dashboard"))
        flash_errors(request, result["errors"], "login")
    return redirect('/travels')

def travels(request):
    if not "id" in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session["id"])
    context = {
        "user" : user,
        "travels" : Travel.objects.all(),
        "others": Travel.objects.exclude(planner=user).exclude(joiner=user.id)
        }
    return render(request,'travel_buddy_app/travels.html',context)

def add(request):
    context={
        "user":User.objects.get(id=request.session["id"])
        }
    return render(request, 'travel_buddy_app/add.html',context)
    
def create(request):
    if request.method == "POST":
        plan_errors = Travel.objects.travel_validation(request.POST)
    if not plan_errors:
        Travel.objects.create_plan(request.POST, request.session["id"])
        return redirect('/travels') 
    else:
        flash_errors(request, plan_errors, "")
        return redirect('/add')

def show(request,travel_id):
    travel = Travel.objects.get(id=travel_id)
    context = {
         "travel": travel
        } 
    return render(request,'travel_buddy_app/show.html',context)

def join(request,travel_id):
    if request.method =="POST":
        dest_id = request.POST["destination"]
        traveler = User.objects.get(id=request.session["id"])
        travelplans = Travel.objects.get(id=dest_id)
        travelplans.joiner.add(traveler)
        travelplans.save()
        return redirect('/travels')

def unjoin(request):
    if request.method =="POST":
        dest_id = request.POST["destination"]
        traveler = User.objects.get(id=request.session["id"])
        travelplans = Travel.objects.get(id=dest_id)
        travelplans.joiner.remove(traveler)
        travelplans.save()
        return redirect('/travels')
    
def delete(request):
    if request.method == "POST":
        Travel.objects.get(id=request.POST["destination"]).delete()
        return redirect('/travels')

def logout(request):
    if 'id' in request.session:
        request.session.pop('id')
    return redirect('/')
