import os
import stat
import logging
from distutils.dir_util import copy_tree
from ebbs import Builder

# Class name is what is used at cli, so we defy convention here in favor of ease-of-use.
class repo_operation(Builder):
    def __init__(this, name="Do something to a git repo"):
        super().__init__(name)

        this.clearBuildPath = False
        this.supportedProjectTypes = []

        this.requiredKWArgs.append('git_config')

        # Assume github creds, etc. are all setup.
        # Assume this.buildPath is the root of the repo.

    # Required Builder method. See that class for details.
    def DidBuildSucceed(this):
        # Assume Build() will throw errors.
        return True 

    # Override of Builder method. See that class for details.
    def PreBuild(this):
        super().PreBuild()

        # This should be unnecessary but just in case...
        this.RunCommand(f"git config --file {gitConfigPath}")