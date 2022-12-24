import os
import stat
import logging
from build_repo_operation import repo_operation

# Class name is what is used at cli, so we defy convention here in favor of ease-of-use.
class push(repo_operation):
    def __init__(this, name="Push to a git repo"):
        super().__init__(name)

    # Required Builder method. See that class for details.
    def Build(this):
        this.RunCommand("git push")
