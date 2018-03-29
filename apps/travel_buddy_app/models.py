from __future__ import unicode_literals
from django.db import models 
import bcrypt
# from dateutil.parser import parse as parse_date
from datetime import date,datetime

# Create your models here.

class UserManager(models.Manager):
    def validate_registration(self,form_data):
        errors=[]
        #name
        if len(form_data['name']) < 3:
            errors.append('Name is required and must be at least 3 characters.')
        if not form_data['name'].isalpha():
            errors.append('Name must be letters only, can not contain any numbers or special characters.')
        #username
        if len(form_data['username']) < 3:
            errors.append('Username is required and must be at least 3 characters.')
        if not form_data['username'].isalpha():
            errors.append('Username must be letters only, can not contain any numbers or special characters.')
        if len(User.objects.filter(username=form_data['username'])) > 0:
            errors.append('Username is already taken.')
        #password
        if len(form_data['password']) < 8:
            errors.append('Password must be at least 8 characters')
        if form_data['password'] != form_data['confirm_password']:
            errors.append('Passwords do not match')
        return errors

    def create_user(self,form_data):
        salt = bcrypt.gensalt()
        return User.objects.create(
            name = form_data['name'],
            username = form_data['username'],
            password = bcrypt.hashpw(form_data['password'].encode(),salt)
        )       

    def validate_login(self,form_data):
        errors=[]
        if len(form_data['username']) == 0:
            errors.append('Username can not be blank!')
        if len(form_data['password']) == 0:
            errors.append('Password can not be blank!')
        user=User.objects.filter(username=form_data['username']).first()
        if user:
            user_password = form_data['password'].encode()
            db_password = user.password.encode()
            if bcrypt.checkpw(user_password,db_password):
                return {'user':user}
            else:
                errors.append('username or password does not match')
        return {'errors':errors}

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = UserManager()

class TravelManager(models.Manager):
    def travel_validation(self, form_data):
        errors=[]
        #destination & description
        if len(form_data['destination']) == 0 :
            errors.append("Destination field is required.")
        if len(form_data['description']) == 0 :
            errors.append("Description field is required.")
        #date
        if len(form_data['start_date'])==0:
            errors.append("A valid Start Date is required.")
        elif str(date.today()) > str(form_data['start_date']):
                errors.append("Travel from date cannot be in the past.")
        if len(form_data['end_date'])==0:
            errors.append("A valid End Date is required.")
        elif str(date.today()) > form_data['end_date']:
            errors.append("Travel to date cannot be in the past.")
        if form_data['start_date'] > form_data['end_date']:
            errors.append("'Travel Date To' should not be before the 'Travel Date From'.")
        
        return errors

    def create_plan(self,form_data,id):
        return Travel.objects.create(
            destination = form_data['destination'],
            description = form_data['description'],
            start_date = form_data['start_date'],
            end_date = form_data['end_date'],
            planner = User.objects.get(id=id)
            ) 

class Travel(models.Model):
    destination = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255)
    start_date = models.DateField()
    end_date = models.DateField()
    planner = models.ForeignKey(User,related_name="planned_travels")
    joiner = models.ManyToManyField(User, related_name="joined_travels")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TravelManager()

    


