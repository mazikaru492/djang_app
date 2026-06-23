from djang.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('groups', views.groups, name='groups'),
    path('add',views.add, name='add'),
    path('creategroup', views.creategroup, name='creategroup'),
    path('post',views.post,name='post'),
    path('share/<int:share_id>/', views.share, name='share'),
    path('good/<int:message_id>/', views.good, name='good'),
]