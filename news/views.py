from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import News
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'news/home.html')


def signupuser(request):
    if request.method=='GET':
        return render(request, 'news/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currentnews')
            except IntegrityError:
                return render(request, 'news/signupuser.html', {'form': UserCreationForm(), 'error': 'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'news/signupuser.html', {'form': UserCreationForm(), 'error': 'Passwords did not match'})

def loginuser(request):
    if request.method=='GET':
        return render(request, 'news/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'news/loginuser.html', {'form': AuthenticationForm(), 'error': "Username and password didn't match"})
        else:
            login(request, user)
            return redirect('currentnews')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def createnews(request):
    if request.method=='GET':
        return render(request, 'news/createnews.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newnews = form.save(commit=False)
            newnews.todocreator = request.user
            newnews.save()
            return redirect('currentnews')
        except ValueError:
            return render(request, 'news/createnews.html', {'form': TodoForm(), 'error': 'Передано неправильні дані. Повторіть спробу'})

@login_required
def currentnews(request):
    news = News.objects.filter(newscreator=request.user, datearchived__isnull=True)
    return render(request, 'news/currentnews.html', {'news': news})

@login_required
def viewnews(request, todo_id):
    viewnews = get_object_or_404(News, pk=news_id, newscreator=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=viewnews)
        return render(request, 'news/viewnews.html', {'viewnews': viewnews, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=viewnews)
            form.save()
            return redirect('currentnews')
        except ValueError:
            return render(request, 'news/createnews.html', {'form': TodoForm(), 'error': 'Передано неправильні дані. Повторіть спробу'})

def archivenews(request, todo_id):
    archivenews = get_object_or_404(News, pk=news_id, newscreator=request.user)
    if request.method == 'POST':
        archivenews.datecompleted = timezone.now()
        archivenews.save()
        return redirect('currentnews')

def deletenews(request, todo_id):
    deletednews = get_object_or_404(News, pk=news_id, newscreator=request.user)
    if request.method == 'POST':
        deletednews.delete()
        return redirect('currentnews')

def deletenews_archives(request, todo_id):
    deletednews = get_object_or_404(News, pk=news_id, newscreator=request.user)
    if request.method == 'POST':
        deletednews.delete()
        return redirect('archivednews')

@login_required
def archivednews(request):
    archivednews = News.objects.filter(newscreator=request.user, datearchived__isnull=False).order_by('-datearchived')
    return render(request, 'news/archivednews.html', {'news': archivednews})
