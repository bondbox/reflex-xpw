# coding:utf-8

from os.path import dirname
from os.path import join
import sys
from unittest import TestCase
from unittest import main

from xpw import Account

sys.path.insert(0, join(dirname(__file__), "..", "..", "rxpw_backend"))

from reflex_xpw_settings import CONFIG
from reflex_xpw_settings import Routes


class TestConfiguration(TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_check_default(self):
        self.assertIsNone(CONFIG.config)
        self.assertIsInstance(CONFIG.routes, Routes)
        self.assertIsInstance(CONFIG.access, Account)

    def test_access_cached_property(self):
        self.assertIs(CONFIG.access, CONFIG.access)


if __name__ == "__main__":
    main()
