from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from .forms import Todoform
from .models import TODO
from django.utils import timezone
from django.contrib.auth.decorators import login_required  #authenticates and allows only certain page to access before registration
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

@login_required
def Logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    else:
        return HttpResponse('404- not found')

@login_required
def currenttodos(request):
    try:
        todo=TODO.objects.filter(user=request.user,Datecomplited__isnull=True) #True hunjel samma current todoma hunxa natra false bhayepaxi complete ma janxa
        return render(request,'todo/currenttodos.html',{'todos':todo})
    except TypeError:
        return HttpResponse('404 - Not Found')

@login_required
def completedtodo(request):
        todo=TODO.objects.filter(user=request.user,Datecomplited__isnull=False).order_by('-Datecomplited') #True hunjel samma current todoma hunxa natra false bhayepaxi complete ma janxa
        return render(request,'todo/completedtodo.html',{'todos':todo})
   

@login_required
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

@login_required       
def viewtodo(request,todo_pk):   #update
    todo=get_object_or_404(TODO,pk=todo_pk,user=request.user) #registered user le matra acess garn apauxa
    
    if request.method=='GET':
        form=Todoform(instance=todo)
        return render(request, 'todo/viewtodo.html',{'todo':todo,'form':form})
    else:
        try:
            todo=Todoform(request.POST,instance=todo)
            todo.save()
            return redirect('currenttodos')
        except ValueError:
            return redirect(request, 'todo/viewtodo.html',{'error':'Error occured'})

@login_required
def completetodo(request,todo_pk):

    todo=get_object_or_404(TODO,pk=todo_pk,user=request.user) 
    if request.method=='POST':
        todo.Datecomplited=timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request,todo_pk):
    todo=get_object_or_404(TODO,pk=todo_pk,user=request.user) 
    if request.method=='POST':
        todo.delete()
        return redirect('currenttodos')


        

