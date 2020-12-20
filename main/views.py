from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Message, Comment
from datetime import datetime
import bcrypt

# Create your views here.


# The following is all for login / user creating
def index(request):
    if 'user_id' in request.session:
        return redirect('/welcome')
    context = {
        'all_users': User.objects.all(),
    }
    return render(request, 'index.html', context)

def process_create(request):
    errors = User.objects.user_validator(request.POST)
    if len(errors) > 0:
        for message in errors.values():
            messages.error(request, message)
        return redirect('/')
    password = request.POST['password']
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        password=hashed,
    )
    request.session['user_id'] = user.id
    return redirect('/welcome')

def process_login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for msg in errors.values():
            messages.error(request, msg)
        return redirect('/')
    email_users = User.objects.filter(email=request.POST['email'])
    user = email_users[0]
    if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        request.session['user_id'] = user.id
        return redirect('/')
    messages.error(request, "Password does not match")
    return render(request, '/welcome')

def logout(request):
    request.session.clear()
    return redirect('/')


# The following is for Once logged in
def welcome(request):
    context = {
        'logged_in_user': User.objects.get(id=request.session['user_id']),
        'all_messages': Message.objects.all(),
    }
    return render(request, 'welcome.html', context)

def process_message(request):
    Message.objects.create(
        user = User.objects.get(id=request.session['user_id']),
        message = request.POST['message'],
    )
    return redirect('/welcome')

def comments(request):
    context = {
        'logged_in_user': User.objects.get(id=request.session['user_id']),
        'all_messages': Message.objects.all(),
        'all_comments': Comment.objects.all(),
    }
    return render(request, 'comments.html', context)

def process_comment(request):
    Comment.objects.create(
        user = User.objects.get(id=request.session['user_id']),
        message = Message.objects.get(id=request.POST['message_id']),
        comment = request.POST['comment'],
    )
    return redirect('/comments')