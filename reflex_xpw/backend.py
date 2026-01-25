from typing import Any
from typing import Dict
from typing import Optional

import reflex as rx
from xpw import Account
from xpw import Profile
from xpw import Secret
from xpw import SessionID
from xpw import SessionUser


class AuthState(rx.State):
    K_SESSION_ID = "SESSION_ID"
    K_SECRET_KEY = "SECRET_KEY"

    @property
    def session_id(self) -> str:
        return rx.get_cookie(key=self.K_SESSION_ID) or SessionID.generate()

    @property
    def secret_key(self) -> str:
        return rx.get_cookie(key=self.K_SECRET_KEY) or Secret.generate().key

    def activate(self, username: str, password: str) -> Optional[SessionUser]:  # noqa:E501
        if user := access.login(username, password, self.session_id, self.secret_key):  # noqa:E501
            rx.set_cookie(key=self.K_SESSION_ID, value=user.session_id)
            rx.set_cookie(key=self.K_SECRET_KEY, value=user.secret_key)
            return user

    def deactivate(self) -> bool:
        if access.logout(session_id=self.session_id, secret_key=self.secret_key):  # noqa:E501
            rx.remove_cookie(key=self.K_SESSION_ID)
            rx.remove_cookie(key=self.K_SECRET_KEY)

    @property
    def identify(self) -> Optional[Profile]:
        return access.fetch(session_id=self.session_id, secret_key=self.secret_key)  # noqa:E501


class LoginState(AuthState):
    """Handle login form"""

    error_message: str = ""

    @rx.event
    def on_submit(self, form_data: Dict[str, Any]):
        """Handle login form on_submit.

        Args:
            form_data: A dict of form fields and values.
        """
        self.error_message = ""
        username: str = form_data["username"]
        password: str = form_data["password"]

        print(f"session_id: {self.session_id}")
        print(f"secret_key: {self.secret_key}")
        print(f"Login: {username} {password}")
        # print(self.router.url.query)
        # print(self.router.url.path)

        # with rx.session() as session:
        #     user = session.exec(
        #         select(LocalUser).where(LocalUser.username == username)
        #     ).one_or_none()
        # if user is not None and not user.enabled:
        #     self.error_message = "This account is disabled."
        #     return rx.set_value("password", "")
        # if (
        #     user is not None
        #     and user.id is not None
        #     and user.enabled
        #     and password
        #     and user.verify(password)
        # ):
        #     # mark the user as logged in
        #     self._login(user.id)
        # else:
        #     self.error_message = "There was a problem logging in, please try again."
        #     return rx.set_value("password", "")
        # self.error_message = ""
        # return LoginState.redirect()  # type: ignore

    @rx.event
    def redirect(self):
        """Redirect to the redirect_to route if logged in, or to the login page if not."""
        if not self.is_hydrated:
            # wait until after hydration to ensure auth_token is known
            return LoginState.redirect()  # type: ignore

        # current_route = self.router.url.path
        # if not self.is_authenticated and current_route != routes.LOGIN_ROUTE:
        #     self.redirect_to = current_route
        #     return rx.redirect(routes.LOGIN_ROUTE)
        # elif self.is_authenticated and current_route == routes.LOGIN_ROUTE:
        #     return rx.redirect(self.redirect_to or "/")
