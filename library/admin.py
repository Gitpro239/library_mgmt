from django.contrib import admin
from .models import Author, LibraryCard, Publisher, Member, Book

admin.site.register(Author)
admin.site.register(LibraryCard)
admin.site.register(Publisher)
admin.site.register(Member)
admin.site.register(Book)

