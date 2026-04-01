from functools import wraps

import reflex as rx

from .backend import LoginState


def require_login(page: rx.app.ComponentCallable) -> rx.app.ComponentCallable:
    """Decorator to require authentication before rendering a page.

    If the user is not authenticated, then redirect to the login page.

    Args:
        page: The page to wrap.

    Returns:
        The wrapped page component.
    """

    @wraps(page)
    def protected_page(*args, **kwargs):
        return rx.cond(
            LoginState.is_hydrated & LoginState.authenticated,
            page(*args, **kwargs),
            rx.fragment(on_mount=LoginState.redirect),
        )

    return protected_page
