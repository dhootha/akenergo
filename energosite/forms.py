# -*- coding: utf-8 -*-
from registration.forms import RegistrationFormUniqueEmail
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms import ModelForm
import os
from models import Abonbaza, MeterReading, Department, UserProfile
from registration.signals import user_registered, user_activated
from django.contrib.auth import login
from captcha.fields import CaptchaField


def check_nls(obj):
    ls = obj.cleaned_data.get('nls')
    count = Abonbaza.objects.filter(nls=ls).count()
    if not count or int(ls) == 0:
        raise forms.ValidationError(_(u"Incorrect personal number"))
    return ls


class EditProfileForm(forms.Form):
    nls = forms.DecimalField(max_digits=7, decimal_places=0, required=True, label=_(u'Personal number'))
    home_phone = forms.CharField(required=False, min_length=10, max_length=10, label=_('Home phone'))
    mobile_phone = forms.CharField(required=False, min_length=10, max_length=10, label=_('Mobile phone'))
    mailing = forms.BooleanField(required=False, initial=True, label=_('I agree to receive newsletter'))
    #    first_name = forms.CharField(max_length=100, required=False, label=_(u'First name'),
    #        widget=forms.TextInput(attrs={'size': '45'}))
    #    last_name = forms.CharField(max_length=100, required=False, label=_(u'Last name'),
    #        widget=forms.TextInput(attrs={'size': '45'}))

    #    password = forms.CharField(label=_(u'Current password'), widget=forms.PasswordInput)
    # email = forms.EmailField(required=True, label=_(u'E-mail address'))

    #    def __init__(self, user, *args, **kwargs):
    #        super(EditProfileForm, self).__init__(*args, **kwargs)
    #        self.user = user

    def clean_nls(self):
        return check_nls(self)

    def clean_home_phone(self):
        val = self.cleaned_data['home_phone']
        if val:
            try:
                int(val)
            except ValueError:
                raise forms.ValidationError(_(u"Incorrect information"))
        return val

    def clean_mobile_phone(self):
        val = self.cleaned_data['mobile_phone']
        if val:
            try:
                int(val)
            except ValueError:
                raise forms.ValidationError(_(u"Incorrect information"))
        return val

#    def clean_password(self):
#        password = self.cleaned_data["password"]
#        if self.user and not self.user.check_password(password):
#            raise forms.ValidationError(_(u"Password incorrect"))
#        return password


class MyRegistrationForm(RegistrationFormUniqueEmail):
#    def __init__(self, *args, **kwargs):
#        super(MyRegistrationForm, self).__init__(*args, **kwargs)
#        self.fields['username'].label=_(u'Username')
#        self.fields['email'].label=_(u'E-mail')
#        self.fields['password1'].label=_("Password")
#        self.fields['password2'].label=_("Password (again)")

    nls = forms.DecimalField(max_digits=7, decimal_places=0, required=True, label=_(u'Personal number'))
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
                raise forms.ValidationError(_(u"Incorrect information"))
        return val

    def clean_mobile_phone(self):
        val = self.cleaned_data['mobile_phone']
        if val:
            try:
                int(val)
            except ValueError:
                raise forms.ValidationError(_(u"Incorrect information"))
        return val

# Сигналы
def create_user_profile(sender, user, request, **kwargs):
#    print 'creating profile \n'
#    form = MyRegistrationForm(request.POST)
    try:
        UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=user, nls=request.POST.get('nls'),
            mailing=request.POST.get('mailing', False),
            home_phone=request.POST.get('home_phone'), mobile_phone=request.POST.get('mobile_phone'),)

user_registered.connect(create_user_profile)

def login_on_activation(sender, user, request, **kwargs):
#    print 'login profile \n'
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)

user_activated.connect(login_on_activation)


class MeterReadingForm(ModelForm):
    class Meta:
        model = MeterReading

    #    fio = forms.CharField(max_length=255, label=_('Client name'), widget=forms.TextInput(attrs={'size': '50'}))
    #    address = forms.CharField(max_length=255, label=_('Address'), widget=forms.TextInput(attrs={'size': '50'}))

    date = forms.CharField(widget=forms.HiddenInput)
    CHOICES = (('one-tariff', _('one-tariff')), ('two-tariff', _('two-tariff')))
    tariff = forms.ChoiceField(label=_("Counter type"), initial='one-tariff', choices=CHOICES)

    def clean_nls(self):
        ls = self.cleaned_data.get('nls')
        abons = Abonbaza.objects.filter(nls=ls)
        if not abons.count() or int(ls) == 0:
            raise forms.ValidationError(_(u"Incorrect personal number"))
        elif abons[0].department.id == 2:
            raise forms.ValidationError(_(u"You don't have permission's") + '!!!')
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


from captcha.fields import CaptchaField

class ContactForm(forms.Form):
#username = forms.CharField(max_length=50, label=_('Username'))

    # CHOICES = ((_('Question'), _('Question')), (_('Proposal'), _('Proposal')), (_('Gratitude'), _('Gratitude')))
    subject = forms.CharField(max_length=128, label=_('Subject'))
    message = forms.CharField(max_length=512, widget=forms.widgets.Textarea(attrs={'rows': '9'}), label=_('Message'))
    captcha = CaptchaField(label=_('Captcha'))

    #attrs={'cols': '60', 'rows': '5'}


    def clean_subject(self):
        subject = self.cleaned_data['subject']
        if not subject.strip().__len__():
            raise forms.ValidationError(_(u"Incorrect information"))
        return subject


    def clean_message(self):
        message = self.cleaned_data['message']
        if not message.strip().__len__():
            raise forms.ValidationError(_(u"Incorrect information"))
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

    #    def clean(self):
    #        cleaned_data = super(TablesForm, self).clean()
    #        year, month, day = int(cleaned_data.get('year')), int(cleaned_data.get('month')), int(cleaned_data.get('day'))
    #        if day and month and year:
    #            try:
    #                date = datetime.date(year, month, day)
    #            except ValueError:
    #                raise forms.ValidationError('{0}.{1}.{2} - Неправильная дата!'.format(day, month, year))
    #        return cleaned_data

    def clean_filename(self):
        data = self.cleaned_data['filename']
        if not str(data).lower().endswith(".dbf"):
            raise forms.ValidationError("Файл " + os.path.basename(str(data)) + " - не dbf")
        return data

#############################3
class ResendActivationEmailForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(maxlength=75)), label=_("E-mail"))
    captcha = CaptchaField(label=_('Captcha'))


