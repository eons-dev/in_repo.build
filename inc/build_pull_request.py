import os
import stat
import logging
from build_repo_operation import repo_operation

# Class name is what is used at cli, so we defy convention here in favor of ease-of-use.
class pull_request(repo_operation):
    def __init__(this, name="Create a Pull Request"):
        super().__init__(name)

        this.optionalKWArgs['approve'] = False
        this.optionalKWArgs['close_branch'] = False

    # Required Builder method. See that class for details.
    def Build(this):
        this.RunCommand("git push")
