# coding:utf-8
# pylint: disable=protected-access, no-member

from types import SimpleNamespace
from unittest import TestCase
from unittest import main
from unittest import mock

from xpw import Profile
from xpw import SessionUser

from reflex_xpw_backend import AuthState
from reflex_xpw_backend import LoginState
from reflex_xpw_backend import LogoutState
from reflex_xpw_settings import CONFIG


def _call_event(handler, *args):
    return getattr(handler, "fn")(*args)


def _call_state_event(handler_name, instance, *args):
    return _call_event(getattr(type(instance), handler_name), instance, *args)


def _event_handler_name(event_spec):
    return getattr(getattr(event_spec, "handler"), "fn").__name__


def _event_var_value(var):
    return getattr(var, "_var_value")


class TestAuthState(TestCase):
    def setUp(self):
        self.state = AuthState(_reflex_internal_init=True)
        self.state.session_id = "old-session"
        self.state.secret_key = "old-secret"

    @mock.patch.object(CONFIG.access, "login")
    def test_activate_success(self, mock_login):
        user = SessionUser(session_id="sid", secret_key="sk")
        mock_login.return_value = user

        result = self.state.activate("demo", "test")

        self.assertIs(result, user)
        self.assertEqual(self.state.session_id, "sid")
        self.assertEqual(self.state.secret_key, "sk")

    @mock.patch.object(CONFIG.access, "login")
    def test_activate_failure(self, mock_login):
        self.state.session_id = "old-session"
        self.state.secret_key = "old-secret"
        mock_login.return_value = None

        result = self.state.activate("demo", "test")

        self.assertIsNone(result)
        self.assertEqual(self.state.session_id, "old-session")
        self.assertEqual(self.state.secret_key, "old-secret")

    @mock.patch.object(CONFIG.access, "logout")
    def test_deactivate_success(self, mock_logout):
        self.state.session_id = "sid"
        self.state.secret_key = "sk"
        mock_logout.return_value = True

        result = self.state.deactivate()

        self.assertTrue(result)
        self.assertNotEqual(self.state.secret_key, "sk")

    @mock.patch.object(CONFIG.access, "logout")
    def test_deactivate_failure(self, mock_logout):
        self.state.session_id = "sid"
        self.state.secret_key = "sk"
        mock_logout.return_value = False

        result = self.state.deactivate()

        self.assertFalse(result)
        self.assertEqual(self.state.secret_key, "sk")

    @mock.patch.object(CONFIG.access, "fetch")
    def test_identify_property(self, mock_fetch):
        expected = Profile(None, "demo")
        mock_fetch.return_value = expected

        result = self.state.identify

        self.assertIs(result, expected)
        mock_fetch.assert_called_once_with(session_id="old-session", secret_key="old-secret")

    @mock.patch.object(CONFIG.access, "check")
    def test_authenticated_property(self, mock_check):
        mock_check.return_value = True

        result = type(self.state).authenticated._fget(self.state)

        self.assertTrue(result)
        mock_check.assert_called_once_with(session_id="old-session", secret_key="old-secret")


