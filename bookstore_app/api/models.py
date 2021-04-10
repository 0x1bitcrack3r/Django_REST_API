from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


#
# # Create your models here.
# class Author(models.Model):
#     name = models.CharField(max_length=200)
#     added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     created_date = models.DateTimeField(default=timezone.now)
#
#     def __str__(self):
#         return self.name
#
#
# class Book(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.CharField(max_length=300)
#     author = models.ForeignKey(Author, on_delete=models.CASCADE)
#     added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     created_date = models.DateTimeField(default=timezone.now)
#
#     def __str__(self):
#         return self.title


class Group(models.Model):
    group_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    group_name = models.CharField(max_length=50)

    def __str__(self):
        return self.group_name


class User(models.Model):
    user_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    groups = models.ManyToManyField(Group, blank=True)

    def __str__(self):
        return self.first_name
