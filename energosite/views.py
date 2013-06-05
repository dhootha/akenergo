# -*- coding: utf-8 -*-
from django.shortcuts import HttpResponseRedirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from django.core.mail import EmailMessage
from django.contrib.sites.models import Site
from django.http import HttpResponse, Http404

from energosite.models import *
from energosite.forms import *

#from django.template import loader, Context
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import ugettext as _
from django.conf import settings
from django.contrib import messages
from dbfpy import dbf
from django.core.cache import cache
from django.template.loader import render_to_string
import hashlib, os, random
from django.utils import timezone
from registration.models import RegistrationProfile
from django.contrib.sites.models import RequestSite
from django.contrib.auth.views import login as django_login
from django.contrib.auth.forms import AuthenticationForm
from django.utils.encoding import force_unicode
import json
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url


def index(request):
    HI_PAGE = get_object_or_404(Page, link='hi', published=True)
    return render(request, 'posts/index.html', {'HI_PAGE': HI_PAGE})


# def ajaxFormErrorsResponse(form):
#     response = {}
#     for err in form.errors:
#         response[err] = form.errors[err][0]
#         # print response[err]
#     non_f_err = form.non_field_errors()
#     return HttpResponse(simplejson.dumps({'response': response, 'response_header': '',
#                                           'non_f_err': non_f_err, 'result': 'error'}), content_type="application/json")


def ajaxResponse(form_errors, response='', response_header='', form=None, update_values=None, captcha_key=None,
                 captcha_image=None):
    errors = {}
    if form_errors and form:
        for field in form:
            if field.errors:
                errors[force_unicode(field.name)] = '; '.join(field.errors)

        if form.non_field_errors():
            errors['non_field'] = '; '.join(form.non_field_errors())

        return HttpResponse(json.dumps({'errors': errors, 'captcha_key': captcha_key,
                                        'captcha_image': captcha_image, 'result': 'error'}),
                            content_type="application/json")

    else:
        return HttpResponse(json.dumps({'response': response, 'response_header': response_header,
                                        'update_values': update_values, 'captcha_key': captcha_key,
                                        'captcha_image': captcha_image, 'result': 'success'}),
                            content_type="application/json")

#
# from django.utils.http import is_safe_url
# from django.http import HttpResponseRedirect as HRR
# from django.utils.translation import check_for_language

# def set_language(request):
#     """
#     Redirect to a given url while setting the chosen language in the
#     session or cookie. The url and the language code need to be
#     specified in the request parameters.
#
#     Since this view changes how the user will see the rest of the site, it must
#     only be accessed as a GET request. If called as a POST request, it will
#     redirect to the page in the request (the 'next' parameter) without changing
#     any state.
#     """
#     next = request.REQUEST.get('next')
#     if not is_safe_url(url=next, host=request.get_host()):
#         next = request.META.get('HTTP_REFERER')
#         if not is_safe_url(url=next, host=request.get_host()):
#             next = '/'
#     response = HRR(next)
#     if request.method == 'GET':
#         lang_code = request.GET.get('language', None)
#         if lang_code and check_for_language(lang_code):
#             if hasattr(request, 'session'):
#                 request.session['django_language'] = lang_code
#             else:
#                 response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
#     return response


def show_page(request, link):
    page = get_object_or_404(Page, link=link, published=True)
    trail = []
    menus = TopMenu.objects.filter(page__link=link)
    if menus.count():
        menu = menus[0]
        ancs = menu.get_ancestors()
        trail = [(reverse('list_submenus', args=[anc.id]), anc.title) for anc in ancs]
        #        trail.append((reverse('list_submenus', args=[menu.id]), menu.title))

    return render(request, 'posts/base_post.html', {'post': page, 'show_comments': False, 'trail': trail})


def show_article(request, link_id):
    article = get_object_or_404(Article, pk=link_id, published=True)
    # trail = []
    # menus = TopMenu.objects.filter(link=reverse('news_list'))
    # if menus.count():
    #     menu = menus[0]
    trail = [(reverse('news_list'), _('Site news'))]

    return render(request, 'posts/base_post.html', {'post': article, 'show_comments': True, 'trail': trail})


