# -*- coding: utf-8 -*-
import os

from registration.forms import RegistrationFormUniqueEmail
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms import ModelForm
from registration.signals import user_registered, user_activated
from django.contrib.auth import login
from captcha.fields import CaptchaField

from models import Abonbaza, MeterReading, Department, UserProfile


def check_nls(obj):
    ls = obj.cleaned_data.get('nls')
    count = Abonbaza.objects.filter(nls=ls).count()
    if not count or int(ls) == 0:
        raise forms.ValidationError(_("Incorrect personal number"))
    return ls


class EditProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('nls', 'home_phone', 'mobile_phone', 'mailing')
    home_phone = forms.CharField(required=False, min_length=10, max_length=10, label=_('Home phone'))
    mobile_phone = forms.CharField(required=False, min_length=10, max_length=10, label=_('Mobile phone'))
    #mailing = forms.BooleanField(required=False, initial=True, label=_('I agree to receive newsletter'))

    def clean_nls(self):
        return check_nls(self)

    def clean_home_phone(self):
        val = self.cleaned_data['home_phone']
        if val:
            try:
                int(val)
            except ValueError:
                raise forms.ValidationError(_("Incorrect information"))
        return val

    def clean_mobile_phone(self):
        val = self.cleaned_data['mobile_phone']
        if val:
            try:
                int(val)
            except ValueError:
                raise forms.ValidationError(_("Incorrect information"))
        return val


class MyRegistrationForm(RegistrationFormUniqueEmail):
    nls = forms.DecimalField(max_digits=7, decimal_places=0, required=True, label=_('Personal number'))
    home_phone = forms.CharField(required=False, min_length=10, max_length=10, label=_('Home phone'))
    mobile_phone = forms.CharField(required=False, min_length=10, max_length=10, label=_('Mobile phone'))
    mailing = forms.BooleanField(required=False, initial=True, label=_('I agree to receive newsletter'))
    captcha = CaptchaField(label=_('Captcha'))

    def clean_nls(self):
        return check_nls(self)

    def clean_home_phone(self):
        val = self.cleaned_data['home_phone']
        if val:
            try:
                int(val)
            except ValueError:
                raise forms.ValidationError(_("Incorrect information"))
        return val

    def clean_mobile_phone(self):
        val = self.cleaned_data['mobile_phone']
        if val:
            try:
                int(val)
            except ValueError:
                raise forms.ValidationError(_("Incorrect information"))
        return val

# Сигналы
def create_user_profile(sender, user, request, **kwargs):
#    print 'creating profile \n'
    try:
        UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=user, nls=request.POST.get('nls'),
                                   mailing=request.POST.get('mailing', False),
                                   home_phone=request.POST.get('home_phone'),
                                   mobile_phone=request.POST.get('mobile_phone'), )


user_registered.connect(create_user_profile)


def login_on_activation(sender, user, request, **kwargs):
#    print 'login profile \n'
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)


user_activated.connect(login_on_activation)


class MeterReadingForm(ModelForm):
    class Meta:
        model = MeterReading
        fields = ('nls', 'fio', 'address', 'pok1', 'pok2', 'pok3', 'date')
        widgets = {
            'date': forms.HiddenInput(),
        }
    # date = forms.CharField(widget=forms.HiddenInput)
    CHOICES = (('one-tariff', _('one-tariff')), ('two-tariff', _('two-tariff')))
    tariff = forms.ChoiceField(label=_("Counter type"), initial='one-tariff', choices=CHOICES)

    def clean_nls(self):
        ls = self.cleaned_data.get('nls')
        abons = Abonbaza.objects.filter(nls=ls)
        if not abons.count() or int(ls) == 0:
            raise forms.ValidationError(_("Incorrect personal number"))
        elif abons[0].department.id == 2:
            raise forms.ValidationError(_("You don't have permission's") + '!!!')
        return ls


class LoadReading(forms.Form):
    CHARSET_CHOICES = (('cp866', 'DOS'), ('cp1251', 'ANSI' ))
    month = forms.ChoiceField(label="Месяц")
    year = forms.ChoiceField(label="Год")
    charset = forms.ChoiceField(label="Кодировка DBF", initial="cp866", choices=CHARSET_CHOICES)


class SearchAddressForm(forms.Form):
    department = forms.ModelChoiceField(queryset=Department.objects.all().order_by("name_ru"), label=_('Department'))
    ul = forms.CharField(min_length=3, max_length=100, label=_('Street'))
    nd = forms.CharField(max_length=25, label=_('House number'))
    nkor = forms.CharField(max_length=25, required=False, label=_('Corps'))
    nkw = forms.CharField(max_length=25, required=False, label=_('Apartment'))


class SearchFioForm(forms.Form):
    department = forms.ModelChoiceField(queryset=Department.objects.all().order_by("name_ru"), label=_('Department'))
    fio = forms.CharField(min_length=3, max_length=100, label=_('Client name'))


class ContactForm(forms.Form):
    # CHOICES = ((_('Question'), _('Question')), (_('Proposal'), _('Proposal')), (_('Gratitude'), _('Gratitude')))
    subject = forms.CharField(max_length=128, label=_('Subject'))
    message = forms.CharField(max_length=512, widget=forms.widgets.Textarea(attrs={'rows': '9'}), label=_('Message'))
    captcha = CaptchaField(label=_('Captcha'))
    #attrs={'cols': '60', 'rows': '5'}

    def clean_subject(self):
        subject = self.cleaned_data['subject']
        if not subject.strip().__len__():
            raise forms.ValidationError(_("Incorrect information"))
        return subject


    def clean_message(self):
        message = self.cleaned_data['message']
        if not message.strip().__len__():
            raise forms.ValidationError(_("Incorrect information"))
        return message


class TablesForm(forms.Form):
    DB_CHOICES = (('', '---------'), ('oplbaza', 'Оплата (oplbaza)'), ('abonbaza', 'Абоненты (abonbaza)'),
                  ('kvitbaza', 'Квитанции (kvitbaza)'), ('debtors', 'Дебиторы (debtors)'),)
    CHARSET_CHOICES = (( 'cp866', 'DOS'), ('cp1251', 'ANSI' ))
    department = forms.ModelChoiceField(label="Отделение", queryset=Department.objects.order_by('name_ru'))
    dbtable = forms.ChoiceField(label="База", choices=DB_CHOICES, initial='oplbaza')
    #widget=forms.widgets.FileInput(attrs={'size': 40})
    filename = forms.FileField(label="Файл данных")
    charset = forms.ChoiceField(label="Кодировка файла", choices=CHARSET_CHOICES, initial="cp866")
    #    day = forms.ChoiceField(label="День", choices=DAYS, initial=getDay)
    month = forms.ChoiceField(label="Месяц")
    year = forms.ChoiceField(label="Год")
    actual_date = forms.DateField(label="Актуальная дата", input_formats=('%d.%m.%Y', '%d.%m.%y', '%Y-%m-%d',))


    def clean_filename(self):
        data = self.cleaned_data['filename']
        if not str(data).lower().endswith(".dbf"):
            raise forms.ValidationError("Файл " + os.path.basename(str(data)) + " - не dbf")
        return data

#############################3
class ResendActivationEmailForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(maxlength=75)), label=_("E-mail"))
    captcha = CaptchaField(label=_('Captcha'))


