from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Course

def index(request):
    keyword = request.GET.get('keyword', '')
    if keyword:
        course_list = Course.objects.filter(
            Q(title__icontains=keyword) | Q(teacher__icontains=keyword)
        )
    else:
        
        course_list = Course.objects.all()
    paginator = Paginator(course_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': '講義シラバス検索',
        'message': '講義名または担当教員名で検索できます。',
        'keyword': keyword,
        'page_obj': page_obj,
    }

    return render(request, 'syllabus/index.html', context)