def list_submenus(request, menu_id):
    menus = TopMenu.objects.filter(pk=menu_id)
    submenus = None
    menu_title = ''
    trail = []
    if menus.count():
        menu = menus[0]
        menu_title = menu.title
        submenus = menu.get_descendants()
        ancs = menu.get_ancestors()
        trail = [(reverse('list_submenus', args=[anc.id]), anc.title) for anc in ancs]
    return render(request, 'posts/list_submenus.html', {'submenus': submenus, 'menu_title': menu_title, 'trail': trail})


def news_list(request):
    news_objects = Article.objects.filter(published=True, tip=1).order_by('-date')
    paginator = Paginator(news_objects, 10) # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        news_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        news_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        news_list = paginator.page(paginator.num_pages)

    page_limit = [1, 2, 3, 4]
    page_limitr = [-4, -3, -2, -1]
    return render(request, 'posts/news_list.html',
                  {"news_list": news_list, 'page_limit': page_limit, 'page_limitr': page_limitr})

# def getLastMonthPayment(nls):
#     sel = "SELECT nls, sum(opl) as opl FROM oplbaza " \
#           "where TO_CHAR(NOW(), 'MM') = TO_CHAR(DAT_KV, 'MM') and TO_CHAR(NOW(), 'YY') = TO_CHAR(DAT_KV, 'YY') " \
#           "and NLS = %s group by nls"
#     pays = Oplbaza.objects.raw(sel, [nls, ])
#     result = 0
#     for pay in pays:
#         result = pay.opl
#         break
#     return result


def is_ur_lica(kod):
    return int(kod) == 2


def is_fizlica(kod):
    return int(kod) == 1

def is_fizlica_rayon(kod):
    return int(kod) == 3



@login_required
def view_debtors(request, kod):
    today = getActualDate("debtors", kod)
    debs = cache.get('debs' + str(kod))
    #    sec = time.time()
    if not debs:
        debs = []
        debtors = Debtors.objects.raw("SELECT A.ID, A.NLS, A.DOLG, B.FIO, B.UL||' '||B.ND||"
                                      " CASE WHEN (B.NKOR!='') AND (B.NKOR!='0') AND (B.NKOR IS NOT NULL) THEN '/'||B.NKOR "
                                      " ELSE '' "
                                      " END || "
                                      " CASE WHEN (B.NKW!='') AND (B.NKW!='0') AND (B.NKW IS NOT NULL) THEN '-'||B.NKW "
                                      " ELSE '' "
                                      " END "
                                      " AS ADDRESS "
                                      " FROM DEBTORS A "
                                      " JOIN ABONBAZA B ON (A.NLS=B.NLS) "
                                      " WHERE A.DEPARTMENT_ID=%s ORDER BY B.UL, B.ND, B.NKOR, B.NKW", [kod])

        for nomer, debtor in enumerate(debtors):
            val = dict(nomer=nomer + 1, address=debtor.address, nls=debtor.nls, dolg=debtor.dolg, fio=debtor.fio)
            debs.append(val)
        cache.set('debs' + str(kod), debs)
        if not debs:
            raise Http404

    paginator = Paginator(debs, 100)
    page = request.GET.get('page')
    try:
        debtors_pages = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        debtors_pages = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        debtors_pages = paginator.page(paginator.num_pages)

    #    print "\n", time.time() - sec

    ur_lica = is_ur_lica(kod)

    trail = []
    menus = TopMenu.objects.filter(link=reverse('view_debtors', args=[kod]))
    if menus.count():
        menu = menus[0].get_root()
        trail = [(reverse('list_submenus', args=[menu.id]), menu.title)]

    page_limit = [1, 2, 3, 4]
    page_limitr = [-4, -3, -2, -1]

    return render(request, 'data/view_debtors.html',
                  {'debtors_pages': debtors_pages, 'today': today, 'ur_lica': ur_lica, 'trail': trail,
                   'page_limit': page_limit,
                   'page_limitr': page_limitr})


def nls_exists(ls):
    return Abonbaza.objects.filter(nls=ls).count() > 0


def get_profile(user):
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)
    return profile


