from django.shortcuts import render, get_object_or_404
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


def detail(request, id):
    course = get_object_or_404(Course, id=id)
    reviews = course.review_set.all().order_by('-created_at')
    context = {
        'title': '講義詳細（シラバス）',
        'course': course,
        'reviews': reviews,
    }
    return render(request, 'syllabus/detail.html', context)