from django.urls import path

from . import views


app_name = 'django_book_store'

urlpatterns = [
    path('', views.login_screen, name='home'),
    path('login/', views.login_screen, name='login'),
    path('index/', views.index, name='index'),
    path('logout/', views.logout_employee, name='logout'),
]
