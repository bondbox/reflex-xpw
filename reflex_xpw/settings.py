from dataclasses import dataclass
from dataclasses import field
from functools import cached_property
from typing import Optional

from xkits_config import Settings
from xpw import Account


@dataclass
class Routes(Settings):
    login: str = "/login"
    logout: str = "/logout"


@dataclass
class Configuration(Settings):
    # Environment Variable Prefix
    ENVAR_PREFIX = "REFLEX_XPW"

    config: Optional[str] = None
    routes: Routes = field(default_factory=Routes)

    @cached_property
    def access(self) -> Account:
        return Account.from_file(config=self.config)


CONFIG: Configuration = Configuration()
