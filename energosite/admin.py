# -*- coding: utf-8 -*-
from models import *
from django.contrib import admin
from mptt.admin import MPTTModelAdmin



#admin.site.register(Upload)
#
#class UploadCategoryInline(admin.TabularInline):
#    model = Upload
#    extra = 3
#
#class UploadCategoryAdmin(admin.ModelAdmin):
#    #list_display = ['title_ru', 'title_kk', 'link', 'published', 'order']
#    #search_fields = ['title_ru',]
#    #prepopulated_fields = {'link': ['title_ru']}
#
#    inlines = (UploadCategoryInline,)
#
#admin.site.register(UploadCategory, UploadCategoryAdmin)

class PageAdmin(admin.ModelAdmin):
    list_display = ('title_ru', 'title_kk', 'link', 'date', 'published', 'order')
    search_fields = ('title_ru',)
    prepopulated_fields = {'link': ['title_ru']}
    #    filter_horizontal = ("upload",)

    # class Media:
    #     js = ('js/tiny_mce/tiny_mce.js', 'js/tiny_mce/textareas.js',)

admin.site.register(Page, PageAdmin)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title_ru', 'title_kk', 'tip', 'date', 'published')
    search_fields = ('title_ru',)
    #    filter_horizontal = ("upload",)
    # class Media:
    #     js = ('js/tiny_mce/tiny_mce.js', 'js/tiny_mce/textareas.js',)

admin.site.register(Article, ArticleAdmin)

# admin.site.register(UserProfile)

admin.site.register(Department)

#admin.site.register(Debtors)


class TopMenuInline(admin.TabularInline):
    model = TopMenu
    extra = 3


class TopMenuAdmin(MPTTModelAdmin):
    list_display = ['title_ru', 'title_kk', 'link', 'published', 'order']
    search_fields = ['title_ru', ]
    prepopulated_fields = {'link': ['title_ru']}

    inlines = (TopMenuInline,)
    mptt_level_indent = 15

admin.site.register(TopMenu, TopMenuAdmin)

from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.admin import UserAdmin
from energosite.models import UserProfile
#from django.db.models import Q

admin.site.unregister(User)


class UserProfileInline(admin.StackedInline):
    model = UserProfile


class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline, ]
    list_display = UserAdmin.list_display + ('nls',)
    search_fields = UserAdmin.search_fields + ('userprofile__nls',)

    def nls(self, obj):
        try:
            return obj.userprofile.nls
        except UserProfile.DoesNotExist:
            return ''

            #    def queryset(self, request):
            #        qs = super(UserAdmin, self).queryset(request)
            #        qs = qs.filter(Q(is_staff=True) | Q(is_superuser=True))
            #        return qs

admin.site.register(User, UserProfileAdmin)


class MailListAdmin(admin.ModelAdmin):
    list_display = ('subject', 'kvit', 'date',)

    # class Media:
    #     js = ('js/tiny_mce/tiny_mce.js', 'js/tiny_mce/textareas.js',)


admin.site.register(Mailing_List, MailListAdmin)