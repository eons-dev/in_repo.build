import os
import stat
import logging
from distutils.dir_util import copy_tree
from ebbs import Builder


# Class name is what is used at cli, so we defy convention here in favor of ease-of-use.
class in_repo(Builder):
    def __init__(this, name="Do stuff in a git repo!"):
        super().__init__(name)

        this.clearBuildPath = False

        this.requiredKWArgs.append("git_repos")

        this.optionalKWArgs["git_provider"] = "github"
        this.optionalKWArgs["git_email"] = None
        this.optionalKWArgs["git_username"] = None
        this.optionalKWArgs["git_password"] = None
        this.optionalKWArgs["gpg_key_id"] = None
        this.optionalKWArgs["gpg_key_data"] = None
        this.optionalKWArgs["gpg_key_file"] = "gpg.key"
        this.optionalKWArgs["gpg_key_password"] = None

        this.supportedProjectTypes = []

        this.requiredPrograms.extend([
            "git",
            "gpg",
            "expect"
        ])

    # Required Builder method. See that class for details.
    def DidBuildSucceed(this):
        return True  # TODO: how would we even know?

    # Required Builder method. See that class for details.
    def Build(this):
        # this.SetupGPG() #NOT READY. See FIXME in method.
        
        this.WriteGitConfig()

        for repo in this.git_repos:
            this.RunCommand(f"git clone --recursive {repo}")

    def SetupGPG(this):
        #TODO: check if this.gpg_key_id exists.

        if (not os.stat(this.gpg_key_file).st_size and this.gpg_key_data)
            keyFile = this.CreateFile(this.gpg_key_file)
            keyFile.write(this.gpg_key_data)
            keyFile.close()
            if (not os.stat(this.gpg_key_file).st_size):
                logging.error(f"Unable to create gpg key file: {this.gpg_key_file}")
                #TODO: Raise error.
                return
        
        if (not os.stat(this.gpg_key_file).st_size):
            logging.debug(f"Proceeding without key signing.")
            return
        
        this.RunCommand(f"gpg --import {this.gpg_key_file}")
        #FIXME: Somehow, we need the keyid output from the above command. Perhaps a "captureOutput" flag?
        this.RunCommand(f"expect -c 'spawn gpg --edit-key {this.gpg_key_file} trust quit; send \"5\ry\r\"; expect eof'") #Command taken from: https://unix.stackexchange.com/questions/184947/how-to-import-secret-gpg-key-copied-from-one-machine-to-another


    def WriteGitConfig(this):
        gitCredsPath = Path("./git.creds")
        gitcreds = this.CreateFile(gitCredsPath)
        gitcreds.write(f'''protocol=https
username={this.git_username}
password={this.git_password}
''')
        gitcreds.close()

        gitConfigPath = str(Path("./git.config").resolve())
        gitconfig = this.CreateFile(gitConfigPath)
        gitconfig.write(f'''[user]
    email = {this.git_email}
    name = {this.git_username}
''')

        if (this.gpg_key_id):
            gitconfig.write(f'''signingkey = {this.gpg_key_id}
[commig]
    gpgsign = true
''')

        gitconfig.write(f'''[credential]
    helper = store --file {str(gitCredsPath.resolve())}
    helper = cache --timeout=14400
''')
        gitconfig.close()

        #Make sure subsequent builders can access the config we created.
        os.putenv("git_config", gitConfigPath)

        this.RunCommand(f"git config --file {gitConfigPath}")
        