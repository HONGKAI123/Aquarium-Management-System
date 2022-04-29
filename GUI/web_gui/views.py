from django.shortcuts import render
from .sql_query import director
from .sql_query import aquarist as aqu
from .sql_query import curator_remove_animal as c_remove
import hashlib
import datetime

# Create your views here.

# from django.http import HttpResponse

from django.db import connection
from mysql import connector

def welcome(request):
    """
    test pages, check sql connection
    """
    # with connection.cursor() as cursor:
    #     cursor.execute(r"SELECT * FROM animal")
    #     row = cursor.fetchall()
    temp = director.view_event('exhibit', '2022-05-02', '2022-05-04')
    print(temp)
    sample = temp;
    # sample = range(1,10)
    # sample = [[],[]]
    # for i in range(1,10):
    #     for j in range(1,10):
    #         sample[0].append(j*i)
    #     sample[1].append(i)
    # print(sample)
    # return render(request, 'index.html', {'numbers': sample})
    test_data = [('101001', 'penguin exhibit', 'exhibit', datetime.date(2022, 5, 4), 130), ('101001', 'penguin exhibit', 'exhibit', datetime.date(2022, 5, 3), 120), ('101002', 'whale exhibit', 'exhibit', datetime.date(2022, 5, 4), 100)]
    test_data_header = ['id','name','type','date']
    return render(request,'Director/director.html',{"job_title":"fuck!","main_table":test_data,"main_table_header":test_data_header,})


def index(request):
    return render(request, 'Login/signup.html')





def log_in(request):
    """
    get username and pwd from webpage,
    using query to see where it exsits.
    if exsit,redirect to relative pages,
    otherwise return error
    """
    if request.method == "POST":
        # todo
        # todo miss select user from each table
        # todo by get user from different table, show the different webpage to them
        # todo set session about the title
        request.session['title'] = '';

        # if row:

        user_name = request.POST.get('username')
        pwd = request.POST.get('pwd')
        print(user_name)
        hash_pwd = hashlib.sha256(pwd.encode('utf-8')).hexdigest()
        print(hash_pwd)

        # with connection.cursor() as cursor:
        with connection.cursor() as cursor:
            cursor.execute(r"SELECT * FROM animal")
            row = cursor.fetchall()

        if 1:
            return render(request, 'Director/director.html',{'job_title':"ha?"})
        else:
            return render(request, 'Login/signup.html', {'error': 'username or password wrong'})
    elif request.method == "GET":
        return render(request, 'Login/signup.html')




def report(request):
    """
    return different type of webpage based on the job title
    :param request:
    :return:
    """
    title = check_title(request)
    if title > 0:
        if title == 1:
            pass
            # todo sql query
            return render(request,'Director/director.html',{'table_value'})
        elif title ==2:
            pass
        elif title ==3:
            pass
        elif title ==4:
            pass
    else:
        return render()


"""
:return 0 if the session/cookie value invalid
return 1 for 
return 2 for 
return 3 for 
"""
def check_title(request) -> int:
    title = request.session['title']
    if title is not None:
        if title == "xxx":
            return 1
        elif title == "yyy":
            return 2
        elif title == "zzz":
            return 2
    else:
        return 0

def dire(request):
    pass