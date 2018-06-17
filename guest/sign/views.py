#coding=utf-8
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from sign.models import Event,Guest
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging
# Create your views here.
'''
def index(request):
    return HttpResponse("Hello Django!")
'''

# create by html template
def index(request):
    return render(request, "index.html")

def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        #if user is not None:
            #auth.login(request, user)
            #request.session['user'] = username
            #response = HttpResponseRedirect('/event_manage/')
            #return response
        
        if username == 'admins' and password == 'admins456':
            return HttpResponse('login success!!')
            return HttpResponseRedirect('/event_manage/')
            response = HttpResponseRedirect('/event_manage/')
            response.set_cookie('user', username, 3600)
            request.session['user'] = username 
            return response
        
        else:
            return render(request, 'index.html', {'error': 'username or password error!'})

#發布會管理
@login_required
def event_manage(request):
    # username = request.COOKIES.get('user', '')
    event_list = Event.objects.all()
    username = request.session.get('user', '')
    return render(request, "event_manage.html",{"user":username,
                                                "events":event_list})
    #return render(request, "event_manage.html")

#發布會名稱搜索
@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get("name", "")
    event_list = Event.objects.filter(name_contains=search_name)
    return render(request, "event_manage.html", {"user": username,
                                                 "events": event_list})

#嘉賓管理
@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.all()
    #劃分頁,每頁顯示兩條數據
    paginator = paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        #如果不是整數,取第一頁數據
        contacts = paginator.page(1)
    except EmptyPage:
        #如果page,不再範圍,取最後一頁面
        contacts = paginator.page(paginiator.num_pages)
    return render(request, "guest_manage.html" ,{"user": username, "guests": contacts})
    #return render(request, "guest_manage.html", {"user": username,
    #                                             "guest": guest_list})-->

#簽到頁面
@login_required
def sign_index(request, eid):
    event = get_object_or_404(Event, id=eid)
    return render(request, 'sign_index.html', {'event':event})

# 签到动作
@login_required
def sign_index_action(request,eid):

    event = get_object_or_404(Event, id=eid)
    phone = request.POST.get('phone','')
    print(phone)

    result = Guest.objects.filter(phone = phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event,'hint': 'phone error.'})

    result = Guest.objects.filter(phone = phone,event_id = eid)
    if not result:
        return render(request, 'sign_index.html', {'event': event,'hint': 'event id or phone error.'})

    result = Guest.objects.get(event_id = eid,phone = phone)

    if result.sign:
        return render(request, 'sign_index.html', {'event': event,'hint': "user has sign in."})
    else:
        Guest.objects.filter(event_id = event_id,phone = phone).update(sign = '1')
        return render(request, 'sign_index.html', {'event': event,'hint':'sign in success!',
            'guest':result
            })

#退出登入
@login_required
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/index/')
    return response
'''
get方法是从数据库的取得一个匹配的结果，返回一个对象，如果记录不存在的话，它会报错。
filter方法是从数据库的取得匹配的结果，返回一个对象列表，如果记录不存在的话，它会返回[]。
'''