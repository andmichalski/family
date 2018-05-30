# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Child, Father, ChildIsToddler, MyChilds, UpdateLastNameForm
from django.contrib import admin
from datetime import datetime
from django.shortcuts import render
from django.core import serializers

# Register your models here.

class ChildInline(admin.TabularInline):
    model = Child

@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    search_fields = ["first_name"]
    list_display = ['name', 'last_name', 'birth']
    date_hierarchy = 'birth'
    raw_id_fields = ("father",)
    actions = ["change_last_name_michalski", "export_to_json"]

    def change_last_name_michalski(self, request, queryset):
        queryset.update(last_name="Michalski")

    change_last_name_michalski.short_description = "Changing last name to Michalski"

    def export_to_json(self, request, queryset):
        data = serializers.serialize("json", queryset)
        with open("json.txt", 'w') as f:
            f.write(data)

    export_to_json.short_description = "Export queryset to json"

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