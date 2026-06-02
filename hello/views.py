from django.shortcuts import render
from django.http import HttpResponse
from .models import Friend
from .forms import HelloForm


def index(request):
    data = Friend.objects.all()
    form = HelloForm()
    result = None
    if request.method == 'POST':
        form = HelloForm(request.POST)
        if form.is_valid():
            ch = form.cleaned_data['id']
            result = 'selected: ' + str(ch) + '.'

    params = {
        'title': 'Hello',
        'message': 'all friends.',
        'data': data,
        'form': form,
        'result': result,
    }
    return render(request, 'hello/index.html', params)
