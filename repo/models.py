from django.db import models


# Create your models here.

class Repo(models.Model):
    name = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.name)


class Class(models.Model):
    name = models.CharField(max_length=255, blank=False, unique=True)
    repo = models.ForeignKey(
        'Repo',
        on_delete=models.CASCADE
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}/{}".format(self.repo, self.name)
