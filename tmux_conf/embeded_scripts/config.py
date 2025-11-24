"""a data class"""

from dataclasses import dataclass

from ..vers_check import VersionCheck


@dataclass(frozen=True)
class RunCmdConfig:
    """
    Docstring for RunCmdConfig
    """

    conf_file: str
    use_embedded: bool
    plugin_handler: str
    vers: VersionCheck  # the VersionCheck instance
