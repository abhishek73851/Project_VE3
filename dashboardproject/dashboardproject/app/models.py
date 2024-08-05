# app/models.py
from django.db import models


def user_csv_file_path(instance, filename):
    return f"user_{instance.id}/{filename}"


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    csv_file = models.FileField(upload_to=user_csv_file_path)

    def __str__(self):
        return self.name
