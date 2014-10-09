# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import ckeditor.fields
import mptt.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Abonbaza',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nls', models.DecimalField(max_digits=7, decimal_places=0, db_index=True)),
                ('fio', models.CharField(max_length=100)),
                ('ul', models.CharField(max_length=100)),
                ('nd', models.CharField(max_length=25)),
                ('nkor', models.CharField(max_length=25, null=True, blank=True)),
                ('nkw', models.CharField(max_length=25, null=True, blank=True)),
                ('iin', models.CharField(max_length=25, null=True, blank=True)),
                ('kpp', models.CharField(max_length=25, null=True, blank=True)),
                ('kod', models.DecimalField(null=True, max_digits=4, decimal_places=0, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ActualDate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dbtable', models.CharField(max_length=100)),
                ('actual_date', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tip', models.IntegerField(default=1, choices=[(1, b'news'), (2, b'vacancy')])),
                ('title_ru', models.CharField(max_length=255, null=True, blank=True)),
                ('title_kk', models.CharField(max_length=255, null=True, blank=True)),
                ('title_en', models.CharField(max_length=255, null=True, blank=True)),
                ('content_ru', ckeditor.fields.RichTextField(null=True, blank=True)),
                ('content_kk', ckeditor.fields.RichTextField(null=True, blank=True)),
                ('content_en', ckeditor.fields.RichTextField(null=True, blank=True)),
                ('date', models.DateTimeField(default=datetime.datetime.now, db_index=True)),
                ('published', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['tip', '-date'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Debtors',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nls', models.DecimalField(max_digits=7, decimal_places=0, db_index=True)),
                ('dolg', models.DecimalField(max_digits=12, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_ru', models.CharField(max_length=100, null=True, blank=True)),
                ('name_kk', models.CharField(max_length=100, null=True, blank=True)),
            ],
            options={
                'ordering': ['name_ru'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Kvitbaza',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nls', models.DecimalField(max_digits=7, decimal_places=0, db_index=True)),
                ('kol_lim', models.DecimalField(null=True, max_digits=3, decimal_places=0, blank=True)),
                ('tar', models.DecimalField(null=True, max_digits=2, decimal_places=0, blank=True)),
                ('n_pok', models.DecimalField(null=True, max_digits=7, decimal_places=0, blank=True)),
                ('k_pok', models.DecimalField(null=True, max_digits=7, decimal_places=0, blank=True)),
                ('n_pok2', models.DecimalField(null=True, max_digits=7, decimal_places=0, blank=True)),
                ('k_pok2', models.DecimalField(null=True, max_digits=7, decimal_places=0, blank=True)),
                ('n_pok3', models.DecimalField(null=True, max_digits=7, decimal_places=0, blank=True)),
                ('k_pok3', models.DecimalField(null=True, max_digits=7, decimal_places=0, blank=True)),
                ('tar1', models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)),
                ('tar2', models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)),
                ('tar3', models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)),
                ('potr1', models.DecimalField(null=True, max_digits=7, decimal_places=0, blank=True)),
                ('potr2', models.DecimalField(null=True, max_digits=7, decimal_places=0, blank=True)),
                ('potr3', models.DecimalField(null=True, max_digits=7, decimal_places=0, blank=True)),
                ('potr', models.DecimalField(null=True, max_digits=7, decimal_places=0, blank=True)),
                ('sum_nach1', models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)),
                ('sum_nach2', models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)),
                ('sum_nach3', models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)),
                ('sum_nach', models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)),
                ('sum_act', models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)),
                ('opl', models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)),
                ('saldo_k', models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)),
                ('nmes', models.DecimalField(null=True, max_digits=2, decimal_places=0, blank=True)),
                ('god', models.DecimalField(null=True, max_digits=4, decimal_places=0, blank=True)),
                ('department', models.ForeignKey(to='energosite.Department')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Mailing_List',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kvit', models.BooleanField(default=False, verbose_name=b'\xd0\x9a\xd0\xb2\xd0\xb8\xd1\x82\xd0\xb0\xd0\xbd\xd1\x86\xd0\xb8\xd1\x8f')),
                ('subject', models.CharField(max_length=255, verbose_name=b'\xd0\xa2\xd0\xb5\xd0\xbc\xd0\xb0')),
                ('content', ckeditor.fields.RichTextField(verbose_name=b'\xd0\xa1\xd0\xbe\xd0\xb4\xd0\xb5\xd1\x80\xd0\xb6\xd0\xb8\xd0\xbc\xd0\xbe\xd0\xb5')),
                ('date', models.DateTimeField(auto_now=True, verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0')),
            ],
            options={
                'ordering': ['-date'],
                'verbose_name': '\u0420\u0430\u0441\u0441\u044b\u043b\u043a\u0430',
                'verbose_name_plural': '\u0420\u0430\u0441\u0441\u044b\u043b\u043a\u0438',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MeterReading',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nls', models.DecimalField(verbose_name='Personal number', max_digits=7, decimal_places=0, db_index=True)),
                ('fio', models.CharField(max_length=255, verbose_name='Client name', db_index=True)),
                ('address', models.CharField(max_length=255, verbose_name='Address')),
                ('pok1', models.DecimalField(verbose_name='Day reading', max_digits=7, decimal_places=0)),
                ('pok2', models.DecimalField(null=True, verbose_name='Night reading', max_digits=7, decimal_places=0, blank=True)),
                ('pok3', models.DecimalField(null=True, verbose_name='Evening reading', max_digits=7, decimal_places=0, blank=True)),
                ('date', models.DateTimeField(verbose_name=b'Date')),
            ],
            options={
                'permissions': (('view_meter_reading', 'Can see available meter Reading'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Oplbaza',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nls', models.DecimalField(max_digits=7, decimal_places=0, db_index=True)),
                ('opl', models.DecimalField(max_digits=12, decimal_places=2)),
                ('dat_kv', models.DateField(null=True, blank=True)),
                ('data', models.DateField(null=True, blank=True)),
                ('department', models.ForeignKey(to='energosite.Department')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title_ru', models.CharField(max_length=255, null=True, blank=True)),
                ('title_kk', models.CharField(max_length=255, null=True, blank=True)),
                ('title_en', models.CharField(max_length=255, null=True, blank=True)),
                ('link', models.SlugField(unique=True, max_length=255)),
                ('content_ru', ckeditor.fields.RichTextField(null=True, blank=True)),
                ('content_kk', ckeditor.fields.RichTextField(null=True, blank=True)),
                ('content_en', ckeditor.fields.RichTextField(null=True, blank=True)),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('published', models.BooleanField(default=True)),
                ('order', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['title_ru'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tables',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=100)),
                ('dbfnumrecs', models.IntegerField(default=0)),
                ('dbtable', models.CharField(max_length=100)),
                ('charset', models.CharField(max_length=25)),
                ('day', models.DecimalField(max_digits=2, decimal_places=0)),
                ('month', models.DecimalField(max_digits=2, decimal_places=0)),
                ('year', models.DecimalField(max_digits=4, decimal_places=0)),
                ('actual_date', models.DateField()),
                ('department', models.ForeignKey(to='energosite.Department')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TopMenu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title_ru', models.CharField(max_length=255, null=True, blank=True)),
                ('title_kk', models.CharField(max_length=255, null=True, blank=True)),
                ('title_en', models.CharField(max_length=255, null=True, blank=True)),
                ('link', models.CharField(max_length=255, null=True, blank=True)),
                ('order', models.IntegerField(default=0)),
                ('published', models.BooleanField(default=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('page', models.ForeignKey(blank=True, to='energosite.Page', null=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name=b'children', blank=True, to='energosite.TopMenu', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nls', models.DecimalField(default=0, verbose_name='Personal number', max_digits=7, decimal_places=0)),
                ('mobile_phone', models.CharField(max_length=25, null=True, blank=True)),
                ('home_phone', models.CharField(max_length=25, null=True, blank=True)),
                ('mailing', models.BooleanField(default=True, verbose_name='I agree to receive newsletter')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='debtors',
            name='department',
            field=models.ForeignKey(to='energosite.Department'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='actualdate',
            name='department',
            field=models.ForeignKey(to='energosite.Department'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='actualdate',
            unique_together=set([('dbtable', 'department')]),
        ),
        migrations.AddField(
            model_name='abonbaza',
            name='department',
            field=models.ForeignKey(to='energosite.Department'),
            preserve_default=True,
        ),
    ]
