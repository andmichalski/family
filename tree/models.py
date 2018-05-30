# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import Q
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
# Create your models here.


class MyChildManager(models.Manager):
    def is_mine(self):
        try:
            iam = Father.objects.get(Q(id=1) & Q(name="Andrzej") & Q(last_name="Michalski"))
        except ObjectDoesNotExist:
            print "Andrzej Michalski have to be on the first place in database with id=1 !!!!!"
        qs = MyChilds.mychilds_objects.filter(father=iam)
        return qs

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

    objects = models.Manager()
    mychilds_objects = MyChildManager()


class ChildIsToddler(Child):
    class Meta:
        proxy = True
        ordering = ['name']
        verbose_name_plural = "Toddler's child"


class MyChilds(Child):
    class Meta:
        proxy = True
        verbose_name_plural = "My childs"