def format_address(ul, nd, nkor, nkw):
    if (not nd) or len(nd.strip()) == 0:
        dom = u""
    else:
        dom = u" д." + nd.strip()
    if (not nkor) or len(nkor.strip()) == 0:
        korpus = u""
    else:
        korpus = u" к." + nkor.strip()
    if (not nkw) or len(nkw.strip()) == 0:
        kv = u""
    else:
        kv = u" кв." + nkw.strip()
    return ul.strip() + dom + korpus + kv


def get_address(nls):
    abons = Abonbaza.objects.filter(nls=nls)

    if not abons.count() or int(nls) == 0:
        return ""
    else:
        abonent = abons[0]

    return format_address(abonent.ul, abonent.nd, abonent.nkor, abonent.nkw)


def get_fio(nls):
    abons = Abonbaza.objects.filter(nls=nls)
    if not abons.count() or int(nls) == 0:
        return ""
    else:
        abonent = abons[0]
    return abonent.fio


def get_department(nls):
    abons = Abonbaza.objects.filter(nls=nls)
    if not abons.count() or int(nls) == 0:
        return ""
    else:
        return abons[0].department.name


def get_depid(nls):
    abons = Abonbaza.objects.filter(nls=nls)
    if not abons.count() or int(nls) == 0:
        return 0
    else:
        return abons[0].department.id


def get_iin(nls):
    abons = Abonbaza.objects.filter(nls=nls)
    if not abons.count() or int(nls) == 0:
        return ""
    else:
        return abons[0].iin


def get_kpp(nls):
    abons = Abonbaza.objects.filter(nls=nls)
    if not abons.count() or int(nls) == 0:
        return ""
    else:
        return abons[0].kpp


@login_required
def edit_profile(request):
    user = request.user
    profile = get_profile(user)
    fio, address, email = get_fio(profile.nls), get_address(profile.nls), profile.user.email

    if request.method == 'POST' and request.is_ajax():
        form = EditProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            new_nls = form.cleaned_data['nls']
            new_fio, new_address = get_fio(new_nls), get_address(new_nls)
            return ajaxResponse(False, response_header=_('Your profile was saved'),
                                update_values={'info_fio': new_fio, 'info_address': new_address})
        else:
            return ajaxResponse(True, form=form)

    form = EditProfileForm(instance=profile)
    return render(request, 'profile/edit_profile.html', {'form': form, 'fio': fio, 'address': address, 'email': email})


@login_required
def meter_reading(request):
    user = request.user
    profile = get_profile(user)

    if is_ur_lica(get_depid(profile.nls)):
        error = _("You don't have permission's")
        return render(request, 'load_data/data_error.html', {'error': error})

    if request.method == 'POST' and request.is_ajax():
        form = MeterReadingForm(request.POST)
        if form.is_valid():
            nls = form.cleaned_data['nls']
            year = timezone.now().year
            month = timezone.now().month
            objects = MeterReading.objects.filter(nls=nls, date__year=year, date__month=month)
            if not objects.count():
                mr = MeterReading(nls=nls)
                mr.date = timezone.now()
            else:
                mr = objects[0]
            mr.fio = form.cleaned_data['fio']
            mr.address = form.cleaned_data['address']
            mr.pok1 = form.cleaned_data['pok1']
            mr.pok2 = form.cleaned_data['pok2']
            mr.pok3 = form.cleaned_data['pok3']
            mr.save()
            # messages.add_message(request, messages.SUCCESS, _('Thank you!'))
            return ajaxResponse(False, response_header=_('Thank you!'))
        else:
            return ajaxResponse(True, form=form)

    fio = get_fio(profile.nls)
    address = get_address(profile.nls)
    dict___ = {'nls': profile.nls, 'fio': fio, 'address': address, 'date': timezone.now()}
    form = MeterReadingForm(initial=dict___)
    return render(request, 'load_data/meter_reading.html', {'form': form})


def encStr(str_, dest):
    try:
        return str_.encode(dest)
    except ValueError:
        return ''


def toInt(value):
    if value:
        try:
            return int(value)
        except ValueError:
            return 0
    else:
        return 0


def getToday():
    return datetime.date.today()


def getYear():
    return datetime.date.today().year


def getMonth():
    return datetime.date.today().month


def getDay():
    return datetime.date.today().day


@login_required
def load_reading(request):

