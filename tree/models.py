# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from django.db import models


# Create your models here.


class MyChildManager(models.Manager):
    def is_mine(self):
        try:
            iam = Father.objects.get(id=1, name="Andrzej", last_name="Michalski")
        except ObjectDoesNotExist:
            print "Andrzej Michalski have to be on the first place in database with id=1 !!!!!"
        qs = iam.child_set.all()
        return qs


class Father(models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(null=True)

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
