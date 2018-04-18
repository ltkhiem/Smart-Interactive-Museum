import json
from unittest import TestCase

from django.test import tag, TransactionTestCase
from rest_framework.test import APITestCase
import os
import shutil

from django.test import SimpleTestCase
from django.test import tag

from capstonemiddleware.settings import REPO_URL


# class MySeleniumTests(StaticLiveServerTestCase):
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


class myTests(SimpleTestCase):
    @tag('a')
    def test_zzcreaterepo(self):
        response = self.client.post('/repo/createrepo/', {'reponame': 'aaa', 'secret': 'cccvzse'}, follow=True)
        #        print(response.status_code)
        #        print(response.content)
        print('zzzzzzzzzzzzz')

    @tag('a')
    def test_createrepo(self):
        response = self.client.post('/repo/createrepo/', {'reponame': 'aaa', 'secret': 'cccvzse'}, follow=True)
        #        print(response.status_code)
        #        print(response.content)
        print('zzzzzzzzzzzzz')

    @tag('b')
    def test_recognize(self):
        response = self.client.post('/repo/createrepo/', {'reponame': 'aaa', 'secret': 'cccvzse'})
        response = self.client.post('/repo/aaa/createclass/', {'secret': 'cccvzse', 'classname': 'name1'})
        response = self.client.post('/repo/aaa/name1/', {'img': 'cccvzse', 'classname': 'name1'})
        with open('2.png', 'rb') as f:
            response = self.client.post('/repo/aaa/name1/upload/', {'img': f, 'secret': 'cccvzse'})
        with open('2.png', 'rb') as f:
            response = self.client.post('/recognize/', {'img': f, 'server': 'anhAn'})
        print(response)


class TuTestCase(APITestCase):
    def test_register(self):
        response = self.client.post('/register/',
                                    {'username': 'nvtu1996', 'password1': 'tutututu', 'password2': 'tutututu'})
        print(response)

    def test_get_auth_token(self):
        response = self.client.post('/get_auth_token/', {'username': 'nvtu1996', 'password': 'tutututu'})
        print(response.content)

    @tag('tu')
    def test_create_repo_and_class(self):
        # Test register new user
        response = self.client.post('/register/', {'username': 'nvtu', 'password1': 'tuninh1996', 'password2': 'tuninh1996'})
        print('/register/ --- {}'.format(response.content))

        # Test get token key
        response = self.client.post('/get_auth_token/', {'username': 'nvtu', 'password': 'tuninh1996'})
        content = json.loads(str(response.content)[2:-1])
        token = "Token " + str(content['token'])
        print('/get_auth_token/ --- {}'.format(response.content))

        # Test create repo
        self.client.credentials(HTTP_AUTHORIZATION=token)
        my_repo_name = 'nvtuRepo'
        response = self.client.post('/repo/create_repo/', {'name': my_repo_name})
        print('/repo/create_repo/ --- {}'.format(response.content))

        # Test create class
        my_class_name = 'TuClass'
        response = self.client.post('/repo/{}/create_class/'.format(my_repo_name), {'name': my_class_name})
        print('/repo/{}/create_class/ --- {}'.format(my_repo_name, response.content))

# from django.test import Client
#
# c = Client()
# response = c.post('/repo/createrepo/', {'reponame': 'aaa', 'secret': 'cccvzse'}, follow=True)
#
# print(response.status_code)
# print(response.content)
# # print(response.redirect_chain)
# print(response.redirect_chain)
# print(response.client)
