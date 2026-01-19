from dataclasses import dataclass

from xkits_config import Settings


@dataclass
class Routes(Settings):
    ENV_PREFIX = "REFLEX_ROUTES"

    login: str = "/login"
    logout: str = "/logout"


ROUTES: Routes = Routes()
