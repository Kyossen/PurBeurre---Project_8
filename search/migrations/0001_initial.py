# Generated by Django 2.2.4 on 2019-08-26 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wordpass', models.CharField(max_length=12)),
                ('email', models.CharField(max_length=25)),
                ('name', models.CharField(max_length=20)),
                ('surname', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'Account',
                'ordering': ['id'],
                'managed': True,
            },
        ),
    ]
