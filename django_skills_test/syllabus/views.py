from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Course

def index(request):
    course_list = Course.objects.all()
    paginator = Paginator(course_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'syllabus/index.html', {'page_obj': page_obj})