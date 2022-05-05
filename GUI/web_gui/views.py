# SJSU CMPE 138 Spring 2022 TEAM6
from django.shortcuts import render
from django.shortcuts import reverse
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect
# from django.forms.widgets import DateInput
from .sql_query import login_verify
from .sql_query.all_query import director
from .sql_query.all_query import aquarist
from .sql_query.all_query import curator


# from .sql_query.all_query import query


# ok
def welcome(request):
    return render(request, 'Home/home.html')


def index(request):
    return render(request, 'Login/signin.html')


def register(request):
    if request.method == "POST":
        pass
        reg_info = []
        reg_info.append(request.POST.get('selection'))
        reg_info.append(request.POST.get('u_id'))
        reg_info.append(request.POST.get("uname"))
        reg_info.append(request.POST.get("phone"))
        reg_info.append(request.POST.get("email"))
        reg_info.append(request.POST.get("pwd"))
        dire = director()
        res = dire.hire_staff(*reg_info)
        if res:
            url = reverse('main_report', kwargs = {'job_title': 'DIRECTOR', "actions": "view"})
            return redirect(url)
        else:
            return redirect('login_page')

    return render(request, 'Register/register.html')


def log_in(request):
    """
    get username and pwd from webpage,
    using query to see where it exsits.
    if exsit,redirect to relative pages,
    otherwise return error
    """
    if request.method == "POST":
        request.session['table'] = ''
        login_info = [request.POST.get('username'), request.POST.get('pwd')]
        if login_info[0] and login_info[1]:
            res = login_verify.verify_user(*login_info)
            if res[1]:
                request.session['table'] = res[0]
                request.session['id'] = login_info[0]
                check_title(request)
                url = reverse('report_pages', kwargs = {"job_title": request.session['title']})
                return redirect(url)
        else:
            return render(request, 'Login/signin.html', {'msg': 'username or password wrong'})

    elif request.method == "GET":
        return render(request, 'Login/signin.html')


def report_view(request, job_title):
    """
    return different type of webpage based on the job title
    :param request:
    :return:
    """
    if job_title == "AQUARIST":
        # test login
        # username = 987153744
        # password = 987153744
        url = reverse('main_report', kwargs = {'job_title': job_title, "actions": "view"})
        return redirect(url)
    elif job_title == "CURATOR":
        # test login
        # username = 736289249
        # password = 736289249
        url = reverse('main_report', kwargs = {'job_title': job_title, "actions": "view"})
        return redirect(url)
    elif job_title == "MANAGER":
        # test login
        # username = 218363685
        # password = 218363685
        url = reverse('main_report', kwargs = {'job_title': job_title, "actions": "view"})
        return redirect(url)
    elif job_title == "DIRECTOR":
        # test login
        # username = 517465989
        # password = 517465989
        url = reverse('main_report', kwargs = {'job_title': job_title, "actions": "view"})
        return redirect(url)

    return render(request, 'Login/signin.html')


def main_view(request, actions, job_title):
    if actions == 'view' and job_title == 'DIRECTOR':
        dire = director()
        value = dire.view_staff_report()
        cont = {
            'actions': actions,
            'job_title': job_title,
            'animal_h': value[0],
            'animal_r': value[1],
            'manager_h': value[2],
            'manager_r': value[3],
            'aquarist_h': value[4],
            'aquarist_r': value[5],
            'event_h': value[6],
            'event_r': value[7],
        }
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        selected = request.POST.get('selection')
        event_ranges = [selected, from_date, to_date]
        if from_date and to_date and selected:
            res = dire.view_event(*event_ranges)
            cont['event_range_h'] = res[0]
            cont['event_range_r'] = res[1]
        return render(request, "Director/director.html", cont)

    elif actions == 'view' and job_title == 'AQUARIST':
        aq = aquarist()
        id = request.session['id']
        result = aq.check_maint_times(id)
        # print(result)
        cont = {
            'actions': actions,
            'job_title': job_title,
            'aqu_h': result[0],
            'aqu_r': result[1]
        }
        return render(request, "Aquarist/aquarist.html", cont)

    elif actions == 'view' and job_title == 'CURATOR':
        cura = curator()
        result1 = cura.check_an_Status()
        result2 = cura.view_all_facilities()
        id_list = []
        for i in result1[1]:
            id_list.append(i[1])
        # print(test_list)
        cura_line = zip(result1, id_list)
        cont = {
            'actions': actions,
            'job_title': job_title,
            'cura_h': result1[0],
            'cura_r': result1[1],
            # 'button_id':id_list
            'ava_h': result2[0],
            'ava_r': result2[1],
        }

        return render(request, "Curator/curator.html", cont)

    elif actions == 'view' and job_title == 'MANAGER':
        return render(request, "Event_manager/event_manager.html")


