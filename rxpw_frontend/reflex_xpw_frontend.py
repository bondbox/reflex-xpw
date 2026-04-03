from typing import Optional

import reflex as rx
from reflex_xpw_backend import LoginState
from reflex_xpw_backend import LogoutState
from reflex_xpw_settings import CONFIG


class BasePage():  # pylint: disable=too-few-public-methods

    def center(self, *children: rx.Component) -> rx.Component:
        return rx.center(*children, height="100vh")


class LoginPage(BasePage):

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

    @property
    def title(self) -> str:
        return "Login"

    def mount(self, app: rx.App, title: Optional[str] = None) -> None:
        app.add_page(self.build, route=CONFIG.routes.login, title=title or self.title)  # noqa:E501

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

    @property
    def title(self) -> str:
        return "Logout"

    def mount(self, app: rx.App, title: Optional[str] = None) -> None:
        app.add_page(self.build, route=CONFIG.routes.logout,
                     title=title or self.title,
                     on_load=LogoutState.on_load)

    def build(self) -> rx.Component:
        return self.center(
            rx.cond(
                LoginState.is_hydrated & LoginState.authenticated,
                rx.heading("Unable to log out. Please try again.", id="prompt"),  # noqa:E501
                rx.heading("Successfully logged out.", id="prompt"),
            ),
        )
