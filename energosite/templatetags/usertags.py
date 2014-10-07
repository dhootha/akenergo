# -*- coding: utf-8 -*-
___author__ = 'uzer'
from django import template
from energosite.models import *
#from django.utils.translation import ugettext as _

import datetime

register = template.Library()

"""
namefile: usertags.py
You would need a template nest for every method, for example to online_users.
/templates/tag/online_users.html

 {% if users %}
 <ul>
 {% for user in users %}
 <li>{{user.username}}</li>
 {% endfor %}
 </ul>
 {% endif %}

to load

{% load usertags %}
{% online_users 5 %}
{% last_registers 5 %}
{% last_logins 5 %}

"""
from energosite.views import get_address, get_fio, get_profile

def get_users_data(users):
    uzery = []
    for user in users:
        profile = get_profile(user)
        uzery.append({'username': user.username, 'nls': profile.nls, 'fio': get_fio(profile.nls),
                      'address': get_address(profile.nls), 'last_login': user.last_login,
                      'date_joined': user.date_joined})
    return uzery


@register.inclusion_tag('tags/users.html')
def online_users(num):
    """
 Show user that has been login an hour ago.
 """
    one_hour_ago = datetime.datetime.now() - datetime.timedelta(hours=1)
    sql_datetime = datetime.datetime.strftime(one_hour_ago, '%Y-%m-%d %H:%M:%S')
    users = get_user_model().objects.filter(last_login__gt=sql_datetime,
        is_active__exact=1).order_by('-last_login')[:num]

    return {
        'users': get_users_data(users),
        'title': "Пользователи в сети",
    }


@register.inclusion_tag('tags/users.html')
def last_registers(num):
    """
 Show last registered users.
 """
    users = get_user_model().objects.filter(is_active__exact=1).order_by('-date_joined')[:num]
    return {
        'users': get_users_data(users),
        'title': "Зарегистрированные пользователи"
    }


@register.inclusion_tag('tags/users.html')
def last_logins(num):
    """
 Show last logins ...
 """
    users = get_user_model().objects.filter(is_active__exact=1).order_by('-last_login')[:num]
    return {
        'users': get_users_data(users),
        'title': "Последние залогинившиеся",
    }

