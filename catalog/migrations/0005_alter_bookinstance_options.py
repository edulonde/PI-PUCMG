# Generated by Django 4.2.7 on 2023-12-13 14:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_alter_author_options_alter_book_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'verbose_name': 'Exemplar', 'verbose_name_plural': 'Exemplares'},
        ),
    ]
