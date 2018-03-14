from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from django.test import tag
from django.test import SimpleTestCase

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



from django.test import Client
c = Client()
response = c.post('/repo/createrepo/', {'reponame': 'aaa', 'secret' :'cccvzse'}, follow = True)
print(response.status_code)
print(response.content)
#print(response.redirect_chain)
print(response.redirect_chain)
print(response.client)
