from os.path import dirname
from os.path import join
import sys

import reflex as rx

sys.path.insert(0, join(dirname(__file__), "..", "rxpw_backend"))
sys.path.insert(0, join(dirname(__file__), "..", "rxpw_frontend"))

from reflex_xpw_backend import LogoutState
from reflex_xpw_defender import Defender
from reflex_xpw_frontend import LoginPage
from reflex_xpw_frontend import LogoutPage


@rx.page(route="/about")
@Defender.no_login_required
def about_page() -> rx.Component:
    return rx.vstack(
        rx.text("Congratulations", id="text"),
        width=["100%", "80%", "60%"],   # mobile / tablet / desktop
        padding=["1em", "2em", "4em"],
    )


@rx.page(route="/hello")
@Defender.login_required
def hello_page() -> rx.Component:
    return rx.vstack(
        rx.text("Hello World", id="text"),
        width=["100%", "80%", "60%"],   # mobile / tablet / desktop
        padding=["1em", "2em", "4em"],
    )


@rx.page(route="/")
@Defender.login_required
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
