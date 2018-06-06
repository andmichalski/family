# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from datetime import datetime
from os import remove, path

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.test import TestCase
from django.urls import reverse

from tree.models import Child, Father
from tree import admin
from mock import patch, Mock, MagicMock


# Create your tests here.

class MyChildManagerTests(TestCase):

    def setUp(self):
        father1 = Father.objects.create(name="Andrzej", last_name="Michalski")
        father2 = Father.objects.create(name="Marcin", last_name="Magiera")
        father3 = Father.objects.create(name="Andrzej", last_name="Makarczuk")
        Child.objects.create(name="Jan", last_name="Michalski", birth=datetime(2014,9,11), father=father1)
        Child.objects.create(name="Franciszek", last_name="Magiera", birth=datetime(2018,1,5), father=father2)
        Child.objects.create(name="Tomasz", last_name="Makarczuk", birth=datetime(2016,11,15), father=father3)

    def test_manager_should_select_all_records_when_call_not_overriden_method(self):
        all_obj = Child.objects.all().count()
        all_obj_child_manager = Child.mychilds_objects.all().count()
        self.assertEqual(all_obj, all_obj_child_manager)

    def test_child_should_have_two_test_managers(self):
        self.assertTrue(Child.mychilds_objects)
        self.assertTrue(Child.objects)

    def test_child_should_be_mine(self):
        childs = Child.mychilds_objects.is_mine()
        child = childs.get(name="Jan")
        father = child.father.__str__()
        self.assertEqual(father, "Andrzej Michalski")

    def test_I_should_have_two_children(self):
        father = Father.objects.get(Q(name="Andrzej") & Q(last_name="Michalski"))
        Child.objects.create(name="Antoni", last_name="Michalski", birth=datetime(2017, 7, 12), father=father)
        childs = Child.mychilds_objects.is_mine()
        self.assertEqual(childs.count(), 2)

    def test_I_shold_not_have_children(self):
        Child.mychilds_objects.filter(Q(name="Jan") | Q(name="Antoni")).delete()
        childs = Child.mychilds_objects.is_mine()
        self.assertEqual(list(childs), [])

    def test_i_am_not_in_the_first_place_in_database(self):
        Father.objects.get(id=1).delete()
        self.assertRaises(ObjectDoesNotExist)


class ChildAdminTests(TestCase):

    def setUp(self):
        father1 = Father.objects.create(name="Andrzej", last_name="Michalski")
        father2 = Father.objects.create(name="Marcin", last_name="Pietraszek")
        Child.objects.create(name="Jan", last_name="Michalski", birth=datetime(2014, 9, 11), father=father1)
        Child.objects.create(name="Franciszek", last_name="Pietraszek", birth=datetime(2018, 1, 5), father=father2)
        Child.objects.create(name="Tomasz", last_name="Pietraszek", birth=datetime(2016, 11, 15), father=father2)
        admin_user = get_user_model().objects.create_superuser('admin', 'admin@example.com', 'password')
        self.client.login(username=admin_user.username, password='password')



    def test_should_change_last_name_michalski_when_call_queryset(self):
        url = reverse("admin:tree_child_changelist")
        childs = Child.objects.filter(father__last_name="Pietraszek")
        selected_ids = [child.pk for child in childs]

        data = {"action": "change_last_name_michalski", "_selected_action": selected_ids}

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(['Michalski', 'Michalski'], [c.last_name for c in Child.objects.filter(id__in=selected_ids)])

    def test_action_should_write_json_file(self):
        url = reverse("admin:tree_child_changelist")
        child = Child.objects.get(id=1)
        data = {"action": "export_to_json", "_selected_action": [child.pk]}
        self.client.post(url, data, follow=True)
        with open("json.txt", 'r') as f:
            json_file = f.read()

        self.assertTrue(path.isfile("json.txt"))
        remove("json.txt")

        json_output = [{"model": "tree.child", "pk": 1,
          "fields": {"name": "Jan", "last_name": "Michalski", "father": 1, "birth": "2014-09-11"}}]
        json_file = json.loads(json_file)
        self.assertEqual(json_output, json_file)

    def test_should_change_last_name(self):
        url = reverse("admin:tree_child_changelist")
        child = Child.objects.get(id=1)
        data = {"action": "change_lastname", "_selected_action": [child.pk], "_last_name": "Pietraszek"}
        response = self.client.post(url, data, follow=True)
        self.assertEqual("Pietraszek", Child.objects.get(id=1).last_name)

    @patch('tree.admin.ChildAdmin.message_user')
    def test_should_display_correct_message(self, mock_message):
        url = reverse("admin:tree_child_changelist")
        child = Child.objects.get(id=1)
        data = {"action": "change_lastname", "_selected_action": [child.pk], "_last_name": "Pietraszek"}
        response = self.client.post(url, data, follow=True)

        self.assertEqual(mock_message.call_count, 1)

        response.wsgi_request.method = "POST"
        mock_message.assert_has_calls(response.wsgi_request, unicode("Changed in selected records last name to Pietraszek"))
