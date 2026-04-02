from functools import wraps
from inspect import unwrap
from typing import Any
from typing import Callable

import reflex as rx

from .backend import LoginState


class Defender:

    REQUIRE_LOGIN_ATTR = "__require_login__"

    @classmethod
    def validate_unwrapped(cls, func: Callable[..., Any]) -> None:
        if unwrap(func) is not func:
            raise ValueError(f"{func.__name__} is already wrapped.")

    @classmethod
    def login_required(cls, original_page: rx.app.ComponentCallable) -> rx.app.ComponentCallable:  # noqa:E501
        """Decorator to require authentication before rendering a page.

        If the user is not authenticated, then redirect to the login page.

        Args:
            original_page: The page to wrap.

        Returns:
            The wrapped page component.
        """
        cls.validate_unwrapped(func=original_page)

        @wraps(original_page)
        def protected_page(*args, **kwargs):
            return rx.cond(
                LoginState.is_hydrated & LoginState.authenticated,
                original_page(*args, **kwargs),
                rx.fragment(on_mount=LoginState.redirect),
            )

        setattr(protected_page, cls.REQUIRE_LOGIN_ATTR, True)
        return protected_page

    @classmethod
    def no_login_required(cls, original_page: rx.app.ComponentCallable) -> rx.app.ComponentCallable:  # noqa:E501
        """Decorator to mark the page as not requiring login.

        Args:
            original_page: The page to wrap.

        Returns:
            The wrapped page component.
        """
        cls.validate_unwrapped(func=original_page)

        @wraps(original_page)
        def public_page(*args, **kwargs):
            return original_page(*args, **kwargs)

        setattr(public_page, cls.REQUIRE_LOGIN_ATTR, False)
        return public_page
