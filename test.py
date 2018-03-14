from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from django.test import tag
from django.test import SimpleTestCase
from capstonemiddleware.settings import REPO_URL
import os
import shutil

#class MySeleniumTests(StaticLiveServerTestCase):
#    fixtures = ['user-data.json']
#
#    @classmethod
#    def setUpClass(cls):
#        super().setUpClass()
#        cls.selenium = WebDriver()
#        #cls.selenium.implicitly_wait(10)
#
#    @classmethod
#    def tearDownClass(cls):
#        cls.selenium.quit()
#        super().tearDownClass()
#
#    @tag('firefox')
#    def test_login(self):
#
#        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
#        username_input = self.selenium.find_element_by_name("username")
#        username_input.send_keys('myuser')
#        password_input = self.selenium.find_element_by_name("password")
#        password_input.send_keys('secret')
#        self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()

def resetRepo():
    for i in os.listdir(REPO_URL):
        shutil.rmtree(REPO_URL + i)

from io import BytesIO

class myTests(SimpleTestCase):
    @tag('a')
    def test_zzcreaterepo(self):
        response = self.client.post('/repo/createrepo/', {'reponame': 'aaa', 'secret' :'cccvzse'}, follow = True)
        #        print(response.status_code)
        #        print(response.content)
        print('zzzzzzzzzzzzz')

    @tag('a')
    def test_createrepo(self):
        response = self.client.post('/repo/createrepo/', {'reponame': 'aaa', 'secret' :'cccvzse'}, follow = True)
#        print(response.status_code)
#        print(response.content)
        print('zzzzzzzzzzzzz')

    @tag('b')
    def test_recognize(self):
        response = self.client.post('/repo/createrepo/', {'reponame': 'aaa', 'secret' :'cccvzse'})
        response = self.client.post('/repo/aaa/createclass/', {'secret' :'cccvzse', 'classname': 'name1'})
        response = self.client.post('/repo/aaa/name1/', {'img' :'cccvzse', 'classname': 'name1'})
        with open('2.png', 'rb') as f:
            response = self.client.post('/repo/aaa/name1/upload/', {'img': f, 'secret': 'cccvzse'})
        with open('2.png', 'rb') as f:
            response = self.client.post('/recognize/', {'img': f, 'server': 'anhAn'})
        print(response)


from django.test import Client
c = Client()
response = c.post('/repo/createrepo/', {'reponame': 'aaa', 'secret' :'cccvzse'}, follow = True)
print(response.status_code)
print(response.content)
#print(response.redirect_chain)
print(response.redirect_chain)
print(response.client)
