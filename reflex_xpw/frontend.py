from functools import wraps
from typing import Optional

import reflex as rx

from .backend import LoginState
from .backend import LogoutState
from .settings import CONFIG


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


class BasePage():  # pylint: disable=too-few-public-methods

    def center(self, *children: rx.Component) -> rx.Component:
        return rx.center(*children, height="100vh")


class LoginPage(BasePage):
    TITLE: str = "Login"

    class LoginForm():  # pylint: disable=too-few-public-methods

        @classmethod
        def build(cls) -> rx.Component:
            return rx.form(
                rx.vstack(
                    rx.heading(
                        "Login",
                        size="7",
                        width="100%",
                        text_align="center",
                    ),
                    rx.cond(
                        LoginState.error_message != "",
                        rx.callout(
                            LoginState.error_message,
                            icon="triangle_alert",
                            color_scheme="red",
                            role="alert",
                            width="100%",
                        ),
                    ),
                    rx.input(
                        size="3",
                        width="100%",
                        id="username",
                        name="username",
                        text_align="center",
                        placeholder="Username",
                    ),
                    rx.input(
                        size="3",
                        width="100%",
                        id="password",
                        name="password",
                        type="password",
                        text_align="center",
                        placeholder="Password",
                    ),
                    rx.button(
                        "Sign in",
                        size="3",
                        width="100%",
                        id="submit",
                        type="submit",
                    ),
                    # rx.center(
                    #     rx.link(
                    #         "Register",
                    #         on_click=RegistrationState.redir,
                    #     ),
                    #     width="100%",
                    # ),
                    spacing="3",
                ),
                on_submit=LoginState.on_submit,
            )

    def mount(self, app: rx.App, title: Optional[str] = None) -> None:
        app.add_page(self.build, route=CONFIG.routes.login, title=title or self.TITLE)  # noqa:E501

    def build(self) -> rx.Component:
        return rx.cond(
            LoginState.is_hydrated & LoginState.authenticated,
            rx.fragment(on_mount=LoginState.redirect),
            self.center(
                rx.card(
                    self.LoginForm.build(),
                    width=["80%", "50%", "20%"],   # mobile / tablet / desktop
                ),
            ),
        )


class LogoutPage(BasePage):
    TITLE: str = "Logout"

    def mount(self, app: rx.App, title: Optional[str] = None) -> None:
        app.add_page(self.build, route=CONFIG.routes.logout,
                     title=title or self.TITLE,
                     on_load=LogoutState.on_load)

    def build(self) -> rx.Component:
        return self.center(
            rx.cond(
                LoginState.is_hydrated & LoginState.authenticated,
                rx.heading("Unable to log out. Please try again.", id="prompt"),  # noqa:E501
                rx.heading("Successfully logged out.", id="prompt"),
            ),
        )
