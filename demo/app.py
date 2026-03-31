import reflex as rx

from reflex_xpw import LoginPage
from reflex_xpw import LogoutPage
from reflex_xpw import LogoutState
from reflex_xpw import require_login


@rx.page(route="/about")
def about_page() -> rx.Component:
    return rx.vstack(
        rx.text("Congratulations", id="text"),
        width=["100%", "80%", "60%"],   # mobile / tablet / desktop
        padding=["1em", "2em", "4em"],
    )


@rx.page(route="/hello")
@require_login
def hello_page() -> rx.Component:
    return rx.vstack(
        rx.text("Hello World", id="text"),
        width=["100%", "80%", "60%"],   # mobile / tablet / desktop
        padding=["1em", "2em", "4em"],
    )


@rx.page(route="/")
@require_login
def index_page() -> rx.Component:
    return rx.vstack(
        rx.text("Demo APP", id="text"),
        rx.button("Logout", id="logout", on_click=LogoutState.on_submit),
        width=["100%", "80%", "60%"],   # mobile / tablet / desktop
        padding=["1em", "2em", "4em"],
    )


app = rx.App()


LoginPage().mount(app)
LogoutPage().mount(app)
