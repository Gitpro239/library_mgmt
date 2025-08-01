
from django.contrib import admin
from django.urls import path
from library.views import register, user_login, user_logout, dashboard, borrow_book

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('borrow/<int:book_id>/', borrow_book, name='borrow_book'),
]

# admin
# admin123

# alex123
# alex123

# author123
# author123

# publisher123
# publisher123

## npython manage.py shell

# from library.models import CustomUser, Publisher, Author, Book
# from django.utils import timezone

# # Create a Publisher
# pub_user = CustomUser.objects.create_user(username='pub1', email='pub1@example.com', password='pass123', user_type='publisher')
# publisher = Publisher.objects.create(user=pub_user, name='Global Books', address='456 Book St.')

# # Create an Author
# auth_user = CustomUser.objects.create_user(username='auth1', email='auth1@example.com', password='pass123', user_type='author')
# author = Author.objects.create(user=auth_user, name='Alice Writer', birth_date=timezone.datetime(1980, 1, 1))

# # Create Books
# Book.objects.create(title='Advanced Python', isbn='1111111111111', publisher=publisher, author=author)
# Book.objects.create(title='Django Mastery', isbn='2222222222222', publisher=publisher, author=author)
# Book.objects.create(title='HTML Mastery', isbn='2222222222222', publisher=publisher, author=author)