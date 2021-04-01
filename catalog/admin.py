from django.contrib import admin
from .models import Book, BookInstance, Author, Language, Genre

admin.site.register(Book)

admin.site.register(BookInstance)

admin.site.register(Author)

admin.site.register(Genre)

admin.site.register(Language)


class BookInline(admin.TabularInline):
    model = Book
