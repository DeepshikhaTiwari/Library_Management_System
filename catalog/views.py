import datetime

from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Book, Author, BookInstance
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .filter import PlaceFilter
from .forms import RenewBookForm


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            return HttpResponseRedirect(reverse('my-borrowed'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 4
    context_object_name = 'my_book_list'
    queryset = Book.objects.filter(title__icontains='war')[:5]
    template_name = 'books/book_detail.html'

    def get_queryset(self):
        return Book.objects.all()

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['filter'] = PlaceFilter(self.request.GET, queryset=self.get_queryset())
        return context


class BookDetailView(generic.DetailView):
    model = Book


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 5

    def get_queryset(self):
        return BookInstance.objects.filter(status__icontains='o')


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 4


class AuthorDetailView(generic.DetailView):
    model = Author


class AuthorCreate(LoginRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']


class AuthorUpdate(LoginRequiredMixin, UpdateView):
    model = Author
    context_object_name = 'author'
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']


class AuthorDelete(LoginRequiredMixin, DeleteView):
    model = Author
    success_url = '/'


class BookCreate(CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre']


class BookUpdate(LoginRequiredMixin, UpdateView):
    model = Book
    context_object_name = 'book'
    fields = ['title', 'author', 'summary', 'isbn', 'genre']


class BookDelete(LoginRequiredMixin, DeleteView):
    model = Book
    success_url = '/'
