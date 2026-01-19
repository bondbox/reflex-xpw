import reflex as rx

from .backend import LoginState


class BasePage():

    def build(self, children) -> rx.Component:
        return rx.center(
            children,
            height="100vh",
        )


class LoginPage(BasePage):
    ROUTE: str = "/login"
    TITLE: str = "Login"

    class LoginForm():

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
                    # login_error(),
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
                    rx.button("Sign in", size="3", width="100%"),
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

    def mount(self, app: rx.App) -> None:
        app.add_page(self.build, route=self.ROUTE, title=self.TITLE)

    def build(self) -> rx.Component:
        return super().build(
            rx.card(
                self.LoginForm.build(),
                width=["80vh", "60vh", "30vh"],   # mobile / tablet / desktop
            ),
        )