class TestLoginState(TestCase):
    def setUp(self):
        self.fake = SimpleNamespace(
            identify=None,
            error_message="",
            is_hydrated=True,
            authenticated=False,
            router=SimpleNamespace(url=SimpleNamespace(path="/login", query_parameters={})),
            activate=lambda username, password: None,
            redirect=lambda: "REDIRECTED",
        )

    def test_on_submit_empty_username(self):
        result = LoginState.on_submit.fn(self.fake, {"username": "", "password": "secret"})

        self.assertEqual(self.fake.error_message, "The username is empty.")
        self.assertEqual(result.handler.fn.__name__, "fn")
        self.assertEqual(result.args[1][1]._var_value, "")

    def test_on_submit_empty_password(self):
        result = LoginState.on_submit.fn(self.fake, {"username": "demo", "password": ""})

        self.assertEqual(self.fake.error_message, "The password is empty.")
        self.assertEqual(result.handler.fn.__name__, "fn")
        self.assertEqual(result.args[1][1]._var_value, "")

    def test_on_submit_login_failure(self):
        self.fake.activate = lambda username, password: None

        result = LoginState.on_submit.fn(self.fake, {"username": "demo", "password": "test"})

        self.assertEqual(self.fake.error_message, "There was a problem logging in, please try again.")
        self.assertEqual(result.handler.fn.__name__, "fn")

    def test_on_submit_already_identified(self):
        self.fake.identify = Profile(None, "demo")
        self.fake.redirect = lambda: "REDIRECTED"

        result = LoginState.on_submit.fn(self.fake, {"username": "demo", "password": "test"})

        self.assertEqual(self.fake.error_message, "")
        self.assertEqual(result, "REDIRECTED")

    def test_on_submit_success(self):
        self.fake.activate = lambda username, password: SessionUser(session_id="sid", secret_key="sk")
        self.fake.redirect = lambda: "REDIRECTED"

        result = LoginState.on_submit.fn(self.fake, {"username": "demo", "password": "test"})

        self.assertEqual(self.fake.error_message, "")
        self.assertEqual(result, "REDIRECTED")

    def test_redirect_waits_for_hydration(self):
        fake = SimpleNamespace(
            is_hydrated=False,
            router=SimpleNamespace(url=SimpleNamespace(path="/login", query_parameters={})),
            authenticated=True,
            redirect=lambda: "REDIRECTED",
        )

        result = LoginState.redirect.fn(fake)

        self.assertEqual(result, "REDIRECTED")

    def test_redirect_to_source_when_authenticated_on_login(self):
        fake = SimpleNamespace(
            is_hydrated=True,
            router=SimpleNamespace(url=SimpleNamespace(path="/login", query_parameters={"src": "/home"})),
            authenticated=True,
        )

        result = LoginState.redirect.fn(fake)

        self.assertEqual(result.args[0][1]._var_value, "/home")

    def test_redirect_to_login_when_not_authenticated(self):
        fake = SimpleNamespace(
            is_hydrated=True,
            router=SimpleNamespace(url=SimpleNamespace(path="/dashboard", query_parameters={})),
            authenticated=False,
        )

        result = LoginState.redirect.fn(fake)

        self.assertEqual(result.args[0][1]._var_value, "/login?src=/dashboard")

    def test_redirect_no_action_when_login_path_and_not_authenticated(self):
        fake = SimpleNamespace(
            is_hydrated=True,
            router=SimpleNamespace(url=SimpleNamespace(path="/login", query_parameters={"src": "/home"})),
            authenticated=False,
        )

        result = LoginState.redirect.fn(fake)

        self.assertIsNone(result)


class TestLogoutState(TestCase):
    def test_on_submit_calls_deactivate(self):
        fake = SimpleNamespace(deactivate=lambda: True)

        result = LogoutState.on_submit.fn(fake)

        self.assertIsNone(result)

    def test_on_load_redirects_when_logout_path(self):
        fake = SimpleNamespace(
            router=SimpleNamespace(url=SimpleNamespace(path=CONFIG.routes.logout, query_parameters={"src": "/home"})),
            deactivate=lambda: True,
            redirect=lambda path: "REDIRECTED",
        )

        result = LogoutState.on_load.fn(fake)

        self.assertEqual(result.args[0][1]._var_value, "/home")

    def test_on_load_returns_none_when_not_logout(self):
        fake = SimpleNamespace(
            router=SimpleNamespace(url=SimpleNamespace(path="/other", query_parameters={"src": "/home"})),
            deactivate=lambda: True,
            redirect=lambda path: "REDIRECTED",
        )

        result = LogoutState.on_load.fn(fake)

        self.assertIsNone(result)


if __name__ == "__main__":
    main()
