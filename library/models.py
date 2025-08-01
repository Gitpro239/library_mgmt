from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('author', 'Author'),
        ('publisher', 'Publisher'),
        ('member', 'Member'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.user_type})"

# One-to-One: Each Member has one LibraryCard
class LibraryCard(models.Model):
    card_number = models.CharField(max_length=10, unique=True)
    issue_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Card {self.card_number}"

class Member(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'member'})
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    library_card = models.OneToOneField(LibraryCard, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# One-to-Many: One Publisher can publish many Books
class Publisher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'publisher'})
    name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.name

# Many-to-One: Many Books can be written by one Author
class Author(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'author'})
    name = models.CharField(max_length=100)
    birth_date = models.DateField()

    def __str__(self):
        return self.name

# Many-to-Many: A Book can be borrowed by many Members, and a Member can borrow many Books
class Book(models.Model):
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    borrowers = models.ManyToManyField(Member, related_name='borrowed_books')

    def __str__(self):
        return self.title