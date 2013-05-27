from django.conf.urls import patterns, include, url
from django.contrib import admin
from energosite.forms import MyRegistrationForm
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

admin.autodiscover()

from django.views.generic.base import TemplateView
from energosite.models import Page, Article
from django.contrib.sitemaps import GenericSitemap


page_dict = {
    'queryset': Page.objects.filter(published=True),
    'date_field': 'date',
}

article_dict = {
    'queryset': Article.objects.filter(published=True),
    'date_field': 'date',
}

sitemaps = {
    'pages': GenericSitemap(page_dict, priority=0.5, changefreq='daily'),
    'articles': GenericSitemap(article_dict, priority=0.5, changefreq='daily'),
}

urlpatterns = patterns('',
    # url(r'^$', TemplateView.as_view(template_name='posts/index.html'), name='home'),
    url(r'^$', 'energosite.views.index', name='home'),
    url(r'^page/(?P<link>.+)/$', 'energosite.views.show_page', name='show_page'),
    url(r'^article/(?P<link_id>\d+)/$', 'energosite.views.show_article', name='show_article'),
    url(r'^list_submenus/(?P<menu_id>\d+)/$', 'energosite.views.list_submenus', name='list_submenus'),
    url(r'^news_list/$', 'energosite.views.news_list', name='news_list'),

    url(r'^meter_reading/input/$', 'energosite.views.meter_reading', name='meter_reading'),
    url(r'^meter_reading/load/$', 'energosite.views.load_reading', name='load_reading'),

    url(r'^search/fio/$', 'energosite.views.search_fio', name='search_fio'),
    url(r'^search/address/$', 'energosite.views.search_address', name='search_address'),
#    url(r'^search/results/$',  TemplateView.as_view(template_name='search/search_results.html'), name='search_results'),

    url(r'^search/google/$', TemplateView.as_view(template_name='search/google_search.html'), name='google_search'),

    url(r'^data/view_payment/$', 'energosite.views.view_payment', name='view_payment'),

    url(r'^data/view_debtors/(?P<kod>\d+)/$', 'energosite.views.view_debtors', name='view_debtors'),

    # url(r'^data/kvit_page/$', TemplateView.as_view(template_name='data/kvit_page.html'), name='kvit_page'),
    url(r'^data/kvit_page/$', 'energosite.views.kvit_page', name='kvit_page'),
    url(r'^data/print_kvit/$', 'energosite.views.print_kvit', name='print_kvit'),

    url(r'^data/recon_rep_page/$', 'energosite.views.recon_rep_page', name='recon_rep_page'),
    url(r'^data/print_recon_rep/$', 'energosite.views.print_recon_rep', name='print_recon_rep'),

    url(r'^contact/form/$', 'energosite.views.contact_form', name='contact_form'),
    url(r'^contact/comments/$', 'energosite.views.site_comments', name='comments'),


    url(r'^upload_data/$', 'energosite.views.upload_data', name='upload_data'),
    url(r'^delete_loaded/(?P<item_id>\d+)/$', 'energosite.views.delete_loaded', name='delete_loaded'),

    url(r'^users_statistics/$', login_required(TemplateView.as_view(template_name='statistics/users.html')),
        name='users_statistics'),


    # url(r'^prodject/', include('prodject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
#    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
#    url(r'^i18n/set_language/$', 'energosite.views.set_language', name='set_language'),


    url(r'^users/my_profile/$', 'energosite.views.edit_profile', name='edit_profile'),
    url(r'^accounts/login/$', 'energosite.views.login', {'template_name': 'registration/login.html'},
        name='auth_login'),
    url(r'^accounts/register/$', 'registration.views.register',
        {'backend': 'registration.backends.default.DefaultBackend', 'form_class': MyRegistrationForm, },
        name='registration_register'),
    url(r'^accounts/activate/resend/$', 'energosite.views.resend_activation_link', name='resend_activation_link'),
    url(r'^accounts/', include('registration.backends.default.urls')),

    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}, name='sitemap'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^ckeditor/', include('ckeditor.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
