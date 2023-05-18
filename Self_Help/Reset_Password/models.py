from django.db import models
from django_cryptography.fields import encrypt
from . import Security_Questions

Security_Questions_list = Security_Questions.Security_Questions


class Post(models.Model):
    onprem_sid = encrypt(models.CharField(max_length=200))
    name = encrypt(models.CharField(max_length=200))
    email = models.CharField(max_length=200)
    question_one = encrypt(models.CharField(max_length=200, choices=Security_Questions_list))
    answer_one = encrypt(models.CharField(max_length=200))
    question_two = encrypt(models.CharField(max_length=200, choices=Security_Questions_list))
    answer_two = encrypt(models.CharField(max_length=200))
    question_three = encrypt(models.CharField(max_length=200, choices=Security_Questions_list))
    answer_three = encrypt(models.CharField(max_length=200))

    def __str__(self):
        return self.name
