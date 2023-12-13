from django.test import TestCase, Client
from django.urls import reverse,resolve
from clothes.views import *
from admins.models import *


class UrlsTest(TestCase):
    def test_homeurlisresolved(self):
        url=reverse('clothes:homepage')
        self.assertEqual(resolve(url).func,homepage)

    def test_showcatisresolved(self):
        url=reverse('clothes:show_categories')
        self.assertEqual(resolve(url).func,show_categories)

    def test_delete_clotheisresolved(self):
        url=reverse('clothes:delete_clothe', args=[2])
        self.assertEqual(resolve(url).func,delete_clothe)

class ViewsTest(TestCase):
    def test_home(self):
        self.client=Client()
        response= self.client.get(reverse('clothes:homepage'))
        self.assertEqual(response.status_code, 200)

    def test_show(self):
        self.client=Client()
        response= self.client.get(reverse('clothes:show_categories'))
        self.assertEqual(response.status_code, 200)

    


