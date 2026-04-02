# coding:utf-8

from inspect import unwrap
from unittest import TestCase
from unittest import main

import reflex as rx

from reflex_xpw.defender import Defender


def original_page() -> rx.Component:
    return rx.text("Hello World")


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
        protected_page = Defender.login_required(original_page)
        self.assertIs(unwrap(protected_page), original_page)
        self.assertRaises(ValueError, Defender.login_required, protected_page)

    def test_no_login_required_wrapped(self):
        public_page = Defender.no_login_required(original_page)
        self.assertIs(unwrap(public_page), original_page)
        self.assertRaises(ValueError, Defender.no_login_required, public_page)


if __name__ == "__main__":
    main()
