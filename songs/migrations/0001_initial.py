# Generated by Django 2.1.5 on 2019-06-19 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('lyrics', models.TextField()),
                ('composer', models.CharField(max_length=100)),
                ('featuring', models.TextField()),
                ('album', models.CharField(max_length=100)),
                ('img', models.ImageField(default='default.jpg', upload_to='album_pic')),
                ('link', models.CharField(max_length=1000)),
            ],
        ),
    ]
