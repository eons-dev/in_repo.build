import os
import stat
import logging
from repo_operation import repo_operation

# Class name is what is used at cli, so we defy convention here in favor of ease-of-use.
class release(repo_operation):
    def __init__(this, name="Release from a git repo"):
        super().__init__(name)

        this.requiredPrograms.append('gh')

    # Required Builder method. See that class for details.
    def Build(this):
        this.RunCommand('''\
ver=$(gh release list | head -1 | awk '{print $1}' | awk -F. '{print $1"."$2"."$3+1}')
gh release create $ver -t $ver --generate-notes
''')
