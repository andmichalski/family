# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Child, Father, ChildIsToddler, MyChilds
from django.contrib import admin
from datetime import datetime

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

@admin.register(ChildIsToddler)
class ChildIsToddlerAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        toddler_year = datetime.now().year - 3
        qs = Child.objects.filter(birth__year__gt=toddler_year)
        return qs

@admin.register(MyChilds)
class MyChildsAdmin(admin.ModelAdmin):
    raw_id_fields = ['father']

    def get_queryset(self, request):
        qs = Child.mychilds_objects.is_mine()
        return qs