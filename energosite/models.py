# -*- coding: utf-8 -*-
#from lxml.html._diffcommand import description
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

# User = get_user_model()
from django.utils import translation
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField


#########################################################
class Department(models.Model):
    name_ru = models.CharField(max_length=100, blank=True, null=True)
    name_kk = models.CharField(max_length=100, blank=True, null=True)

    @property
    def name(self):
        return getattr(self, u"name_{0}".format(translation.get_language()[:2])) or self.name_ru

    def __unicode__(self):
        return self.name_ru

    class Meta:
        ordering = ['name_ru']


class Abonbaza(models.Model):
    nls = models.DecimalField(max_digits=7, decimal_places=0, db_index=True)
    fio = models.CharField(max_length=100)
    ul = models.CharField(max_length=100)
    nd = models.CharField(max_length=25)
    nkor = models.CharField(max_length=25, blank=True, null=True)
    nkw = models.CharField(max_length=25, blank=True, null=True)

    iin = models.CharField(max_length=25, blank=True, null=True)
    kpp = models.CharField(max_length=25, blank=True, null=True)
    kod = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)

    department = models.ForeignKey(Department)

    # class Meta:
    #     db_table = 'abonbaza'

    def __unicode__(self):
        return str(self.nls)


class Kvitbaza(models.Model):
    nls = models.DecimalField(max_digits=7, decimal_places=0, db_index=True)

    kol_lim = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)

    tar = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)

    n_pok = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)
    k_pok = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)
    n_pok2 = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)
    k_pok2 = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)
    n_pok3 = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)
    k_pok3 = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)


    tar1 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    tar2 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    tar3 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    potr1 = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)
    potr2 = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)
    potr3 = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)
    potr = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)

    sum_nach1 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    sum_nach2 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    sum_nach3 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    sum_nach = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    sum_act = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    opl = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    # saldo_n = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    saldo_k = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    # saldoka = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    # dat_kv = models.DateField(blank=True, null=True)
    nmes = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    god = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)

    department = models.ForeignKey(Department)

    # class Meta:
    #     db_table = 'kvitbaza'

    def __unicode__(self):
        return str(self.nls)


class Oplbaza(models.Model):
    nls = models.DecimalField(max_digits=7, decimal_places=0, db_index=True)
    opl = models.DecimalField(max_digits=12, decimal_places=2)
    dat_kv = models.DateField(blank=True, null=True)
    data = models.DateField(blank=True, null=True)
    department = models.ForeignKey(Department)

    # class Meta:
    #     db_table = 'oplbaza'

    def __unicode__(self):
        return str(self.nls)


class Tables(models.Model):
    filename = models.CharField(max_length=100)
    dbfnumrecs = models.IntegerField(default=0)
    dbtable = models.CharField(max_length=100)
    charset = models.CharField(max_length=25)
    day = models.DecimalField(max_digits=2, decimal_places=0)
    month = models.DecimalField(max_digits=2, decimal_places=0)
    year = models.DecimalField(max_digits=4, decimal_places=0)
    actual_date = models.DateField()
    department = models.ForeignKey(Department)

    # class Meta:
    #     db_table = 'tables'


class Debtors(models.Model):
    #nls = models.ForeignKey(Abonbaza, db_column='nls', to_field='nls')
    nls = models.DecimalField(max_digits=7, decimal_places=0, db_index=True)
    dolg = models.DecimalField(max_digits=12, decimal_places=2)
    department = models.ForeignKey(Department)

    # class Meta:
    #     db_table = 'debtors'

        #        permissions = (("view_debuch", "Can see available debtors"),)

    def __unicode__(self):
        return str(self.nls)

#########################################################

class MeterReading(models.Model):
    nls = models.DecimalField(_('Personal number'), max_digits=7, decimal_places=0, db_index=True)
    fio = models.CharField(_('Client name'), max_length=255, db_index=True)
    address = models.CharField(_('Address'), max_length=255)
    pok1 = models.DecimalField(_('Day reading'), max_digits=7, decimal_places=0)
    pok2 = models.DecimalField(_('Night reading'), max_digits=7, decimal_places=0, blank=True, null=True)
    pok3 = models.DecimalField(_('Evening reading'), max_digits=7, decimal_places=0, blank=True, null=True)
    date = models.DateTimeField('Date')

    class Meta:
        permissions = (("view_meter_reading", "Can see available meter Reading"),)

##################################################

#class UploadCategory(models.Model):
#    title = models.CharField(max_length=255)
#    directory = models.SlugField(max_length=255, unique=True)
#
#
#    def __unicode__(self):
#        return  u"%s - %s" % (self.title, self.directory)
#
#    class Meta:
#        ordering = ['directory', ]
#
#
#def make_upload_path(instance, filename):
#    """Generates upload path for FileField"""
#    return u"uploads/%s/%s" % (instance.category.directory, filename)
#
#
#class Upload(models.Model):
#    category = models.ForeignKey(UploadCategory)
#    title_ru = models.CharField(max_length=255)
#    title_kk = models.CharField(max_length=255, null=True, blank=True)
#    description_ru = models.CharField(max_length=255, blank=True, null=True)
#    description_kk = models.CharField(max_length=255, blank=True, null=True)
#    file_ru = models.FileField(upload_to=make_upload_path, max_length=255)
#    file_kk = models.FileField(upload_to=make_upload_path, max_length=255, null=True, blank=True)
#
#    def __unicode__(self):
#        return  u"%s - %s" % (self.file_ru.name, self.category.title)
#
#    class Meta:
#        ordering = ['category__title', 'title_ru']
#
#    @property
#    def title(self):
#        return getattr(self, u"title_{0}".format(translation.get_language()[:2])) or self.title_ru
#
#    @property
#    def description(self):
#        return getattr(self, u"description_{0}".format(translation.get_language()[:2])) or self.description_ru
#
#    @property
#    def file(self):
#        return getattr(self, u"file_{0}".format(translation.get_language()[:2])) or self.file_ru
#
#
#    def clean(self):
#        if (not self.title_ru) and (not self.title_kk):
#            raise ValidationError('You must set title!!!')


