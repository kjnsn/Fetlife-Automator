import unittest
import responses
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

from automator import FetlifeAutomator


class FetlifeAutomatorTest(unittest.TestCase):
    @responses.activate
    def test_login(self):
        main_page_html = read_fixture("main_page.txt")
        responses.add(responses.GET, 'https://fetlife.com/',
                      body=main_page_html, status=200)

        automator = FetlifeAutomator()

        responses.add(responses.GET, 'https://fetlife.com/settings/profile',
                      status=302, headers={'Location': 'https://fetlife.com/users/sign_in'})

        login_page_html = read_fixture("users_sign_in.txt")
        responses.add(responses.GET, 'https://fetlife.com/users/sign_in',
                      body=login_page_html, status=200)

        responses.add(responses.POST, 'https://fetlife.com/users/sign_in',
                      body=None, status=200)

        responses.add(responses.GET, 'https://fetlife.com/settings/profile',
                      body=read_fixture('logged_in_profile.txt'), status=200)

        logged_in, _ = automator.log_in('username', 'secret_password')
        self.assertTrue(logged_in)

    def test_send_message(self):
        main_page_html = read_fixture("main_page.txt")
        responses.add(responses.GET, 'https://fetlife.com/',
                      body=main_page_html, status=200)

        automator = FetlifeAutomator()

        responses.add(responses.GET, 'https://fetlife.com/settings/profile',
                      status=302, headers={'Location': 'https://fetlife.com/users/sign_in'})

        login_page_html = read_fixture("users_sign_in.txt")
        responses.add(responses.GET, 'https://fetlife.com/users/sign_in',
                      body=login_page_html, status=200)

        responses.add(responses.POST, 'https://fetlife.com/users/sign_in',
                      body=None, status=200)

        responses.add(responses.GET, 'https://fetlife.com/settings/profile',
                      body=read_fixture('logged_in_profile.txt'), status=200)

        logged_in, _ = automator.log_in('username', 'secret_password')
        self.assertTrue(logged_in)


def read_fixture(name):
    file = open(os.path.join(dir_path, "__fixtures__", name))
    contents = file.read()
    file.close()
    return contents
