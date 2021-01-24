from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import time


class TestHomePage(StaticLiveServerTestCase):

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.browser = webdriver.Chrome(executable_path='functional_tests/chromedriver',chrome_options=chrome_options)

    def tearDown(self):
        self.browser.close()

    def test_home_non_login(self):
        self.browser.get(self.live_server_url)
        class_name = self.browser.find_element_by_class_name('center')
        self.assertEquals(class_name.find_element_by_tag_name('h1').text, "Create your kitchen")

    def test_non_login_sidebar_redirects_to_login(self):
        self.browser.get(self.live_server_url)
        new_url = self.live_server_url + reverse('login')
        self.browser.find_element_by_link_text('Log In').click()
        self.assertEquals(self.browser.current_url, new_url)

    def test_non_login_sidebar_redirects_to_signup(self):
        self.browser.get(self.live_server_url)
        new_url = self.live_server_url + reverse('signup')
        self.browser.find_element_by_link_text('Sign Up').click()
        self.assertEquals(self.browser.current_url, new_url)

   