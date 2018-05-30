# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from tree.models import Child, Father
from datetime import datetime
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
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

