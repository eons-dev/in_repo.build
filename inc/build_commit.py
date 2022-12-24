import os
import stat
import logging
from build_repo_operation import repo_operation

# Class name is what is used at cli, so we defy convention here in favor of ease-of-use.
class commit(repo_operation):
    def __init__(this, name="Commit to a git repo"):
        super().__init__(name)

        this.optionalKWArgs['message'] = "update with ebbs"

    # Required Builder method. See that class for details.
    def Build(this):
        this.RunCommand(f'''\
git add .
git commit -S -m '{this.message}'
''')
