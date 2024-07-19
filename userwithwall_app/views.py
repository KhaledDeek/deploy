from django.shortcuts import render , redirect , HttpResponse
from . import models
from django.contrib import messages
import bcrypt

def index(request):
    return render(request , 'index.html')

def register(request):
    if request.method == 'POST':
        errors = models.User.objects.signup_validator(request.POST)
        if len(errors) > 0:
            for k , value in errors.items():
                messages.error(request , value)
            return redirect('/')
        else:
            new_user = models.create_user(first_name=request.POST['first_name'] , last_name=request.POST['last_name'] , email=request.POST['email'] , password=request.POST['password'] , dob = request.POST['dob'])
            request.session['first_name'] = request.POST['first_name']
            request.session['id'] = new_user.id
            return redirect('/wall')
    else:
        return redirect('/')


def validate_login(request):
    if request.method == 'POST':
        user = models.User.objects.get(email=request.POST['email'])  
        request.session['first_name'] = user.first_name
        request.session['id'] = user.id
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            return redirect('/wall')
        else:
            context = {
                'error' : 'Email or Password do not Match',
            }
            return render(request , 'index.html' , context )
    else:
        return redirect('/')


def success(request):
    if 'first_name' not in request.session:
        return redirect('/')
    else:
        id = request.session['id']
        context = {
            'fn' : request.session['first_name'] ,
            'users': models.user_info(id=id),
            'messages' : models.view_msgs(),
        }
        return render(request , 'welcome.html' , context)

def create_message(request):
    models.create_msg(message=request.POST['txt'] , user = models.User.objects.get(id=request.session['id']) )
    return redirect('/wall')

def create_comment(request):
    if request.method =='POST':
        models.create_comment(comment = request.POST['txt'] , user = models.User.objects.get(id=request.session['id']) , message = models.Message.objects.get(id = request.POST['msg_id']))
        return redirect('/wall')
    else: 
        return redirect('/wall')


def clear_comment(request):
    models.clear_comment(id = request.POST['comment_id'])
    return redirect('/wall')

def logout(request):
    request.session.clear()
    return redirect('/')



