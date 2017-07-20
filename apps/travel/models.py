from __future__ import unicode_literals
from datetime import datetime
from django.db import models

class UserManager(models.Manager):
    def validator(self, postData):
        errors = []
        if len(postData['name'].replace(' ', '')) < 3:
            errors.append('Name must be at least 3 characters')
        if len(postData['username'].replace(' ', '')) < 3:
            errors.append('Username must be at least 3 characters')
        if len(User.objects.filter(username=postData['username'])) > 0:
            errors.append('Username is taken')
        if len(postData['pw']) < 8:
            errors.append('Password must be at least 8 characters')
        if postData['pw'] != postData['cpw']:
            errors.append('Passwords do not match')
        return errors


class TripManager(models.Manager):
    def validator(self, postData):
        errors=[]

        sdate=datetime.strptime(postData['start'], '%Y-%m-%d')
        edate=datetime.strptime(postData['end'], '%Y-%m-%d')
        if postData['dest'] == '':
            errors.append('Please enter a destination')
        if postData['desc'] == '':
            errors.append('Please enter a description')
        if datetime.strptime(postData['start'], '%Y-%m-%d').date() < datetime.now().date():
            errors.append('Start date must be in the future')
        if datetime.strptime(postData['end'], '%Y-%m-%d').date() < datetime.now().date():
            errors.append('End date must be in the future')
        if datetime.strptime(postData['end'], '%Y-%m-%d').date() < datetime.strptime(postData['start'], '%Y-%m-%d').date():
            errors.append('End date must be after the start date')
        
        return errors
        

# Create your models here.
class User(models.Model):
    name=models.CharField(max_length=255)
    username=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    objects=UserManager()

class Trip(models.Model):
    destination=models.CharField(max_length=255)
    description=models.TextField()
    startDate=models.DateField()
    endDate=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    planner=models.ForeignKey(User, related_name='trips')
    joiners=models.ManyToManyField(User, related_name='jtrips')

    objects=TripManager()
