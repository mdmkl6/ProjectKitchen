from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.auth import login
import time


class TestHomePage(StaticLiveServerTestCase):

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.browser = webdriver.Chrome(executable_path='functional_tests/chromedriver',chrome_options=chrome_options)
        user = User.objects.create(username='user1')
        user.set_password('haslo1234')
        user.save()         
        self.client=Client()
        self.client.login(username='user0', password='haslo1234')
        self.browser.get(self.live_server_url + reverse('login'))
        username = self.browser.find_element_by_name("username")
        username.clear()
        username.send_keys("user1")
        password = self.browser.find_element_by_name("password")
        password.clear()
        password.send_keys("haslo1234")
        self.browser.find_element_by_css_selector("button[class='btn btn-default']").click()

    def tearDown(self):
        self.browser.close()
    
    def test_sidebar_redirects_to_kitchen(self):
        new_url = self.live_server_url + reverse('kitchen')
        self.browser.find_element_by_link_text('Kitchen').click()
        self.assertEquals(self.browser.current_url, new_url)

    def test_home_login_redirects_to_shopping(self):
        new_url = self.live_server_url + reverse('shopping')
        self.browser.find_element_by_link_text('Shopping List').click()
        self.assertEquals(self.browser.current_url, new_url)

    def test_home_login_redirects_to_recipes(self):
        new_url = self.live_server_url + reverse('recipes')
        self.browser.find_element_by_link_text('Recipes').click()
        self.assertEquals(self.browser.current_url, new_url)

    def test_home_login_redirects_to_products(self):
        new_url = self.live_server_url + reverse('products')
        self.browser.find_element_by_link_text('Products').click()
        self.assertEquals(self.browser.current_url, new_url)

