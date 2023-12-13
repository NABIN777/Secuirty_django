from django.test import TestCase, Client
from django.urls import reverse,resolve
from clothes.views import *
from clothes.models import *



class modelsTest(TestCase):
    def test_category(self):
        c=Category(name='test')
        self.assertEqual(c.name,'test')
        c.save()
        self.assertEqual(c.name,'test')
        c.delete()
        self.assertEqual(c.name,'test')
        c.name='test2'
        self.assertEqual(c.name,'test2')
        c.save()
        self.assertEqual(c.name,'test2')
        c.delete()
        self.assertEqual(c.name,'test2')
        c.name='test3'
        self.assertEqual(c.name,'test3')
        c.save()
        self.assertEqual(c.name,'test3')
        c.delete()
        self.assertEqual(c.name,'test3')
        c.name='test4'
        self.assertEqual(c.name,'test4')
        c.save()
        self.assertEqual(c.name,'test4')
        c.delete()
        self.assertEqual(c.name,'test4')
        c.name='test5'
        self.assertEqual(c.name,'test5')
        c.save()
        self.assertEqual(c.name,'test5')
        c.delete()
        self.assertEqual(c.name,'test5')
        c.name='test6'
        self.assertEqual(c.name,'test6')
        c.save()
        self.assertEqual(c.name,'test6')
        c.delete()
        self.assertEqual(c.name,'test6')
        c.name='test7'
        self.assertEqual(c.name,'test7')
        c.save()
        self.assertEqual(c.name,'test7')
        c.delete()
        self.assertEqual(c.name,'test7')
        c.name='test8'
        self.assertEqual(c.name,'test8')