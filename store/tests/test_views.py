from django.http import HttpRequest, request, response
from django.test import TestCase, Client, RequestFactory
from django.urls.base import reverse
from store.models import Category, Product
from django.contrib.auth.models import User
from unittest import skip
from store.views import all_products

class TestViewResponses(TestCase):
  def setUp(self):
    self.c = Client()
    self.factory = RequestFactory()
    Category.objects.create(name='django', slug='django')
    User.objects.create(username='admin')
    self.data1 = Product.objects.create(category_id=1, title='django beginners', created_by_id=1,
                                        slug='django-beginners', price='11', image='animal')

  def test_url_allowed_hosts(self):
    response = self.c.get('/')
    self.assertEqual(response.status_code, 200)

  def test_product_detail_url(self):
    response = self.c.get(reverse('store:product_detail', args=['django-beginners']))
    self.assertEqual(response.status_code, 200)

  def test_category_detail_url(self):
    response = self.c.get(reverse('store:category_list', args=['django']))
    self.assertEqual(response.status_code, 200)

  def test_homepage_html(self):
    request = HttpRequest()
    response = all_products(request)
    html = response.content.decode('utf8')
    self.assertIn('<title>Home</title>', html)
    self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
    self.assertEqual(response.status_code, 200)

  def test_view_function(self):
    request = self.factory.get('/item/django-beginners')
    response = all_products(request)
    html = response.content.decode('utf8')
    self.assertIn('<title>Home</title>', html)
    self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
    self.assertEqual(response.status_code, 200)