#    for i in range(1, 50000):
#        mr = MeterReading(nls=i, fio='tty', address='trytyt', pok1=i, pok2=45, pok3=2, date=datetime.datetime.now())
#        mr.save()

    user = request.user
    if not user.has_perm('energosite.view_meter_reading'):
        error = "У вас нет прав для загрузки показаний!"
        return render(request, 'load_data/data_error.html', {'error': error})

    MONTHS = [(0, 'Все месяцы')] + [(rang, str(rang)) for rang in range(1, 13)]
    YEARS = [(rang, str(rang)) for rang in range(getToday().year - 2, getToday().year + 3)]
    if request.method == 'POST':
        form = LoadReading(request.POST)
        form.fields['month'].choices, form.fields['month'].initial = MONTHS, getMonth()
        form.fields['year'].choices, form.fields['year'].initial = YEARS, getYear()
        if form.is_valid():
            year = int(form.cleaned_data['year'])
            month = int(form.cleaned_data['month'])
            charset = form.cleaned_data['charset']
            date_filter = {'date__year': year}
            if month:
                date_filter['date__month'] = month
            mrss = MeterReading.objects.filter(**date_filter)
            #print MeterReading._meta.get_all_field_names()
            fileName = os.path.join(settings.MEDIA_ROOT, hashlib.md5(str(random.random())).hexdigest() + '.dbf')
            dbfFile = dbf.Dbf(fileName, new=True)
            dbfFile.addField(
                ("NLS", "N", 7, 0),
                ("FIO", "C", 50),
                ("ADDRESS", "C", 75),
                ("POK1", "N", 7, 0),
                ("POK2", "N", 7, 0),
                ("POK3", "N", 7, 0),
                ("DATE", "D"),
            )
            for mr in mrss:
                rec = dbfFile.newRecord()
                try:
                    rec['NLS'] = toInt(mr.nls)
                    rec['FIO'], rec['ADDRESS'] = encStr(mr.fio, charset), encStr(mr.address, charset)
                    rec['POK1'], rec['POK2'], rec['POK3'] = toInt(mr.pok1), toInt(mr.pok2), toInt(mr.pok3)
                    rec['DATE'] = mr.date
                    rec.store()
                except TypeError:
                    continue

            dbfFile.close()
            response = HttpResponse(content_type='application/dbf')
            response['Content-Disposition'] = 'attachment; filename=poks.dbf'
            file2read = open(fileName, 'rb')
            response.write(file2read.read())
            file2read.close()
            try:
                os.remove(fileName)
            except OSError:
                pass
            return response
    else:
        form = LoadReading()
        form.fields['month'].choices, form.fields['month'].initial = MONTHS, getMonth()
        form.fields['year'].choices, form.fields['year'].initial = YEARS, getYear()

    return render(request, 'load_data/load_reading.html', {'form': form})


def ajax_search_address(request):
    # abonents = None
    if request.method == 'POST' and request.is_ajax():
        form = SearchAddressForm(request.POST)
        if form.is_valid():
            # Обработка
            # ...
            department = request.POST.get('department', 0)
            ul = request.POST.get('ul', '')
            nd = request.POST.get('nd', '')
            nkor = request.POST.get('nkor', '')
            nkw = request.POST.get('nkw', '')

            condits = ["department_id = %s", "upper(ul) like %s", "upper(nd) = %s"]
            params = [department, ul.upper() + "%", nd.upper()]

            if nkor:
                condits.append("upper(nkor) = %s")
                params.append(nkor.upper())
            if nkw:
                condits.append("upper(nkw) = %s")
                params.append(nkw.upper())

            abonents = Abonbaza.objects.extra(where=condits, params=params).order_by("nls")[:100]
            return ajaxResponse(False, response=render_to_string('search/result_table.html', {'abonents': abonents}),
                                response_header=_('Search results'))

        else:
            return ajaxResponse(True, form=form)

    form = SearchAddressForm()
    return render(request, 'search/search_abonent.html', {'ssheader': _('Search by address'), 'submCaptrans': _('Find'),
                                                          'form': form})


