'''
    from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
'''

from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cluster import Cluster
from polls.models import TestModel
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import TestModel
from .forms import PersonForm

'''
def index(request):
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    session.set_keyspace('ndb')
    insert = TestModel(nrc="12/mgdn(naing)123456",labour_id="Hello",marital_status=1,name="ei nghon",race="burmese",religion="muslim")
    insert.save()
    cluster.shutdown()
    return HttpResponse("Hello world")
'''

def index(request):
    return render(request, 'base.html')

#return HttpResponse("Hello, world. You're at the polls index.")

def add_a_person(request):
    submitted = False
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            print("save")
            return HttpResponseRedirect('/add_a_person/?submitted=True')
    else:
        form = TestModel()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'add_a_person.html', {'form': form, 'submitted': submitted})
#return HttpResponse("DONE")


def get_a_person(request):
    a= [0,1,2,3]
    b= {'a':0,'b':1}
    return render( request, 'retrieve_person.html',{'TestModel': TestModel.objects.get(name='ei nghon'),'list':a,'dict':b})

def delete_a_person(request):
    submitted = False
    if request.method == 'POST':
        aa = request.POST
        c = TestModel.objects.get(nrc=aa.get('nrc'))
        c.delete();
        return HttpResponseRedirect('/delete_a_person/?submitted=True')

    else:
        form = TestModel()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'delete_person.html', {'form': form, 'submitted': submitted})

def request_approval(request):
    submitted = False
    if request.method == 'POST':
        aa = request.POST
        c = TestModel.objects.get(nrc=aa.get('nrc'))
        return render(request, 'receive_approval.html', {'TestModel': c})
    else:
        form = TestModel()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'request_approval.html', {'form': form, 'submitted': submitted})

def update_person(request):
    submitted = False
    if request.method == 'POST':
        aa = request.POST
        c = TestModel.objects.get(nrc=aa.get('nrc'))
        return render(request, 'receive_approval.html', {'TestModel': c})
    else:
        form = TestModel()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'request_approval.html', {'form': form, 'submitted': submitted})
