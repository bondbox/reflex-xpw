# coding:utf-8

from inspect import unwrap
from unittest import TestCase
from unittest import main

import reflex as rx

from reflex_xpw.defender import login_required


class TestDefender(TestCase):

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

    def test_login_required_wrapped(self):

        def original_page() -> rx.Component:
            return rx.text("Hello World")

        protected_page = login_required(original_page)
        self.assertIs(unwrap(protected_page), original_page)
        self.assertRaises(ValueError, login_required, protected_page)


if __name__ == "__main__":
    main()
