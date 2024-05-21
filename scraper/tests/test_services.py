from unittest import mock

from django.db import IntegrityError
from django.test import TestCase
from model_bakery import baker

from scraper import services


class GetLinksTest(TestCase):
    def setUp(self):
        self.url = "https://www.example.com"

    @mock.patch("scraper.services.logger.error")
    @mock.patch("scraper.services.requests.get")
    def test_get_links(self, p_get, p_error):
        p_get.return_value.text = "<html><head><title>Example Title</title></head><body><a href='https://www.example.com'>Example</a></body></html>"
        name, links = services.get_links(self.url)
        self.assertEqual(name, "Example Title")
        self.assertEqual(links, [("https://www.example.com", "Example")])
        p_error.assert_not_called()

    @mock.patch("scraper.services.logger.error")
    @mock.patch("scraper.services.requests.get")
    def test_get_links_no_title(self, p_get, p_error):
        p_get.return_value.text = (
            "<html><body><a href='https://www.example.com'>Example</a></body></html>"
        )
        name, links = services.get_links(self.url)
        self.assertEqual(name, "")
        self.assertEqual(links, [("https://www.example.com", "Example")])
        p_error.assert_not_called()

    @mock.patch("scraper.services.logger.error")
    @mock.patch("scraper.services.requests.get")
    def test_get_links_no_text(self, p_get, p_error):
        p_get.return_value.text = (
            "<html><body><a href='https://www.example.com'></a></body></html>"
        )
        name, links = services.get_links(self.url)
        self.assertEqual(name, "")
        self.assertEqual(links, [])
        p_error.assert_not_called()

    @mock.patch("scraper.services.logger.error")
    @mock.patch("scraper.services.requests.get")
    def test_get_links_request_error(self, p_get, p_error):
        p_get.side_effect = services.requests.RequestException
        with self.assertRaises(services.requests.RequestException):
            services.get_links(self.url)
        p_error.assert_called_once()


class CreatePageTest(TestCase):
    def setUp(self):
        self.url = "https://www.example.com"

    @mock.patch("scraper.services.logger.error")
    @mock.patch("scraper.services.get_links")
    def test_create_page(self, p_get_links, p_error):
        p_get_links.return_value = "Example Title", [
            ("https://www.example.com", "Example")
        ]
        services.create_page(self.url)
        self.assertEqual(services.Page.objects.count(), 1)
        self.assertEqual(services.Link.objects.count(), 1)
        p_error.assert_not_called()

    @mock.patch("scraper.services.logger.error")
    @mock.patch("scraper.services.get_links")
    def test_create_page_no_title(self, p_get_links, p_error):
        p_get_links.return_value = "", [("https://www.example.com", "Example")]
        services.create_page(self.url)
        self.assertEqual(services.Page.objects.count(), 1)
        self.assertEqual(services.Page.objects.first().name, self.url)
        self.assertEqual(services.Link.objects.count(), 1)
        p_error.assert_not_called()

    @mock.patch("scraper.services.logger.error")
    @mock.patch("scraper.services.get_links")
    def test_create_page_no_text(self, p_get_links, p_error):
        p_get_links.return_value = "Example Title", []
        services.create_page(self.url)
        self.assertEqual(services.Page.objects.count(), 1)
        self.assertEqual(services.Link.objects.count(), 0)
        p_error.assert_not_called()

    @mock.patch("scraper.services.logger.error")
    @mock.patch("scraper.services.get_links")
    def test_create_page_multiple_links(self, p_get_links, p_error):
        p_get_links.return_value = "Example Title", [
            ("https://www.example.com", "Example"),
            ("https://www.google.com", "Google"),
            ("https://www.example.com", "Example"),
        ]
        services.create_page(self.url)
        self.assertEqual(services.Page.objects.count(), 1)
        self.assertEqual(services.Link.objects.count(), 2)
        p_error.assert_not_called()

    @mock.patch("scraper.services.logger.error")
    @mock.patch("scraper.services.Link.objects.bulk_create")
    @mock.patch("scraper.services.get_links")
    def test_create_page_integrity_error(self, p_get_links, p_bulk_create, p_error):
        p_bulk_create.side_effect = IntegrityError
        p_get_links.return_value = "Example Title", [
            ("https://www.example.com", "Example"),
            ("https://www.google.com", "Google"),
        ]
        services.create_page(self.url)

        p_get_links.assert_called_once_with(self.url)
        p_bulk_create.assert_called_once()
        p_error.assert_called_once()

    @mock.patch("scraper.services.logger.info")
    @mock.patch("scraper.services.get_links")
    def test_create_page_already_exists(self, p_get_links, p_info):
        existing_page = baker.make("scraper.Page", url=self.url)
        services.create_page(self.url)
        p_get_links.assert_not_called()
        p_info.assert_called_once()
