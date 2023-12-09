# Generated by Django 4.2.7 on 2023-12-09 00:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_remove_book_isbn'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='language',
            field=models.CharField(blank=True, choices=[('pt', 'Português'), ('en', 'Inglês'), ('es', 'Espanhol'), ('fr', 'Francês'), ('de', 'Alemão'), ('it', 'Italiano'), ('ja', 'Japonês'), ('cn', 'Chinês'), ('ar', 'Árabe'), ('ru', 'Russo')], default='pt', help_text='Selecione o idioma do livro', max_length=2),
        ),
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(help_text='Selecione um gênero para esse livro.', to='catalog.genre'),
        ),
        migrations.AlterField(
            model_name='book',
            name='summary',
            field=models.TextField(help_text='Insira uma breve descrição do livro', max_length=1000),
        ),
        migrations.AlterField(
            model_name='bookinstance',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, help_text='ID único para este livro específico em toda a biblioteca', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='bookinstance',
            name='status',
            field=models.CharField(blank=True, choices=[('m', 'Manutenção'), ('e', 'Em empréstimo'), ('d', 'Disponível'), ('r', 'Reservado')], default='m', help_text='Disponibilidade do livro', max_length=1),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(help_text='Insira um gênero de livro (por exemplo, Ficção Científica, Poesia Francesa etc.)', max_length=200, unique=True),
        ),
    ]
