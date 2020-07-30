from django.db import models


class UserInfo(models.Model):
    username = models.CharField(max_length=16)
    password = models.CharField(max_length=32)


class UserGroup(models.Model):
    title = models.CharField(max_length=32)
