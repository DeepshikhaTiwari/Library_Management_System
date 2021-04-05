from django.shortcuts import render
from django.views import generic
from catalog.models import Book, Author, BookInstance, Genre
from django.shortcuts import get_object_or_404


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    content_object_name = 'my_book_list'
    queryset = Book.objects.filter(title__icontains='war')[:5]
    template_name = 'books/my_arbitrary_template_name_list.html'

    def get_queryset(self):
        return Book.objects.filter(title__icontains='war')[:5]

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context


class BookDetailView(generic.DetailView):
    model = Book

    def book_detail_view(request, primary_key):
        try:
            book = get_object_or_404(Book, pk=primary_key)
        except Book.DoesNotExist:
            return render(request, 'catalog/book_detail.html', context={'book': book})

