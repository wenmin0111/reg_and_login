from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# NAME_REGEX =re.compile('^[A-z]+$')

# Create your models here.
class UserManager(models.Manager):
    def reg_fn_validation(self, postData):
        errors = []
        # //first_name validate
        if len(postData['first_name'])< 2 or not postData['first_name'].isalpha():
            errors.append('firstName: Letters only and No fewer than 2 characters.')
        # //last_name validate
        if len(postData['last_name'])< 2 or not postData['last_name'].isalpha():
            errors.append('lastName: Letters only and No fewer than 2 characters.')
        # //email validate
        if not EMAIL_REGEX.match(postData['email']):
            errors.append('EMAIL is NOT validate.')
        elif len(User.objects.filter(email=postData['email'])) != 0:
            errors.append('EMAIL has been registered.')
        # //password validate
        if len(postData['password']) < 8:
            errors.append('password not less than 8 characters.')
        elif postData['password'] != postData['confirm']:
            errors.append('password not match.')
            # return 'errors'

        if len(errors) == 0:
            hashed_pw = bcrypt.hashpw(postData['password'].encode('utf-8'), bcrypt.gensalt())
            # print hashed_pw + "STORED HASH"
            d = User.objects.create(first_name=postData['first_name'], last_name=postData['last_name'], email=postData['email'], password=hashed_pw)
            return [True, d]

        else:
            # print errors
            # return [False, False]
            return errors
    def login_check(self, postData):
        errors = []
        # check email exist
        if User.objects.filter(email=postData['email']).count()==0:
            errors.append('User is not exist!')
        elif len(postData['password'])==0:
                errors.append('Please insert password!')
        # check pw
        else:
            stored_hash = User.objects.get(email=postData['email']).password
            input_hash = bcrypt.hashpw(postData['password'].encode(), stored_hash.encode())
        # print input_hash + "INPUT HASH"
            if stored_hash != input_hash:
                errors.append('Incorrect password!')
        if len(errors) == 0:
            return True
        else:
            # print errors
            return errors

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __unicode__(self):
        return 'id: '+ str(self.id) + ' first_name: '+ self.first_name + ' last_name: ' + self.last_name + ' email: ' + self.email + 'password: ' + self.password + '   '

class Post(models.Model):
    post = models.TextField()
    user = models.ForeignKey(User, related_name='user_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return 'id: '+ str(self.id) + ' post: '+ self.post + '   '

# favoriting_users = models.ManyToManyField(User, related_name='favoriting_books')
# ManyToManyField represents this calss
#
# class UserBook(models.Model):
#     user = models.ForeignKey(User, related_name='user_posts')
#     book = models.ForeignKey(Book, related_name='user_posts')
#
#     def __unicode__(self):
#         return 'id: '+ str(self.id) + ' user_id: '+ str(self.user.id) + ' book_id: ' + str(self.post.id) + '   '
