# Generated by Django 3.1.2 on 2020-11-11 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Corpus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quality', models.BooleanField(auto_created=True)),
                ('uuid', models.CharField(max_length=36)),
                ('userid', models.CharField(max_length=16)),
                ('timestamp', models.TimeField(auto_now=True)),
                ('first_couplet', models.CharField(max_length=16)),
                ('second_couplet', models.CharField(max_length=16)),
                ('status', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('userid', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.CharField(max_length=48)),
                ('username', models.CharField(max_length=16)),
                ('password', models.CharField(max_length=16)),
                ('avatar', models.ImageField(upload_to='../avatar/')),
            ],
        ),
    ]