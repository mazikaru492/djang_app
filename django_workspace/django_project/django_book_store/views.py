from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters

from .forms import LoginForm
from .models import Employee


def _session_employee(request):
    employee_no = request.session.get('book_store_employee_no')
    if not employee_no:
        return None
    employee = Employee.objects.filter(employee_no=employee_no).first()
    if employee is None:
        request.session.pop('book_store_employee_no', None)
    return employee


@sensitive_post_parameters('password')
@never_cache
@require_http_methods(['GET', 'POST'])
def login_screen(request):
    if request.method == 'GET' and _session_employee(request) is not None:
        return redirect('django_book_store:index')
    form = LoginForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        request.session.cycle_key()
        request.session['book_store_employee_no'] = form.employee.employee_no
        return redirect('django_book_store:index')

    return render(request, 'django_book_store/login.html', {
        'form': form,
    })


@never_cache
@require_http_methods(['GET'])
def index(request):
    employee = _session_employee(request)
    if employee is None:
        return redirect('django_book_store:login')
    return render(request, 'django_book_store/index.html', {'employee': employee})


@require_POST
def logout_employee(request):
    request.session.pop('book_store_employee_no', None)
    request.session.cycle_key()
    return redirect('django_book_store:login')
