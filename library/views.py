from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser, Member, Publisher, Author, LibraryCard, Book
from django.http import HttpResponseForbidden

# Registration View
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user_type = request.POST['user_type']
        name = request.POST['name']

        # Create CustomUser
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            user_type=user_type
        )

        # Create corresponding model based on user_type
        if user_type == 'member':
            card = LibraryCard.objects.create(card_number=f"LC{user.id:04d}")
            Member.objects.create(user=user, name=name, email=email, library_card=card)
        elif user_type == 'publisher':
            Publisher.objects.create(user=user, name=name, address=request.POST['address'])
        elif user_type == 'author':
            birth_date = request.POST['birth_date']
            Author.objects.create(user=user, name=name, birth_date=birth_date)

        messages.success(request, 'Registration successful! Please log in.')
        return redirect('login')
    return render(request, 'register.html')

# Login View
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'login.html')

# Logout View
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

# Role-Based Dashboard
@login_required(login_url="login/")
def dashboard(request):
    user = request.user
    if user.user_type == 'member':
        try:
            member = Member.objects.get(user=user)
            borrowed_books = member.borrowed_books.all()
            books = Book.objects.all()

            return render(request, 'member_dashboard.html', {
                'member': member,
                'borrowed_books': borrowed_books,
                "books" : books
            })
        except Member.DoesNotExist:
            return HttpResponseForbidden("Member profile not found.")
    elif user.user_type == 'publisher':
        try:
            publisher = Publisher.objects.get(user=user)
            published_books = Book.objects.filter(publisher=publisher)
            return render(request, 'publisher_dashboard.html', {
                'publisher': publisher,
                'published_books': published_books
            })
        except Publisher.DoesNotExist:
            return HttpResponseForbidden("Publisher profile not found.")
    elif user.user_type == 'author':
        try:
            author = Author.objects.get(user=user)
            authored_books = Book.objects.filter(author=author)
            return render(request, 'author_dashboard.html', {
                'author': author,
                'authored_books': authored_books
            })
        except Author.DoesNotExist:
            return HttpResponseForbidden("Author profile not found.")
    return HttpResponseForbidden("Invalid user type.")

# Example View for Members to Borrow a Book
@login_required
def borrow_book(request, book_id):
    if request.user.user_type != 'member':
        return HttpResponseForbidden("Only members can borrow books.")
    try:
        member = Member.objects.get(user=request.user)
        book = Book.objects.get(id=book_id)
        book.borrowers.add(member)
        messages.success(request, f'You have borrowed "{book.title}".')
        return redirect('dashboard')
    except (Member.DoesNotExist, Book.DoesNotExist):
        return HttpResponseForbidden("Error borrowing book.")