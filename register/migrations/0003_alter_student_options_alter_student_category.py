# Generated by Django 5.1.4 on 2024-12-15 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0002_rename_students_student'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ['chestnumber']},
        ),
        migrations.AlterField(
            model_name='student',
            name='category',
            field=models.CharField(choices=[('1', 'Anganvadi'), ('2', 'LKG'), ('3', 'UKG'), ('4', '1st'), ('5', '2nd'), ('6', '3rd'), ('7', '4th'), ('8', '5th'), ('9', '6th'), ('10', '7th')], max_length=20),
        ),
    ]
