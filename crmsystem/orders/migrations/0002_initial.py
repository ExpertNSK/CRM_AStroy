# Generated by Django 3.2.16 on 2022-12-27 07:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='loader',
            name='referer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='loaders', to=settings.AUTH_USER_MODEL, verbose_name='Пригласил'),
        ),
        migrations.AddField(
            model_name='loader',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.status', verbose_name='Статус'),
        ),
        migrations.AddField(
            model_name='counteragent',
            name='contacts',
            field=models.ManyToManyField(through='orders.ContactCounterAgent', to='orders.Contactperson', verbose_name='Контактное лицо'),
        ),
        migrations.AddField(
            model_name='counteragent',
            name='kind_of_work',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.kindofwork', verbose_name='Виды работ'),
        ),
        migrations.AddField(
            model_name='contactcounteragent',
            name='contact_person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.contactperson', verbose_name='Контактное лицо'),
        ),
        migrations.AddField(
            model_name='contactcounteragent',
            name='counteragent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.counteragent', verbose_name='Контрагент'),
        ),
    ]
