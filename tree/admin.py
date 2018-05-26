# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Child, Father
from django.contrib import admin

# Register your models here.

class ChildInline(admin.TabularInline):
    model = Child

@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    search_fields = ["first_name"]
    list_display = ['name', 'last_name', 'birth']
    date_hierarchy = 'birth' #TODO why can not do with father
    raw_id_fields = ("father",)


@admin.register(Father)
class FatherAdmin(admin.ModelAdmin):
    inlines = [ChildInline]