# Generated by Django 4.0.6 on 2022-09-12 05:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('helloproject', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='code',
            field=models.CharField(default='32908a54', max_length=500),
        ),
        migrations.AlterField(
            model_name='student',
            name='s_email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='code',
            field=models.CharField(default='ad0c6279', max_length=500),
        ),
        migrations.CreateModel(
            name='notifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_student_sender', models.BooleanField()),
                ('message', models.CharField(max_length=500)),
                ('timestamp', models.DateTimeField()),
                ('s_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='helloproject.student', to_field='s_email', unique=True)),
                ('t_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='helloproject.teacher')),
            ],
        ),
    ]
