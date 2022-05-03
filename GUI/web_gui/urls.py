# SJSU CMPE 138 Spring 2022 TEAM4
from django.urls import path,re_path
from . import views

urlpatterns = [
    #path('index/',views.index),
    # path('',views.welcome),
    path('',views.index,name = 'index_page'),
    path(r'login/',views.log_in,name = 'login_page'),
    path('register/',views.register,name='reg'),
    re_path(r'^(?P<job_title>\w+)/$',views.report,name = 'jobs_page'),
    # re_path(r'^(?P<title>\w+)/(?P<op>\w+)/$',views.todo_view,name='ops'),


    # path('',views.welcome),
    # path('login/',views.log_in,name = 'login'),
    # path('director/',views.dire,name = 'dire_edit'),
    # path('Home',views.home, name='home'),
    # path('register',views.register, name='tiny')
]
