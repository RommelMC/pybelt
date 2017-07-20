from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from models import *
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'travel/index.html')

def login(request):
    if request.method=='POST':
        if request.POST['action'] == 'register':
            errors = User.objects.validator(request.POST)
            if len(errors) > 0:
                for tag, error in errors.iteritems():
                    messages.error(request, error)
                return redirect(reverse('index'))
            hashpw = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt())
            User.objects.create(name=request.POST['name'], username=request.POST['username'], password=hashpw)
            request.session['curr'] = User.objects.get(username=request.POST['username']).id
            return redirect(reverse('home'))
        elif request.POST['action'] == 'login':
            if len(User.objects.filter(username=request.POST['username'])) == 0:
                messages.error(request,'Invalid username')
                return redirect(reverse('index'))
            if not bcrypt.checkpw(request.POST['pw'].encode(), User.objects.get(username=request.POST['username']).password.encode()):
                messages.error(request,'Invalid password')
                return redirect(reverse('index'))
            else:
                request.session['curr']=User.objects.get(username=request.POST['username']).id
                return redirect(reverse('home'))

def home(request):
    # allusertrips= (Trip.objects.get(planner=User.objects.get(id=request.session['curr'])) | Trip.objects.get(User.objects.get(id=request.session['curr']) in joiners)).distinct()
    # allusertrips=(User.objects.get(id=request.session['curr']).trips | User.objects.get(id=request.session['curr']).jtrips).distinct()
    allusertrips=User.objects.get(id=request.session['curr']).jtrips.all()
    context={
        'trips':allusertrips, 'alltrips': Trip.objects.exclude(pk__in = allusertrips), 'user':User.objects.get(id=request.session['curr'])
    }
    return render(request, 'travel/home.html', context)

def add(request):
    return render(request, 'travel/add.html')

def addtrip(request):
    if request.method=='POST':
        errors = Trip.objects.validator(request.POST)
        if len(errors) > 0:
            for error in errors:
                messages.error(request, error)
            return redirect(reverse('add'))
        sdate=datetime.strptime(request.POST['start'], '%Y-%m-%d').date()
        edate=datetime.strptime(request.POST['end'], '%Y-%m-%d').date()
        t1 = Trip.objects.create(destination=request.POST['dest'], description=request.POST['desc'], startDate=sdate, endDate=edate, planner=User.objects.get(id=request.session['curr']))
        t1.joiners.add(User.objects.get(id=request.session['curr']))
        return redirect(reverse('home'))

def join(request, id):
    User.objects.get(id=request.session['curr']).jtrips.add(Trip.objects.get(id=id))
    return redirect(reverse('home'))

def trippage(request, id):
    context={
        'trip':Trip.objects.get(id=id)
    }
    return render(request, 'travel/trippage.html', context)