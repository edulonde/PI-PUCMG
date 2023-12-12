from django.db import models
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns
import uuid  # Required for unique book instances


class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Insira um gênero de livro (por exemplo, Ficção Científica, Poesia Francesa etc.)"
    )

    class Meta:
        verbose_name = 'Gênero'
        verbose_name_plural = 'Gêneros'

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a particular genre instance."""
        return reverse('genre-detail', args=[str(self.id)])


class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.RESTRICT, null=True)
    # Foreign Key used because book can only have one author, but authors can have multiple books.
    # Author as a string rather than object because it hasn't been declared yet in file.

    summary = models.TextField(
        max_length=1000, help_text="Insira uma breve descrição do livro")

    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(
        Genre, help_text="Selecione um gênero para esse livro.")

    class Meta:
        verbose_name = 'Livro'
        verbose_name_plural = 'Livros'

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

    LANGUAGES = (
        ('pt', 'Português'),
        ('en', 'Inglês'),
        ('es', 'Espanhol'),
        ('fr', 'Francês'),
        ('de', 'Alemão'),
        ('it', 'Italiano'),
        ('ja', 'Japonês'),
        ('cn', 'Chinês'),
        ('ar', 'Árabe'),
        ('ru', 'Russo'),)

    language = models.CharField(
        max_length=2,
        choices=LANGUAGES,
        blank=True,
        default='pt',
        help_text='Selecione o idioma do livro',
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])


class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="ID único para este livro específico em toda a biblioteca")
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)



    LOAN_STATUS = (
        ('m', 'Manutenção'),
        ('e', 'Em empréstimo'),
        ('d', 'Disponível'),
        ('r', 'Reservado'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Disponibilidade do livro',
    )

    class Meta:
        ordering = ['due_back']
        verbose_name = 'Exemplar'
        verbose_name_plural = 'Exemplares'

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)


    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'
