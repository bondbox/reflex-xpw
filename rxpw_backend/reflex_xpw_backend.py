from datetime import timedelta
from typing import Any
from typing import Dict
from typing import Optional

import reflex as rx
from reflex_xpw_settings import CONFIG
from xpw import Pass
from xpw import Profile
from xpw import SessionUser


class AuthState(rx.State):
    K_SESSION_ID = "SESSION_ID"
    K_SECRET_KEY = "SECRET_KEY"

    session_id: str = rx.Cookie(name=K_SESSION_ID)
    secret_key: str = rx.Cookie(name=K_SECRET_KEY)

    def activate(self, username: str, password: str) -> Optional[SessionUser]:  # noqa:E501
        if user := CONFIG.access.login(username, password, self.session_id, self.secret_key):  # noqa:E501
            self.session_id = user.session_id
            self.secret_key = user.secret_key
            return user

        return None

    def deactivate(self) -> bool:
        if CONFIG.access.logout(session_id=self.session_id, secret_key=self.secret_key):  # noqa:E501
            self.secret_key = Pass.random_generate(64).value
            return True

        return False

    @property
    def identify(self) -> Optional[Profile]:
        return CONFIG.access.fetch(session_id=self.session_id, secret_key=self.secret_key)  # noqa:E501

    @rx.var(cache=True, interval=timedelta(seconds=180), initial_value=False)
    def authenticated(self) -> bool:
        return CONFIG.access.check(session_id=self.session_id, secret_key=self.secret_key)  # noqa:E501


class LoginState(AuthState):
    """Handle login form"""

    error_message: str = ""

    @rx.event
    def on_submit(self, form_data: Dict[str, Any]):
        """Handle login form on_submit.

        Args:
            form_data: A dict of form fields and values.
        """
        if isinstance(self.identify, Profile):
            self.error_message = ""  # pragma: no cover
            return self.redirect()  # pragma: no cover

        # self.error_message = ""
        username: str = form_data["username"]
        password: str = form_data["password"]

        def alert(error_message: str):
            self.error_message = error_message
            return rx.set_value("password", "")

        if not username:
            return alert("The username is empty.")

        if not password:
            return alert("The password is empty.")

        if self.activate(username, password) is None:
            return alert("There was a problem logging in, please try again.")

        self.error_message = ""
        return self.redirect()

    @rx.event
    def redirect(self):
        """Redirect to the page if logged in, or to the login page if not."""
        if not self.is_hydrated:
            # wait until after hydration to ensure auth_token is known
            return self.redirect()  # pragma: no cover

        if (active_path := self.router.url.path) == CONFIG.routes.login and self.authenticated:  # noqa:E501
            source_path: str = self.router.url.query_parameters.get("src", "/")
            return rx.redirect(source_path)

        if active_path != CONFIG.routes.login and not self.authenticated:
            return rx.redirect(f"{CONFIG.routes.login}?src={active_path}")

        return None


class LogoutState(AuthState):

    @rx.event
    def on_submit(self):
        assert self.deactivate()

    @rx.event
    def on_load(self):
        if self.router.url.path == CONFIG.routes.logout and self.deactivate():
            source_path: str = self.router.url.query_parameters.get("src", "/")
            return rx.redirect(source_path)

        return None