class Page(models.Model):
    title_ru = models.CharField(max_length=255, null=True, blank=True)
    title_kk = models.CharField(max_length=255, null=True, blank=True)
    title_en = models.CharField(max_length=255, null=True, blank=True)
    link = models.SlugField(max_length=255, unique=True, db_index=True)
    content_ru = RichTextField(null=True, blank=True)
    content_kk = RichTextField(null=True, blank=True)
    content_en = RichTextField(null=True, blank=True)
    #    upload = models.ManyToManyField(to=Upload, null=True, blank=True)
    date = models.DateTimeField(default=datetime.datetime.now)
    published = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title_ru

    class Meta:
        ordering = ['title_ru']

    @property
    def title(self):
        return getattr(self, u"title_{0}".format(translation.get_language()[:2])) or self.title_ru

    @property
    def content(self):
        return getattr(self, u"content_{0}".format(translation.get_language()[:2])) or self.content_ru


    @models.permalink
    def get_absolute_url(self):
        return 'show_page', [self.link]


from django.utils.text import Truncator

class Article(models.Model):
    TYPES = [(1, 'news'), (2, 'vacancy')]
    tip = models.IntegerField(choices=TYPES, default=1)
    title_ru = models.CharField(max_length=255, null=True, blank=True)
    title_kk = models.CharField(max_length=255, null=True, blank=True)
    title_en = models.CharField(max_length=255, null=True, blank=True)
    content_ru = RichTextField(null=True, blank=True)
    content_kk = RichTextField(null=True, blank=True)
    content_en = RichTextField(null=True, blank=True)
    #    upload = models.ManyToManyField(to=Upload, null=True, blank=True)
    date = models.DateTimeField(default=datetime.datetime.now, db_index=True)
    published = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title_ru

    class Meta:
        ordering = ['tip', '-date']

    @property
    def title(self):
        return getattr(self, u"title_{0}".format(translation.get_language()[:2])) or self.title_ru

    @property
    def content(self):
        return getattr(self, u"content_{0}".format(translation.get_language()[:2])) or self.content_ru

    @property
    def summary(self):
        # return text.truncate_html_words(self.content, settings.MAX_ARTICLE_LENGTH)
        return Truncator(self.content).words(settings.MAX_ARTICLE_LENGTH, truncate='...', html=True)

    @models.permalink
    def get_absolute_url(self):
        return 'show_article', [self.id]


class TopMenu(MPTTModel):
    title_ru = models.CharField(max_length=255, null=True, blank=True)
    title_kk = models.CharField(max_length=255, null=True, blank=True)
    title_en = models.CharField(max_length=255, null=True, blank=True)
    link = models.CharField(max_length=255, blank=True, null=True)
    page = models.ForeignKey(Page, blank=True, null=True)
    order = models.IntegerField(default=0)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    published = models.BooleanField(default=True)

    @property
    def title(self):
        return getattr(self, u"title_{0}".format(translation.get_language()[:2])) or self.title_ru

    @property
    def title_cut(self):
        return self.title[:15]

    def clean(self):
        if (self.link.strip() == '') and (not self.page):
            raise ValidationError('You must set link or page')
        if (self.link.strip() != '') and self.page:
            raise ValidationError('You must set only link or page')

    def __unicode__(self):
        return self.title_ru

    class MPTTMeta:
        order_insertion_by = ['order']

    def get_absolute_url(self):
        if self.link.strip() != '':
            return self.link
        elif self.page:
            return self.page.get_absolute_url()
        else:
            return '#'

    def save(self, force_insert=False, force_update=False, using=None):
        super(TopMenu, self).save()
        TopMenu.objects.rebuild()



class UserProfile(models.Model):
#    user = models.ForeignKey(settings.AUTH_USER_MODEL, unique=True, related_name='profiles')
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    nls = models.DecimalField(_('Personal number'), max_digits=7, decimal_places=0, default=0)
    mobile_phone = models.CharField(blank=True, null=True, max_length=25)
    home_phone = models.CharField(blank=True, null=True, max_length=25)
    mailing = models.BooleanField(_('I agree to receive newsletter'), default=True)

    def __unicode__(self):
        return u"{0} - {1}".format(self.user.username, self.nls)


class ActualDate(models.Model):
    dbtable = models.CharField(max_length=100)
    actual_date = models.DateField()
    department = models.ForeignKey(Department)

    class Meta:
        unique_together = (('dbtable', 'department'),)


class Mailing_List(models.Model):
#    CHOICES = ((1, 'Квитанция'), (2, 'Новость'))
    kvit = models.BooleanField('Квитанция', default=False)
    subject = models.CharField('Тема', max_length=255)
    content = RichTextField('Содержимое')
    date = models.DateTimeField('Дата', auto_now=True)

    def __unicode__(self):
        return self.subject

    class Meta:
        ordering = ['-date']
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
