from typing import Any
from typing import Dict

import reflex as rx


class AuthState(rx.State):
    pass


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
        print(f"Login: {username} {password}")
        print(self.router.url.query)
        print(self.router.url.path)
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
