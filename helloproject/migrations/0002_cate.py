# Generated by Django 4.0.6 on 2022-07-28 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helloproject', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='cate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
    ]
