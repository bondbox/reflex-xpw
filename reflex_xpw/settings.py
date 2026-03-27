from dataclasses import dataclass

from xkits_config import Settings


@dataclass
class Routes(Settings):
    # Environment Variable Prefix
    ENVAR_PREFIX = "REFLEX_ROUTES"

    login: str = "/login"
    logout: str = "/logout"


ROUTES: Routes = Routes()
