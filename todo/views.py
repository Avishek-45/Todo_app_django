from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from .forms import Todoform
from .models import TODO
# Create your views here.


def home(request):
     return render(request,'todo/home.html')

def signupuser(request):
    if request.method=='GET':
        return render(request,'todo/signupuser.html',{'form':UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user= User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request,'todo/signupuser.html',{'form':UserCreationForm,'error':'Username not found.Try new one.'})
        else:
            return render(request,'todo/signupuser.html',{'form':UserCreationForm,'error':'Password should match.'})
            

def Loginuser(request):
    if request.method == 'GET':
        return render(request,'todo/Loginuser.html',{'form':AuthenticationForm})
    else:
        user=authenticate(request, username=request.POST['username'], password=request.POST['username'])
        if user is None:
            return render(request,'todo/Loginuser.html',{'form':AuthenticationForm,'error':'Username or Password didnot match.'})
        else:
            login(request,user)
            return redirect('currenttodos')


def Logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    else:
        return HttpResponse('404- not found')

def currenttodos(request):
    todo=TODO.objects.filter(user=request.user)
    return render(request,'todo/currenttodos.html',{'todos':todo})

def create_todo(request):
    if request.method=='GET':
        context={'form':Todoform()}
        return render(request,'todo/create_todo.html',context)
    else:
        try:
            form=Todoform(request.POST)
            newtodos=form.save(commit=False)
            newtodos.user=request.user   #kun user le  save gareko create garna lai
            newtodos.save()
            return redirect('/')

        except ValueError:
            return render(request,'todo/create_todo.html',{'form':Todoform(),'error':'Bad input'})

        
def viewtodo(request,todo_pk):
    todo=get_object_or_404(TODO,pk=todo_pk)
    return render(request, 'todo/viewtodo.html',{'todo':todo})