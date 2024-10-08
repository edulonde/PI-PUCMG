from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('borrowed/', views.LoanedBooksAllListView.as_view(), name='all-borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('genres', views.GenreListView.as_view(), name='genres'),
    path('genre/<int:pk>/books/', views.books_by_genre, name='books-by-genre'),
    path('register', views.register_request, name="register"),
    path('myaccount/', views.MyAccountView.as_view(), name='my-account'),
    path('book/<int:pk>/toggle_favorite/', views.toggle_favorite, name='toggle-favorite'),
    path('book/<uuid:pk>/return/', views.return_book_librarian, name='return-book-librarian'),
    path('book/<uuid:pk>/borrow/', views.borrow_book, name='borrow-book'),
    path('export-to-pdf/', views.create_pdf, name='export-to-pdf'),

]
