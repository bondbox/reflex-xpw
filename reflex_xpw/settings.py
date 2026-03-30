from dataclasses import dataclass
from dataclasses import field
from typing import Optional

from xkits_config import Settings


@dataclass
class Routes(Settings):
    login: str = "/login"
    logout: str = "/logout"


@dataclass
class Configuration(Settings):
    # Environment Variable Prefix
    ENVAR_PREFIX = "REFLEX_XPW"

    config_file: Optional[str] = None
    routes: Routes = field(default_factory=Routes)


CONFIG: Configuration = Configuration()
