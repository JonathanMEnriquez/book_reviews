# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .models import *
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'reviews/index.html')

def process(request, action):
    if request.method == 'POST':
        if action == 'add':
            check_submission = User.objects.validateRegistration(request.POST)
            if len(check_submission) > 0:
                for message in check_submission['error']:
                    messages.error(request, message)
                return redirect('/')
            else:
                newuser = User.objects.addUser(request.POST)
                request.session['id'] = newuser.id
                return redirect('/books')
        elif action == 'login':
            if len(request.POST['user_input']) < 1 or len(request.POST['password']) < 8:
                messages.warning(request, 'Invalid login information')
                return redirect('/')
            user = User.objects.validateLogin(request.POST)
            if user:
                request.session['id'] = user
                return redirect('/books')
            else:
                messages.warning(request, 'Invalid login information')
                return redirect('/')
            return redirect('/')
        elif action == 'addbook':
            if len(request.POST['title']) < 1 or len(request.POST['content']) < 1 or len(request.POST['rating']) < 1:
                messages.error(request, 'Please fill in all fields')
                return redirect('/books/add')
            if len(request.POST['newname']) < 1:
                try:
                    author = Author.objects.get(id = request.POST['name'])
                except:
                    print "couldn't find author"
                    return redirect('/books/add')
            else:
                if not Author.objects.validateAuthor(request.POST):
                    messages.error(request, 'Please enter a valid author name')
                    return redirect('/books/add')
                author = Author.objects.addAuthor(request.POST)
            book = Book.objects.addBook(request.POST, author)
            user_id = request.session['id']
            user = User.objects.get(id = user_id)
            review = Review.objects.addRating(request.POST, user, book)
            return redirect('/books/'+str(book.id)+'')
        else:
            print 'went through process for some reason'
            return redirect('/books')
    else:
        print 'get out'
        return redirect('/')

def addbookshort(request, book_id):
    if request.method == 'POST':
        if len(request.POST['title']) < 1 or len(request.POST['content']) < 1 or len(request.POST['rating']) < 1:
            messages.error(request, 'Please fill in all fields')
            return redirect('/books/{}'.format(book_id))
        try:
            author = Author.objects.get(name = request.POST['name'])
        except:
            print "couldn't find author"
            return redirect('/books/{}'.format(book_id))
        try:
            book = Book.objects.get(id = book_id)
        except:
            print "couldn't find book"
            return redirect('/books/{}'.format(book_id))
        user_id = request.session['id']
        user = User.objects.get(id = user_id)
        review = Review.objects.addRating(request.POST, user, book)
        return redirect('/books/'+str(book.id))
    else:
        print 'get out of add book short process'
        return redirect('/books/{}'.format(book_id))

def logout(request):
    try:
        del request.session['id']
        return redirect('/')
    except:
        return redirect('/')

def welcome(request):
    try:
        request.session['id']
    except:
        return redirect('/')
    context = {
        'user':User.objects.get(id = request.session['id']),
        'recent':Review.objects.order_by('-created_at')[:3],
        'books':Book.objects.order_by('title'),
    }
    return render(request, 'reviews/welcome.html', context)

def add_review(request):
    try:
        request.session['id']
    except:
        return redirect('/')
    context = {
        "the_user": User.objects.get(id = request.session['id']),
        "authors": Author.objects.all(),
    }
    return render(request, 'reviews/addreview.html', context)

def show_book(request, book_id):
    context = {
        'reviews': Book.objects.get(id=book_id).reviews.all(),
        'book': Book.objects.get(id = book_id)
    }
    return render(request, 'reviews/showbook.html', context)

def show_user(request, user_id):
    context = {
        'user': User.objects.get(id = user_id),
        'reviews': Review.objects.filter(reviewer__id=user_id),
    }
    return render(request, 'reviews/showuser.html', context)