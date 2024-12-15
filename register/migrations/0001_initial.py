# Generated by Django 5.1.4 on 2024-12-15 16:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('studentname', models.CharField(max_length=30, validators=[django.core.validators.RegexValidator('^[a-zA-Z\\s]+$', 'Enter a valid name. Only letters and spaces are allowed.')])),
                ('parentname', models.CharField(max_length=30, validators=[django.core.validators.RegexValidator('^[a-zA-Z\\s]+$', 'Enter a valid name. Only letters and spaces are allowed.')])),
                ('phonenumber', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^\\d{10}$', 'Enter a valid 10-digit phone number.')])),
                ('category', models.CharField(choices=[('1', 'Anganvadi'), ('1', 'LKG'), ('1', 'UKG'), ('2', '1st'), ('2', '2nd'), ('3', '3rd'), ('3', '4th'), ('3', '5th'), ('4', '6th'), ('4', '7th')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('paid', models.BooleanField(default=False)),
                ('chestnumber', models.CharField(help_text='Unique chest number for the student.', max_length=10, unique=True)),
            ],
            options={
                'ordering': ['created_at'],
                'constraints': [models.UniqueConstraint(fields=('studentname', 'parentname', 'phonenumber', 'category'), name='unique_student_in_category_and_phone'), models.UniqueConstraint(fields=('chestnumber',), name='unique_chestnumber')],
            },
        ),
    ]
