from django.db import models
import re
import bcrypt
from datetime import datetime


class UserManager(models.Manager):
    def signup_validator(self , postData):
        errors = {}
        if postData['dob'] == '':
            errors['dob'] = 'Please enter Date of Birth'
        else:
            dob = datetime.strptime(postData['dob'] , "%Y-%m-%d")
            age = int(datetime.today().strftime('%Y')) - int(dob.strftime('%Y')) 
            if age <= 13 : 
                errors['dob'] = 'Age must be greater than 13'
        if len(postData['first_name']) < 2 : 
            errors['first_name'] = 'First Name must be at least 2 characters '
        if len(postData['last_name']) < 2 : 
            errors['last_name'] = 'Last Name must be at least 2 characters '
        if len(postData['password']) < 8 : 
            errors['password'] = 'Password should be at least 8 characters'
        if postData['dob']>= datetime.today().strftime('%Y-%m-%d'):
            errors['dob'] = 'Date of Birth must be in the past'
        if postData['password'] != postData['confirmPassword'] :
            errors['cpw'] = 'Passwords do not match'
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):      
            errors['email'] = "Invalid email address!"
        if User.objects.filter(email = postData['email']).exists():
            errors['email'] = "Email already exists"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length= 50)
    email = models.CharField(max_length=100)
    dob = models.DateField()
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Message(models.Model):
    message = models.TextField()
    users = models.ForeignKey(User , related_name='messages' , on_delete=models.CASCADE )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    comment = models.TextField()
    users = models.ForeignKey(User , related_name='comments' , on_delete=models.CASCADE )
    messages = models.ForeignKey(Message , related_name='comments' , on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




def create_user(first_name , last_name , email , password , dob):
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    return User.objects.create(first_name = first_name , last_name = last_name , email = email , password = pw_hash , dob = dob)


def user_info(id):
    return User.objects.get(id=id)

def view_msgs():
    return Message.objects.all()

def create_msg(message , user):
    return Message.objects.create(message = message , users = user)

def create_comment(comment , user , message):
    return Comment.objects.create(comment = comment , users = user  , messages = message)

def clear_comment(id):
    thecomment = Comment.objects.get(id=id)
    return thecomment.delete()