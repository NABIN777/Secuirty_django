from django.test import TestCase, Client
from django.urls import reverse
from clothes.views import *


class ViewsTest(TestCase):
    def test_home(self):
        self.client=Client()
        response= self.client.get(reverse('clothes:homepage'))
        self.assertEqual(response.status_code, 200)

    def test_show(self):
        self.client=Client()
        response= self.client.get(reverse('clothes:show_categories'))
        self.assertEqual(response.status_code, 200)

    def test_delete_clothe(self):
        self.client=Client()
        response= self.client.get(reverse('clothes:delete_clothe', args=[2]))
        self.assertEqual(response.status_code, 200)  
        
    def test_add_clothe(self):
        self.client=Client()
        response= self.client.get(reverse('clothes:add_clothe'))
        self.assertEqual(response.status_code, 200)      

