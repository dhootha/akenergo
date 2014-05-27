from django import template
from django.utils.translation import ugettext as _

from energosite.models import *



register = template.Library()


@register.inclusion_tag('tags/top_menu.html', takes_context=True)
def top_menu(context):
    return {
        'top_menu_nodes': TopMenu.objects.filter(level=0, published=True),
        'request': context.get('request'),
    }


@register.inclusion_tag('tags/bottom_menu.html', takes_context=True)
def bottom_menu(context):
    return {
        'bottom_menu_nodes': TopMenu.objects.filter(level=0, published=True),
        'request': context.get('request'),
    }


@register.inclusion_tag('tags/recent_news_list.html', takes_context=True)
def recent_news_list(context, num=10):
    return {
        'news_list': Article.objects.filter(published=True, tip=1).order_by('-date')[:num],
        'request': context.get('request'),
    }

@register.simple_tag(takes_context=True)
def current_nav(context, url):
    if not context.get('request'):
        return ''
    path = context.get('request').path
    #    url = template.Variable(self.url).resolve(context)
    if (url == '/' or url == '') and not (path == '/' or path == ''):
        return ''
    if path.startswith(url):
        return 'active'
    return ''


# ------------------------------------------------------------------------

@register.inclusion_tag("tags/breadcrumbs.html", takes_context=True)
def breadcrumbs(context, show_home=True):
    # trail_home = [('/', _('Home'))]
    if context.get('trail'):
        # return {"trail": trail_home + context.get('trail')}
        return {"trail": context.get('trail'), "show_home": show_home}
    else:
        return {"trail": [], "show_home": show_home}


from django.utils.encoding import force_unicode
import re


def intspace(value):
    """
    Converts an integer to a string containing spaces every three digits.
    For example, 3000 becomes '3 000' and 45000 becomes '45 000'.
    See django.contrib.humanize app
    """
    orig = force_unicode(value)
    new = re.sub("^(-?\d+)(\d{3})", '\g<1> \g<2>', orig)
    if orig == new:
        return new
    else:
        return intspace(new)


@register.filter
def currency(money):
    if not money:
        return '0.00'
    value = round(float(money), 2)
    return '{0},{1}'.format(intspace(int(value)), ("{:.2f}".format(value))[-2:])


@register.filter
def none2zero(value):
    if value:
        return value
    else:
        return '0'


import calendar


@register.filter
def month_name(month_number):
    if month_number:
        return _(calendar.month_name[int(month_number)])
    else:
        return ''


@register.assignment_tag(takes_context=True)
def get_department(context):
    user = None
    request = context.get('request')
    if request:
        user = getattr(request, 'user')
    if user and isinstance(user, User):
        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=user)
        nls = getattr(profile, 'nls')
        abons = Abonbaza.objects.filter(nls=nls)
        if not abons.count() or int(nls) == 0:
            return 0
        else:
            return abons[0].department.id


@register.assignment_tag
def get_page(page_link):
    pages = Page.objects.filter(link=page_link, published=True)
    if pages.count():
        return dict(title=pages[0].title, content=pages[0].content)
    else:
        return dict(title='', content='')


#    "$%s%s" % (intcomma(int(dollars)), ("%0.2f" % dollars)[-3:])


@register.inclusion_tag("tags/pager.html")
def show_pager(pager, num_pages=4, pager_class='pagination'):
    page_steps = range(1, num_pages + 1)
    page_steps_reversed = [-elm for elm in reversed(page_steps)]

    pages_count = pager.paginator.num_pages

    pages = []
    if pager.has_previous():
        pages.append({'num': pager.previous_page_number(), 'caption': '&laquo;', 'class': None})
        pages.append({'num': 1, 'caption': 1, 'class': None})
    else:
        pages.append({'num': None, 'caption': '&laquo;', 'class': 'disabled'})

    page_number = pager.number
    left_pages = [elm + page_number for elm in page_steps_reversed if elm + page_number > 1]
    for i, page_num in enumerate(left_pages):
        if i == 0 and page_num > 2:
            pages.append({'num': None, 'caption': '...', 'class': 'disabled'})
        pages.append({'num': page_num, 'caption': page_num, 'class': None})

    pages.append({'num': None, 'caption': page_number, 'class': 'active'})

    right_pages = [elm + page_number for elm in page_steps if elm + page_number < pages_count]
    for i, page_num in enumerate(right_pages):
        pages.append({'num': page_num, 'caption': page_num, 'class': None})
        if (i == len(right_pages) - 1) and (page_num < pages_count - 1):
            pages.append({'num': None, 'caption': '...', 'class': 'disabled'})

    if pager.has_next():
        pages.append({'num': pages_count, 'caption': pages_count, 'class': None})
        pages.append({'num': pager.next_page_number(), 'caption': '&raquo;', 'class': None})
    else:
        pages.append({'num': None, 'caption': '&raquo;', 'class': 'disabled'})


    return {'pages': pages, 'pager_class': pager_class}



@register.inclusion_tag("blocks/standard_form.html")
def standard_form(form, form_id='standard_form', action='', req_method='POST', submitCaption='OK'):
    return {'form':form, 'formId': form_id, 'ACTION': action, 'REQ_METHOD': req_method, 'submCaptrans': submitCaption}