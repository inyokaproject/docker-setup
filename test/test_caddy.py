#!/usr/bin/python

import unittest
import http.client
import ssl
import random

from typing import Final

BASE_DOMAIN: Final = 'ubuntuusers.localhost'


class CaddyCommonTest(unittest.TestCase):
    domainname = BASE_DOMAIN

    def setUp(self):
        ssl_c= ssl.SSLContext() # WARNING: this 'will not have certificate validation nor hostname checking enabled by default' (is ok for local testing, otherwise not)
        port = random.randint(1_100, 65_000)
        self.conn = http.client.HTTPSConnection(self.domainname, source_address=('127.0.0.1', port), context=ssl_c)
        #self.conn.set_debuglevel(1)

    def tearDown(self):
        self.conn.close()

    def test_no_server_header(self):
        self.conn.request("HEAD", "/")
        r = self.conn.getresponse()
        self.assertNotIn('Server', r.getheaders())

    def test_hsts_header(self):
        self.conn.request("HEAD", "/")
        r = self.conn.getresponse()
        self.assertEqual(r.getheader('Strict-Transport-Security'), 'max-age=31536000;')

    def test_x_content_type_header(self):
        self.conn.request("HEAD", "/")
        r = self.conn.getresponse()
        self.assertEqual(r.getheader('X-Content-Type-Options'), 'nosniff')

    def test_max_request_body_size(self):
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/plain"}
        with self.assertRaises(ConnectionResetError):
           self.conn.request("POST", "/", body='issue' * int(1E7), headers=headers)

    def test_favicon(self):
        self.conn.request("HEAD", "/favicon.ico")
        r = self.conn.getresponse()
        self.assertEqual(r.status, 200)
        self.assertEqual(r.getheader('Content-Type'), "image/vnd.microsoft.icon")

    def test_robotstxt(self):
        self.conn.request("HEAD", "/robots.txt")
        r = self.conn.getresponse()
        self.assertEqual(r.status, 200)
        self.assertEqual(r.getheader('Content-Type'), "text/plain; charset=utf-8")


class ForumTest(CaddyCommonTest):
    domainname = f'forum.{BASE_DOMAIN}'


class PasteTest(CaddyCommonTest):
    domainname = f'paste.{BASE_DOMAIN}'


class WikiTest(CaddyCommonTest):
    domainname = f'wiki.{BASE_DOMAIN}'


class PlanetTest(CaddyCommonTest):
    domainname = f'planet.{BASE_DOMAIN}'


class IkhayaTest(CaddyCommonTest):
    domainname = f'ikhaya.{BASE_DOMAIN}'


class NotFoundMixin:

    def test_404_template(self):
        self.conn.request("GET", "/fgjkbfgb_doesnotexist")
        r = self.conn.getresponse()
        self.assertEqual(r.status, 404)
        self.assertIn('404: Not Found', r.read().decode())
        self.assertEqual(r.getheader('Cache-Control'), 'no-cache')


class MediaTest(CaddyCommonTest, NotFoundMixin):

    domainname = f'media.{BASE_DOMAIN}'

    def test_cache_control_404(self):
        self.conn.request("HEAD", "/")
        r = self.conn.getresponse()
        self.assertEqual(r.status, 404)
        self.assertEqual(r.getheader("Cache-Control"), "no-cache")

    def test_cache_control(self):
        self.conn.request("HEAD", "/favicon.ico")
        r = self.conn.getresponse()
        self.assertEqual(r.status, 200)
        self.assertEqual(r.getheader("Cache-Control"), "max-age=2592000")

    # TODO needs a media file that is always present
    def test_generic_content_type(self):
        self.conn.request("HEAD", "/portal/files/ubuntuusers.png")
        r = self.conn.getresponse()
        self.assertEqual(r.status, 200)
        self.assertEqual(r.getheader("Content-Type"), "application/octet-stream")

    def test_linkmap_content_type(self):
        self.conn.request("HEAD", f"https://{self.domainname}/linkmap/linkmap-0a47f39ae20f45b95b654a09e127ca90.css")
        r = self.conn.getresponse()
        self.assertEqual(r.status, 200)
        self.assertEqual(r.getheader("Content-Type"), "text/css; charset=utf-8")


class StaticTest(CaddyCommonTest, NotFoundMixin):

    domainname = f'static.{BASE_DOMAIN}'

    def test_cache_control_404(self):
        self.conn.request("HEAD", "/")
        r = self.conn.getresponse()
        self.assertEqual(r.status, 404)
        self.assertEqual(r.getheader("Cache-Control"), "no-cache")

    def test_cache_control(self):
        self.conn.request("HEAD", "/favicon.ico")
        r = self.conn.getresponse()
        self.assertEqual(r.status, 200)
        self.assertEqual(r.getheader("Cache-Control"), "max-age=2592000")

    def test_access_control(self):
        self.conn.request("HEAD", "/")
        r = self.conn.getresponse()
        self.assertEqual(r.getheader("Access-Control-Allow-Origin"), "*")


class WWWPrefixTest(CaddyCommonTest):

    domainname = f'www.{BASE_DOMAIN}'

    def setUp(self):
        super().setUp()

        self.no_www = self.domainname.replace('www.', '', 1)

    def test_redirect(self):
        self.conn.request("HEAD", "/")
        r = self.conn.getresponse()
        self.assertEqual(r.status, 302)
        self.assertEqual(r.getheader('Location'), f"https://{self.no_www}/")

    def test_error_template(self):
        self.conn.request("HEAD", "/fgjkbfgb_doesnotexist")
        r = self.conn.getresponse()
        self.assertEqual(r.status, 302)
        self.assertEqual(r.getheader('Location'), f"https://{self.no_www}/fgjkbfgb_doesnotexist")

    def test_favicon(self):
        self.conn.request("HEAD", "/favicon.ico")
        r = self.conn.getresponse()
        self.assertEqual(r.status, 302)
        self.assertEqual(r.getheader('Location'), f"https://{self.no_www}/favicon.ico")

    def test_robotstxt(self):
        self.conn.request("HEAD", "/robots.txt")
        r = self.conn.getresponse()
        self.assertEqual(r.status, 302)
        self.assertEqual(r.getheader('Location'), f"https://{self.no_www}/robots.txt")


class WWWPrefixForumTest(WWWPrefixTest):
    domainname = f'www.forum.{BASE_DOMAIN}'


class WWWPrefixPasteTest(WWWPrefixTest):
    domainname = f'www.paste.{BASE_DOMAIN}'


class WWWPrefixWikiTest(WWWPrefixTest):
    domainname = f'www.wiki.{BASE_DOMAIN}'


class WWWPrefixPlanetTest(WWWPrefixTest):
    domainname = f'www.planet.{BASE_DOMAIN}'


class WWWPrefixIkhayaTest(WWWPrefixTest):
    domainname = f'www.ikhaya.{BASE_DOMAIN}'


class WWWPrefixStaticTest(WWWPrefixTest):
    domainname = f'www.static.{BASE_DOMAIN}'


class WWWPrefixMediaTest(WWWPrefixTest):
    domainname = f'www.media.{BASE_DOMAIN}'


if __name__ == '__main__':
    unittest.main()
