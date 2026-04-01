from functools import wraps
from inspect import unwrap

import reflex as rx

from .backend import LoginState


def login_required(original_page: rx.app.ComponentCallable) -> rx.app.ComponentCallable:  # noqa:E501
    """Decorator to require authentication before rendering a page.

    If the user is not authenticated, then redirect to the login page.

    Args:
        page: The page to wrap.

    Returns:
        The wrapped page component.
    """
    if unwrap(original_page) is not original_page:
        raise ValueError(f"{original_page.__name__} is already wrapped.")

    @wraps(original_page)
    def protected_page(*args, **kwargs):
        return rx.cond(
            LoginState.is_hydrated & LoginState.authenticated,
            original_page(*args, **kwargs),
            rx.fragment(on_mount=LoginState.redirect),
        )

    setattr(protected_page, "__require_login__", True)
    return protected_page


def no_login_required(original_page: rx.app.ComponentCallable) -> rx.app.ComponentCallable:  # noqa:E501
    """Decorator to mark the page as not requiring login.

    Args:
        page: The page to wrap.

    Returns:
        The wrapped page component.
    """
    if unwrap(original_page) is not original_page:
        raise ValueError(f"{original_page.__name__} is already wrapped.")

    @wraps(original_page)
    def public_page(*args, **kwargs):
        return original_page(*args, **kwargs)

    setattr(public_page, "__require_login__", False)
    return public_page
