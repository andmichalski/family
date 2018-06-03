# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Child, Father, ChildIsToddler, MyChilds, UpdateLastNameForm
from django.contrib import admin
from datetime import datetime
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponseRedirect
from django import forms
from django.conf.urls import url
from django.template.response import TemplateResponse

# Register your models here.

class ChildInline(admin.TabularInline):
    model = Child

@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    search_fields = ["first_name"]
    list_display = ['name', 'last_name', 'birth']
    date_hierarchy = 'birth'
    raw_id_fields = ("father",)
    actions = ["change_last_name_michalski", "export_to_json", "change_lastname"]
    change_list_template = "admin/tree/child/change_view.html"

    def change_last_name_michalski(self, request, queryset):
        queryset.update(last_name="Michalski")

    change_last_name_michalski.short_description = "Changing last name to Michalski"

    def export_to_json(self, request, queryset):
        data = serializers.serialize("json", queryset)
        with open("json.txt", 'w') as f:
            f.write(data)

    export_to_json.short_description = "Export queryset to json"

    class LastNameForm(forms.Form):
        _last_name = forms.CharField(max_length=50)

    def change_lastname(self, request,queryset):
        form = None
        if 'apply' in request.POST:
            form = UpdateLastNameForm(request.POST)
            new_last_name = request.POST['_last_name']
            queryset.update(last_name=new_last_name)
            self.message_user(request, "Changed in selected records last name to {}".format(new_last_name))
            return HttpResponseRedirect(request.get_full_path())
        if not form:
            form = self.LastNameForm()
        return render(request, "admin/tree/child/change_last_name.html", {'users': queryset, 'form':form})

    change_lastname.short_description = "Change to custom last name"

    def get_urls(self):
        urls = super(ChildAdmin, self).get_urls()
        my_urls = [url(r'^childview', self.childview, name="childview"),
                   url(r'^childdetail', self.childdetailview, name="childdetail"),
                   url(r'^childlist', self.childlistview, name="childlist")]
        return my_urls + urls

    def childview(self, request):
        fathers = Father.objects.all()
        return TemplateResponse(request, "admin/tree/child/gen_tree.html", {'fathers': fathers})

    def childdetailview(self,request):
        if 'child' in request.GET:
            child = Child.objects.get(id=request.GET['child'])

        return TemplateResponse(request, "admin/tree/child/child_detail.html", {'child': child})

    def childlistview(self, request):
        if 'name' in request.GET:
            childs = Child.objects.filter(name=request.GET['name'])
        elif 'last_name' in request.GET:
            childs = Child.objects.filter(last_name=request.GET['last_name'])
        elif 'birth_user' in request.GET:
            _id = int(request.GET['birth_user'])
            _date = Child.objects.get(id=_id).birth
            childs = Child.objects.filter(birth=_date)
        elif 'father_user' in request.GET:
            _id = int(request.GET['father_user'])
            _father = Child.objects.get(id=_id).father
            childs = Child.objects.filter(father=_father)
        else:
            childs = Child.objects.all()
        return TemplateResponse(request, "admin/tree/child/child_list.html", {'childs': childs})

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