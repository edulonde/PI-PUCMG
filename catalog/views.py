from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import generic
from django.db.models import Count
from .forms import BookForm, NewUserForm, BorrowBookForm
from .models import Book, Author, BookInstance, Genre, Favorite
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
import datetime
from django.contrib.auth.decorators import login_required, permission_required
from catalog.forms import RenewBookForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.db.models import Case, When, Value
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table
from io import BytesIO


def index(request):
    all_genres = Genre.objects.all()
    last_books = Book.objects.all().order_by('-id')[:4]

    context = {
        'all_genres': all_genres.annotate(num_books=Count('book')).order_by('?'),
        'last_books': last_books,

    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['favorite_books'] = [favorite.book for favorite in Favorite.objects.filter(user=self.request.user)]
        return context


class BookDetailView(generic.DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_favorite'] = Favorite.objects.filter(user=self.request.user, book=self.object).exists()
        return context


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author


class GenreListView(generic.ListView):
    model = Genre
    paginate_by = 10


def books_by_genre(request, pk):
    genre = get_object_or_404(Genre, pk=pk)
    books = Book.objects.filter(genre=genre)

    context = {
        'genre': genre,
        'books': books,
    }

    return render(request, 'catalog/books_by_genre.html', context)


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorite_list'] = Favorite.objects.filter(user=self.request.user)
        context['loaned_books'] = BookInstance.objects.filter(borrower=self.request.user).exclude(status='d')
        return context

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='e')
            .order_by('due_back')
        )


class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission."""
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 100

    def get_queryset(self):
        return (
            BookInstance.objects.all()
            .annotate(
                order=Case(
                    When(~Q(due_back=None), then=Value(1)),
                    When(status='e', then=Value(2)),
                    default=Value(3),
                )
            )
            .order_by('order', 'due_back')
        )


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/11/2023'}
    permission_required = 'catalog.add_author'


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'
    permission_required = 'catalog.change_author'


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.delete_author'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("author-delete", kwargs={"pk": self.object.pk})
            )


class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    permission_required = 'catalog.add_book'


class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.change_book'


class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.delete_book'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("book-delete", kwargs={"pk": self.object.pk})
            )


def dashboard(request):
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'd')
    num_instances_disponivel = BookInstance.objects.filter(status__exact='d').count()
    num_instances_emprestado = BookInstance.objects.filter(status__exact='e').count()
    num_instances_manutencao = BookInstance.objects.filter(status__exact='m').count()
    num_instances_reservado = BookInstance.objects.filter(status__exact='r').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    num_genres = Genre.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_disponivel': num_instances_disponivel,
        'num_instances_emprestado': num_instances_emprestado,
        'num_instances_manutencao': num_instances_manutencao,
        'num_instances_reservado': num_instances_reservado,
        'num_authors': num_authors,
        'num_genres': num_genres,

    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'dashboard.html', context=context)


def register_request(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            messages.error(request, " Ocorreu um erro ao cadastrar o usuário.")
    else:
        form = NewUserForm()
    context = {"form": form}
    return render(request=request, template_name="registration/register.html", context=context)


class MyAccountView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'catalog/my_account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['favorites'] = Favorite.objects.filter(user=self.request.user)
        return context


@login_required
def toggle_favorite(request, pk):
    book = get_object_or_404(Book, pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, book=book)
    if not created:
        favorite.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
@never_cache
def return_book_librarian(request, pk):
    """View function for returning a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # Update the status and return date of the book instance
    print(book_instance.status, book_instance.return_date, book_instance.due_back, book_instance.pk)
    book_instance.status = 'd'
    book_instance.return_date = datetime.date.today()
    book_instance.due_back = None
    book_instance.borrower = None
    print(book_instance.status, book_instance.return_date, book_instance.due_back, book_instance.pk)
    book_instance.save()

    # redirect to a new URL:
    return HttpResponseRedirect(reverse('all-borrowed'))


@login_required
def borrow_book(request, pk):
    """View function for borrowing a specific BookInstance."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = BorrowBookForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            book_instance.status = 'e'
            book_instance.due_back = timezone.now() + datetime.timedelta(days=15)
            book_instance.borrower = user
            book_instance.save()
            return HttpResponseRedirect(reverse('all-borrowed'))
    else:
        form = BorrowBookForm()

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_borrow.html', context)


def create_pdf(request):
    # Cria um arquivo PDF em memória
    buffer = BytesIO()

    # Cria o objeto PDF, usando o buffer como destino
    pdf = SimpleDocTemplate(buffer, pagesize=letter)

    # Recupera todas as instâncias de livros do banco de dados
    book_instances = BookInstance.objects.all()

    # Cria uma lista para armazenar os dados da tabela
    data = []

    # Adiciona o cabeçalho da tabela
    data.append(["Book Title", "Book Author", "Book Status"])

    # Adiciona os dados de cada instância de livro na tabela
    for instance in book_instances:
        data.append([instance.book.title, instance.book.author, instance.status])

    # Cria a tabela no PDF
    table = Table(data)

    # Adiciona a tabela ao PDF
    elements = []
    elements.append(table)

    # Constrói o PDF
    pdf.build(elements)

    # Recupera o valor do PDF a partir do buffer
    pdf_value = buffer.getvalue()
    buffer.close()

    # Cria a resposta HTTP enviando o PDF gerado
    response = HttpResponse(pdf_value, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=book_instances.pdf'
    return response