def editing(request, job_title, actions):
    if actions == 'view' and job_title == 'DIRECTOR':
        dire = director()
        dire.refreshAll()
        url = reverse('main_report', kwargs = {'job_title': job_title, "actions": "view"})
        return redirect(url)
    elif actions == 'view' and job_title == 'AQUARIST':
        aq = aquarist()
        arg_list = [request.POST.get('maintain_id'), request.POST.get('maintain_time')]
        aq.maintain_facility(*arg_list)
        url = reverse('main_report', kwargs = {'job_title': job_title, "actions": "view"})
        return redirect(url)

    elif actions == 'view' and job_title == 'CURATOR':
        cur = curator()
        arg = request.POST.get('animal_id')
        if arg:
            cur.update_an_Status(arg)
        url = reverse('main_report', kwargs = {'job_title': job_title, "actions": "view"})
        return redirect(url)


def fire(request, job_title, actions):
    id = request.POST.get('fire_delete')
    dire = director()
    res = dire.fire_staff(id)
    if res:
        print("ok")
    url = reverse('main_report', kwargs = {'job_title': job_title, "actions": "view"})
    return redirect(url)


def deleting(request, job_title, actions):
    if actions == 'view' and job_title == 'DIRECTOR':
        id = request.POST.get('event_delete')
        if len(id) == 6:
            dire = director()
            res = dire.cancel_event(101001)
            if res:
                print("ok")
        url = reverse('main_report', kwargs = {'job_title': job_title, "actions": "view"})
        return redirect(url)
    elif actions == 'view' and job_title == 'CURATOR':
        cur = curator()
        arg = request.POST.get('animal_id')
        if arg:
            res = cur.remove_animal(request.session['id'], arg)
            if res:
                print('ok')
        url = reverse('main_report', kwargs = {'job_title': job_title, "actions": "view"})
        return redirect(url)


def testing(request, job_title, actions, id_num):
    url = reverse('main_report', kwargs = {'job_title': job_title, "actions": "view"})
    return redirect(url)


def creating(request, job_title, actions):
    if actions == 'view' and job_title == 'DIRECTOR':
        create_event = []
        create_event.append(request.POST.get('event_id'))
        create_event.append(request.POST.get('event_title'))
        create_event.append(request.POST.get('create_selection'))
        create_event.append(request.POST.get('event_overseer'))
        if create_event[0] and create_event[1] and create_event[2] and create_event[3]:
            dire = director()
            res = dire.create_event(*create_event)
            if res:
                print("ok")
        url = reverse('main_report', kwargs = {'job_title': job_title, "actions": "view"})
        return redirect(url)
    elif actions == 'view' and job_title == 'CURATOR':
        cur = curator()
        arg_list = []
        arg_list.append(request.POST.get('animal_id'))
        arg_list.append(request.POST.get('animal_name'))
        arg_list.append(request.POST.get('selection'))
        arg_list.append(request.session['id'])
        arg_list.append(request.POST.get('facility_id'))
        cur.add_new_animal(*arg_list)
        url = reverse('main_report', kwargs = {'job_title': job_title, "actions": "view"})
        return redirect(url)


def check_title(request) -> int:
    """
    by checking the table name set the job title for it
    title = staff, when table is aquarist,curator,event_manager
    title = Director when table is general_manager
    """
    table = request.session['table']
    if table is not None:
        if table == "aquarist":
            request.session['title'] = 'AQUARIST'
        elif table == "curator":
            request.session['title'] = 'CURATOR'
        elif table == "event_manager":
            request.session['title'] = 'MANAGER'
        elif table == "general_manager":
            request.session['title'] = 'DIRECTOR'