def search_address(request):
    abonents = None
    form = SearchAddressForm()
    if request.method == 'GET':
        department = request.GET.get('department', 0)
        ul = force_unicode(request.GET.get('ul', ''))
        nd = force_unicode(request.GET.get('nd', ''))
        nkor = force_unicode(request.GET.get('nkor', ''))
        nkw = force_unicode(request.GET.get('nkw', ''))
        form.fields['department'].initial = department
        form.fields['ul'].initial = ul
        form.fields['nd'].initial = nd
        form.fields['nkor'].initial = nkor
        form.fields['nkw'].initial = nkw

        if SearchAddressForm(request.GET).is_valid():

        # department = form.cleaned_data['department'].id
            # ul = unicode(form.cleaned_data['ul']).upper() + "%"
            # nd = unicode(form.cleaned_data['nd']).upper()
            # nkor = unicode(form.cleaned_data['nkor']).upper()
            # nkw = unicode(form.cleaned_data['nkw']).upper()

            condits = ["department_id = %s", "upper(ul) like %s", "upper(nd) = %s"]
            params = [department, ul.upper() + "%", nd.upper()]

            if nkor:
                condits.append("upper(nkor) = %s")
                params.append(nkor.upper())
            if nkw:
                condits.append("upper(nkw) = %s")
                params.append(nkw.upper())

            abonents = Abonbaza.objects.extra(where=condits, params=params).order_by("nls")[:100]

    return render(request, 'search/search_abonent.html', {'ssheader': _('Search by address'),
                                                          'form': form, 'abonents': abonents, 'REQ_METHOD': 'GET'})


def ajax_search_fio(request):
    # abonents = None
    if request.method == 'POST' and request.is_ajax():
        form = SearchFioForm(request.POST)
        if form.is_valid():
            # Обработка
            # ...
            fio = request.POST.get('fio', '').upper() + '%'
            department = request.POST.get('department', 0)
            abonents = Abonbaza.objects.extra(where=["department_id = %s", "upper(fio) like %s"],
                                              params=[department, fio]).order_by("nls")[:100]

            return ajaxResponse(False, response=render_to_string('search/result_table.html', {'abonents': abonents}),
                                response_header=_('Search results'))
        else:
            return ajaxResponse(True, form=form)

    form = SearchFioForm()
    return render(request, 'search/search_abonent.html', {'ssheader': _('Search by surname'), 'submCaptrans': _('Find'),
                                                          'form': form})


def search_fio(request):
    abonents = None
    form = SearchFioForm()
    if request.method == 'GET':
        department = request.GET.get('department', 0)
        fio = force_unicode(request.GET.get('fio', ''))
        form.fields['department'].initial = department
        form.fields['fio'].initial = fio

        if SearchFioForm(request.GET).is_valid():
            # department = form.cleaned_data['department'].id
            # fio = unicode(form.cleaned_data['fio']).upper() + "%"
            abonents = Abonbaza.objects.extra(where=["department_id = %s", "upper(fio) like %s"],
                                              params=[department, fio.upper() + '%']).order_by("nls")[:100]

    return render(request, 'search/search_abonent.html', {'ssheader': _('Search by surname'),
                                                          'form': form, 'abonents': abonents, 'REQ_METHOD': 'GET'})


def getActualDate(dbtable, department):
    dates = ActualDate.objects.filter(dbtable=dbtable, department=department)
    if dates.count():
        return dates[0].actual_date
    else:
        return None


def first_day_of_next_month(dt):
    if not hasattr(dt, 'year'):
        return None
    next_month = (dt.month % 12) + 1
    return datetime.date(dt.year, next_month, 1)
    # - datetime.timedelta(days=1)


