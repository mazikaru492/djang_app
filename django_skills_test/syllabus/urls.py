from django.urls import path
from . import views

app_name = 'syllabus'

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:id>/', views.detail, name='detail'),  
]