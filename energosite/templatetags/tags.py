# -*- coding: utf-8 -*-
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


#def current_nav(parser, token):
#    args = token.split_contents()
#    template_tag = args[0]
#    if len(args) < 2:
#        raise template.TemplateSyntaxError, "%r tag requires at least one argument" % template_tag
#    return NavSelectedNode(args[1])

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

#@register.inclusion_tag("tags/breadcrumbs.html", takes_context=True)
#def breadcrumbs(context):
#    """
#    Generate a list of the page's ancestors suitable for use as breadcrumb navigation.
#    By default, generates an unordered list with the id "breadcrumbs" -
#    override breadcrumbs.html to change this.
#    """
#    trail = []
#
#    if not context.get('request'):
#        return {"trail": trail}
#    current_link = context['request'].path
#    match = resolve(current_link)
#    if match.url_name == 'show_page':
#        menus = TopMenu.objects.filter(page__link=match.kwargs.get('link', None))
#        if menus:
#            menu = menus[0]
#            ancs = menu.get_ancestors()
#            trail = [(reverse('list_submenus', args=[anc.id]), anc.title) for anc in ancs]
#    elif match.url_name == 'show_article':
#        menus = TopMenu.objects.filter(link=reverse('news_list'))
#        if menus:
#            menu = menus[0]
#            trail = [(menu.get_absolute_url(), menu.title)]
#    elif match.url_name == 'contact_form':
#        menus = TopMenu.objects.filter(link=reverse('contact_form'))
#        if menus:
#            menu = menus[0].get_root()
#            trail = [(reverse('list_submenus', args=[menu.id]), menu.title)]
#    elif match.url_name == 'comments':
#        menus = TopMenu.objects.filter(link=reverse('comments'))
#        if menus:
#            menu = menus[0].get_root()
#            trail = [(reverse('list_submenus', args=[menu.id]), menu.title)]
#    elif match.url_name == 'list_submenus':
#        id = match.kwargs.get('menu_id')
#        menus = TopMenu.objects.filter(pk=id)
#        if menus:
#            menu = menus[0]
#            ancs = menu.get_ancestors()
#            trail = [(reverse('list_submenus', args=[anc.id]), anc.title) for anc in ancs]
#
#            #   trail.append((None, menu.title))
#            #    trail.insert (0, (reverse('home'), _('Home')))
#    return {"trail": trail}

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

    page_number = pager.number

    previous_page_number = None
    next_page_number = None
    has_previous = pager.has_previous()
    if has_previous:
        previous_page_number = pager.previous_page_number()
    has_next = pager.has_next()
    if has_next:
        next_page_number = pager.next_page_number()

    pages_count = pager.paginator.num_pages

    left_pages = [elm + page_number for elm in page_steps_reversed if elm + page_number > 1]
    right_pages = [elm + page_number for elm in page_steps if elm + page_number < pages_count]

    return {
        'page_number': page_number, 'has_previous': has_previous, 'has_next': has_next,
        'previous_page_number': previous_page_number,
        'next_page_number': next_page_number, 'pages_count': pages_count, 'left_pages': left_pages,
        'right_pages': right_pages, 'pager_class': pager_class
    }