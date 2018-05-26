# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
# Create your models here.

class Father(models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return self.name + " " + self.last_name

class Child(models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    father = models.ForeignKey(Father, on_delete=models.CASCADE)
    birth = models.DateField(null=True)

    def __str__(self):
        return self.name + " " + self.last_name

    def is_toddler(self):
        age = datetime.now - self.birth
        if age.year < 3:
            return True
        else:
            return False