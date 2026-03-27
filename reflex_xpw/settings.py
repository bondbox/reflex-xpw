from dataclasses import dataclass
from typing import Optional

from xkits_config import Settings


@dataclass
class Routes(Settings):
    # Environment Variable Prefix
    ENVAR_PREFIX = "REFLEX_ROUTES"

    login: str = "/login"
    logout: str = "/logout"


ROUTES: Routes = Routes()


@dataclass
class Configuration(Settings):
    # Environment Variable Prefix
    ENVAR_PREFIX = "REFLEX_XPW"

    config_file: Optional[str] = None


CONFIG: Configuration = Configuration()
