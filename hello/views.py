from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Friend
from django.db.models import QuerySet
from .forms import HelloForm


def index(request):
    data = Friend.objects.all()
    params = {
        'title': 'Hello',
        'data': data,
    }
    return render(request, 'hello/index.html', params)
#crate model
def create(request):
    params = {
        'title': 'Hello',
        'form': HelloForm(),
    }
    if (request.method == 'POST'):
        name = request.POST.get('name')
        mail = request.POST.get('mail')
        gender = 'gender' in request.POST
        age = int(request.POST.get('age'))
        birth = request.POST.get('birthday')
        dirth = Friend(name=name, mail=mail, gender=gender, age=age, birthday=birth)
        dirth.save()
        return redirect('/hello')
    return render(request, 'hello/create.html', params)