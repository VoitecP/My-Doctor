# Generated by Django 4.2.1 on 2023-05-06 15:37

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('usertype', models.CharField(choices=[('d', 'Doctor'), ('p', 'Patient'), ('d', 'Director')], default='', max_length=1)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'permissions': [('is_user', 'Is User')],
                'managed': True,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=30, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('slug', models.SlugField(editable=False, null=True)),
                ('description', models.CharField(max_length=12)),
            ],
            options={
                'permissions': [('is_director', 'Is Director')],
            },
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('slug', models.SlugField(editable=False, null=True)),
                ('specialization', models.CharField(max_length=12)),
            ],
            options={
                'permissions': [('is_doctor', 'Is Doctor')],
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('slug', models.SlugField(editable=False, null=True)),
                ('adress', models.CharField(max_length=80)),
                ('birth_date', models.DateField(default=datetime.date.today)),
            ],
            options={
                'permissions': [('is_patient', 'Is Patient')],
            },
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(default='', max_length=100)),
                ('date', models.DateTimeField(blank=True, default=None, null=True)),
                ('description', models.TextField()),
                ('price', models.CharField(max_length=10)),
                ('category', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.category')),
                ('doctor', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='core.doctor')),
                ('patient', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='core.patient')),
            ],
            options={
                'ordering': ('date',),
            },
        ),
    ]
