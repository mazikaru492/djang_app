from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Course
from .forms import ReviewForm, CourseForm

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

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.course = course
            review.save()
            return redirect('syllabus:detail', id=course.id)
    else:
        form = ReviewForm()
    reviews = course.review_set.all().order_by('-created_at')
    context = {
        'title': '講義詳細（シラバス）',
        'course': course,
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'syllabus/detail.html', context)







def create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('syllabus:index')
    else:
        form = CourseForm()

    context = {
        'title': '新規講義の登録',
        'form': form,
    }
    return render(request, 'syllabus/course_form.html', context)


def edit(request, id):
    course = get_object_or_404(Course, id=id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('syllabus:index')
    else:
        form = CourseForm(instance=course)

    context = {
        'title': '講義情報の編集',
        'form': form,
    }
    return render(request, 'syllabus/course_form.html', context)


def delete(request, id):
    course = get_object_or_404(Course, id=id)
    if request.method == 'POST':
        course.delete()
        return redirect('syllabus:index')
    context = {
        'title': '講義の削除',
        'course': course,
    }
    return render(request, 'syllabus/course_confirm_delete.html', context)