@login_required
def view_payment(request):
    user = request.user
    profile = get_profile(user)
    nls = profile.nls

    payments = Oplbaza.objects.extra(select={'year': "to_char(dat_kv, 'YY')", 'month': "to_char(dat_kv, 'MM')",
                                             'day': "to_char(dat_kv, 'DD')"}).filter(nls=nls)
    payments = payments.extra(order_by=['year', 'month', 'day'])

    actual_pay_date = None
    if payments.count():
        actual_pay_date = getActualDate("oplbaza", payments[0].department)

    dolg = 0
    actual_kvit_date = None
    # kvits = Kvitbaza.objects.extra(select={'year': "to_char(dat_kv, 'YY')", 'month': "to_char(dat_kv, 'MM')",
    #                                        'day': "to_char(dat_kv, 'DD')"}).filter(nls=nls)
    kvits = Kvitbaza.objects.filter(nls=nls).order_by('-god', '-nmes')

    # kvits = kvits.extra(where=["to_char(dat_kv, 'YY-MM')=%s"], params=[])
    # kvits = kvits.extra(order_by=['-year', '-month', '-day'])

    fizlica = is_fizlica(get_depid(profile.nls)) or is_fizlica_rayon(get_depid(profile.nls))
    urlica = is_ur_lica(get_depid(profile.nls))


    if kvits.count():
        if kvits[0].saldo_k:
            dolg += kvits[0].saldo_k
            # if kvits[0].saldoka:
        #     dolg += kvits[0].saldoka
        actual_kvit_date = getActualDate('kvitbaza', kvits[0].department)

    return render(request, 'data/view_payment.html',
                  {'nls':nls, 'payments': payments, 'dolg': dolg, 'actual_kvit_date': actual_kvit_date,
                   'actual_pay_date': actual_pay_date, 'fizlica': fizlica, 'urlica': urlica})


def render_recon_rep(nls):
    # reports = Kvitbaza.objects.extra(select={'year': "to_char(dat_kv, 'YY')", 'month': "to_char(dat_kv, 'MM')",
    #                                          'day': "to_char(dat_kv, 'DD')"}).filter(nls=nls)
    # reports = reports.extra(order_by=['year', 'month', 'day'])
    reports = Kvitbaza.objects.filter(nls=nls).order_by('god', 'nmes')
    # fiz_lica = is_fizlica(get_depid(nls))
    return render_to_string('data/recrep_shablon.html', {'reports': reports, })
    # 'fiz_lica': fiz_lica,


@login_required
def print_recon_rep(request):
    user = request.user
    nls = get_profile(user).nls
    reports_table = render_recon_rep(nls)
    return render(request, 'data/print_recon_rep.html', {'reports_table': reports_table})


@login_required
def recon_rep_page(request):
    user = request.user
    nls = get_profile(user).nls
    reports_table = render_recon_rep(nls)
    return render(request, 'data/recon_rep_page.html', {'nls':nls, 'reports_table': reports_table})


def render_kvit(nls):
    fio = get_fio(nls)
    address = get_address(nls)
    iin = get_iin(nls)
    kpp = get_kpp(nls)
    # kvits = Kvitbaza.objects.extra(select={'year': "to_char(dat_kv, 'YY')", 'month': "to_char(dat_kv, 'MM')",
    #                                        'day': "to_char(dat_kv, 'DD')"}).filter(nls=nls)
    # kvits = kvits.extra(order_by=['-year', '-month', '-day'])
    kvits = Kvitbaza.objects.filter(nls=nls).order_by('-god', '-nmes')

    dolg = 0

    if kvits.count():
        if kvits[0].saldo_k:
            dolg += kvits[0].saldo_k
            # if kvits[0].saldoka:
        #     dolg += kvits[0].saldoka

        kvit_date = getActualDate('kvitbaza', kvits[0].department)

        ur_lica = is_ur_lica(kvits[0].department.id)

        return render_to_string('data/kvit_table.html',
                                {'titles': [u'Хабарлама / Извещение', u'Түбіртек / Квитанция'], 'nls': nls, 'fio': fio,
                                 'address': address,
                                 'dolg': dolg, 'kvit_date': kvit_date, 'ur_lica': ur_lica, 'iin': iin, 'kpp': kpp})
    else:
        return ''


@login_required
def print_kvit(request):
    user = request.user
    nls = get_profile(user).nls
    kvitanciya = render_kvit(nls)
    if not kvitanciya:
        messages.add_message(request, messages.ERROR, _('Not found'))
        return HttpResponseRedirect(reverse('kvit_page'))
        # response = HttpResponse(mimetype='text/html')
    # response['Content-Disposition'] = 'attachment; filename=kvitanciya.html'
    # response.write(kvitanciya)
    # return response
    return render(request, 'data/print_kvit.html', {'kvitanciya': kvitanciya})


