import django_filters
from .models import Book


class PlaceFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Book
        fields = ['title', 'author', 'genre']
