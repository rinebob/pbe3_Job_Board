# Generated by Django 2.0.7 on 2018-07-27 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks_pb3', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(on_delete='', related_name='created_jobs', to='tasks_pb3.User')),
                ('worker', models.ForeignKey(on_delete='', related_name='worked_jobs', to='tasks_pb3.User')),
            ],
        ),
    ]