@login_required
def kvit_page(request):
    user = request.user
    nls = get_profile(user).nls
    kvitanciya = render_kvit(nls)
    if not kvitanciya:
        messages.add_message(request, messages.ERROR, _('Not found'))
        return HttpResponseRedirect(reverse('kvit_page'))
    return render(request, 'data/kvit_page.html', {'kvitanciya': kvitanciya})


@login_required
def contact_form(request):
    user = request.user
    if request.method == 'POST' and request.is_ajax():
        captcha_key, captcha_image = None, None
        form = ContactForm(request.POST)
        if form.is_valid():
            captcha_key = CaptchaStore.generate_key()
            captcha_image = captcha_image_url(captcha_key)
            subject = render_to_string('contact/subject.html')
            msg = render_to_string('contact/message.html',
                                   dict(user_name=user.username, user_email=user.email,
                                        tema=form.cleaned_data.get('subject'),
                                        user_message=form.cleaned_data.get('message'),
                                        default_email=settings.DEFAULT_FROM_EMAIL))

            #            email_count = request.session.get('email_sent', 0)
            #            if email_count >= 2:
            #                messages.add_message(request, messages.ERROR, _("Limit of sending mail exhausted"))
            #            else:
            try:
                emessg = EmailMessage(subject, msg, settings.DEFAULT_FROM_EMAIL, settings.DEFAULT_TO_EMAIL)
                #                emessg.content_subtype = "html"
                emessg.send()
                #                request.session['email_sent'] = email_count + 1
                # messages.add_message(request, messages.INFO, _('Message was sent. Thank you!'))
                return ajaxResponse(False, response_header=_('Message was sent. Thank you!'), captcha_key=captcha_key,
                                    captcha_image=captcha_image)
            except:
                return ajaxResponse(False, response_header=_('Error sending mail'), captcha_key=captcha_key,
                                    captcha_image=captcha_image)
                # messages.add_message(request, messages.ERROR, _('Error sending mail'))
                #return HttpResponseRedirect(reverse('contact_form'))
        else:
            if not form.errors.get('captcha'):
                captcha_key = CaptchaStore.generate_key()
                captcha_image = captcha_image_url(captcha_key)
            return ajaxResponse(True, form=form, captcha_key=captcha_key, captcha_image=captcha_image)

    form = ContactForm()
    trail = []
    menus = TopMenu.objects.filter(link=reverse('contact_form'))
    if menus.count():
        menu = menus[0].get_root()
        trail = [(reverse('list_submenus', args=[menu.id]), menu.title)]

    return render(request, 'contact/contact_form.html', {'form': form, 'trail': trail})


def site_comments(request):
    trail = []
    menus = TopMenu.objects.filter(link=reverse('comments'))
    if menus.count():
        menu = menus[0].get_root()
        trail = [(reverse('list_submenus', args=[menu.id]), menu.title)]
    return render(request, 'contact/comments.html', {'trail': trail})


