# Generated by Django 3.2.16 on 2022-12-24 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20221224_1938'),
    ]

    operations = [
        migrations.CreateModel(
            name='Counteragent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[(1, 'Юридическое лицо'), (2, 'Физическое лицо')], max_length=50, verbose_name='Тип контрагента')),
                ('legal_name', models.CharField(max_length=200, verbose_name='Юридическое наименование')),
                ('short_name', models.CharField(max_length=200, verbose_name='Краткое наименование')),
                ('inn', models.IntegerField(verbose_name='ИНН')),
                ('kpp', models.IntegerField(verbose_name='КПП')),
                ('legal_address', models.TextField(max_length=200, verbose_name='Юридический адрес')),
                ('actual_address', models.TextField(max_length=200, verbose_name='Фактический адрес')),
                ('payment_account', models.IntegerField(verbose_name='Рассчетный счёт')),
                ('correspondent_account', models.IntegerField(verbose_name='Корреспондентский счёт')),
                ('bik', models.IntegerField(verbose_name='БИК')),
                ('bank', models.CharField(max_length=50, verbose_name='Наименование банка')),
                ('kind_of_work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.kindofwork', verbose_name='Виды работ')),
            ],
            options={
                'verbose_name': 'Контрагент',
                'verbose_name_plural': 'Контрагенты',
                'ordering': ['short_name'],
            },
        ),
    ]