def handle_uploaded_file(f, copyto):
    try:
        dbfFile = dbf.Dbf(f)
        result = dbfFile.recordCount
        destination = open(copyto, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
        dbfFile.close()
    except ValueError:
        result = -1
    return result


#def getDbfRecCount(fileName):
#    try:
#        dbfFile = dbf.Dbf(fileName)
#        result = dbfFile.recordCount
#        dbfFile.close()
#    except ValueError:
#        return -1
#    return result


@login_required
def upload_data(request):
    user = request.user
    if not user.has_perm('energosite.add_tables'):
        error = "У вас нет прав для добавления данных!"
        return render(request, 'load_data/data_error.html', {'error': error})

    #    DAYS = [(0, 'Все дни')] + [(rang, rang) for rang in range(1, 32)]
    MONTHS = [(0, 'Все месяцы')] + [(rang, str(rang)) for rang in range(1, 13)]
    YEARS = [(0, 'Все годы')] + [(rang, str(rang)) for rang in range(getYear() - 2, getYear() + 3)]

    if request.method == "POST":
        form = TablesForm(request.POST, request.FILES)
        form.fields['month'].choices, form.fields['month'].initial = MONTHS, getMonth()
        form.fields['year'].choices, form.fields['year'].initial = YEARS, getYear()
        form.fields['actual_date'].initial = getToday()
        if form.is_valid():
            dbtable = form.cleaned_data.get('dbtable')
            department = form.cleaned_data.get('department')
            charset = form.cleaned_data.get('charset')
            day = 0
            month = form.cleaned_data.get('month')
            year = form.cleaned_data.get('year')
            actual_date = form.cleaned_data.get("actual_date")
            dbfFileName = u"{0}_{1}_{2:0>2}{3:0>4}".format(dbtable, department.id, month, year) + ".dbf"
            dbfnumrecs = handle_uploaded_file(request.FILES['filename'],
                                              os.path.join(settings.UPLOAD_DATA_PATH, dbfFileName))
            if dbfnumrecs >= 0:
                messages.add_message(request, messages.SUCCESS,
                                     u"Файл - {0} ({1}) за {2:0>2}/{3:0>4} загружен".format(dbtable, department, month,
                                                                                            year))

                tabs = Tables.objects.filter(dbtable=dbtable, department=department, month=month, year=year)
                if tabs.count():
                    tabs[0].dbfnumrecs, tabs[0].charset, tabs[0].actual_date = dbfnumrecs, charset, actual_date
                    tabs[0].save()
                else:
                    Tables(dbtable=dbtable, department=department, filename=dbfFileName, dbfnumrecs=dbfnumrecs,
                           charset=charset, day=day, month=month, year=year, actual_date=actual_date).save()

                    #                datas = ActualDate.objects.filter(dbtable=dbtable, department=department)
                    #                if datas:
                    #                    datas[0].actual_date = actual_date
                    #                    datas[0].save()
                    #                else:
                    #                    ActualDate(dbtable=dbtable, department=department, actual_date=actual_date).save()
            else:
                messages.add_message(request, messages.ERROR,
                                     u"Файл {0} не DBF или испорчен".format(form.cleaned_data.get('filename')))
            return HttpResponseRedirect(reverse('upload_data'))
    else:
        form = TablesForm()
        form.fields['month'].choices, form.fields['month'].initial = MONTHS, getMonth()
        form.fields['year'].choices, form.fields['year'].initial = YEARS, getYear()
        form.fields['actual_date'].initial = getToday()
    tables = Tables.objects.order_by("department__name_ru", "dbtable", 'year', 'month', 'day')
    return render(request, 'load_data/upload_data.html', {'form': form, 'tables': tables})


@login_required
def delete_loaded(request, item_id):
    user = request.user
    if not user.has_perm('energosite.delete_tables'):
        error = "У вас нет прав для удаления данных!"
        return render(request, 'load_data/data_error.html', {'error': error})
    tabs = Tables.objects.filter(pk=item_id)
    if tabs.count():
        messages.add_message(request, messages.INFO, u"Файл {0} удалён".format(tabs[0].filename))
        tabs[0].delete()
    return HttpResponseRedirect(reverse('upload_data'))

##############################################################

def resend_activation_link(request):
    if Site._meta.installed:
        site = Site.objects.get_current()
    else:
        site = RequestSite(request)

    if request.method == 'POST':
        form = ResendActivationEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            #            print email
            users = User.objects.filter(email=email, is_active=False)

            if not users.count():
                form._errors["email"] = (_("Account for email address is not registered or already activated."),)
            else:
                for user in users:
                    for profile in RegistrationProfile.objects.filter(user=user):
                        if profile.activation_key_expired():
                            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
                            profile.activation_key = hashlib.sha1(salt + user.username).hexdigest()
                            profile.save()
                            user.date_joined = timezone.now()
                            user.save()
                        profile.send_activation_email(site)

                messages.add_message(request, messages.INFO, _('Resend activation link done'))
                return HttpResponseRedirect(reverse('home'))

    else:
        form = ResendActivationEmailForm()

    return render(request, "registration/resend_activation_email_form.html", {"form": form})


def login(request, template_name='registration/login.html'):
    form = AuthenticationForm(data=request.POST)

    if request.method == "POST":
        if not form.is_valid():
            non_field_errors = form.non_field_errors()

            if non_field_errors:
            # test if the account is not active
                user_inactive = non_field_errors[0].find(_("This account is inactive.")) != -1
                #                user_inactive = User.objects.filter(username=request.POST.get('username'), is_active=0).count() == 1

                if user_inactive:
                    return render(request, template_name, {'form': form, 'user_inactive': user_inactive, })

    return django_login(request)















