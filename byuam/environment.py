import getpass
import os
import pwd

from . import pipeline_io

class Environment:

    PROJECT_ENV = "BYU_PROJECT_DIR"
    PIPELINE_FILENAME = ".project"

    PROJECT_NAME = "name"
    PRODUCTION_DIR = "production_dir"
    ASSETS_DIR = "assets_dir"
    SHOTS_DIR = "shots_dir"
    USERS_DIR = "users_dir"
    EMAIL_ADDRESS = "email_address"
    EMAIL_PASSWORD = "email_password"

    @staticmethod
    def create_new_dict(name, assets_dir, shots_dir, users_dir):
        datadict = {}
        datadict[Environment.PROJECT_NAME] = name
        datadict[Environment.ASSETS_DIR] = assets_dir
        datadict[Environment.SHOTS_DIR] = shots_dir
        datadict[Environment.USERS_DIR] = users_dir
        return datadict

    def __init__(self):
        """
        Creates an Environment instance from data in the .project file in the directory defined by the 
        environment variable $BYU_PROJECT_DIR. If this variable is not defined or the .project file does
        not exist inside it, an EnvironmentError is raised. Creates the workspace for the current user
        if it doesn't already exist.
        """
        self._project_dir = os.getenv(Environment.PROJECT_ENV)
        if self._project_dir is None:
            raise EnvironmentError(Environment.PROJECT_ENV + " is not defined")
        
        project_file = os.path.join(self._project_dir, Environment.PIPELINE_FILENAME)
        if not os.path.exists(project_file):
            raise EnvironmentError(project_file + " does not exist")
        self._datadict = pipeline_io.readfile(project_file)
        self._current_username = getpass.getuser()
        self._current_user_workspace = os.path.join(self.get_users_dir(), self._current_username)
        self._create_user(self._current_username)

    def get_project_name(self):
        """
        return the name of the current project
        """
        return self._datadict[Environment.PROJECT_NAME]

    def get_project_dir(self):
        """
        return the absolute filepath to the directory of the current project
        """
        return os.path.abspath(self._project_dir)

    def get_assets_dir(self):
        """
        return the absolute filepath to the assets directory of the current project
        """
        return os.path.abspath(self._datadict[Environment.ASSETS_DIR])

    def get_shots_dir(self):
        """
        return the absolute filepath to the shots directory of the current project
        """
        return os.path.abspath(self._datadict[Environment.SHOTS_DIR])

    def _create_user(self, username):
        workspace = os.path.join(self.get_users_dir(), username)
        if not os.path.exists(workspace):
            pipeline_io.mkdir(workspace)
        user_pipeline_file = os.path.join(workspace, User.PIPELINE_FILENAME)
        if not os.path.exists(user_pipeline_file):
            datadict = User.create_new_dict(username)
            pipeline_io.writefile(user_pipeline_file, datadict)
        # user = User(workspace)
        # return user

    def get_user(self, username=None):
        if username is None:
            username = self._current_username
        user_filepath = os.path.join(self.get_users_dir(), username)
        if not os.path.exists(user_filepath):
            raise EnvironmentError("no such user "+str(username))
        return User(user_filepath)

    def get_users_dir(self):
        """
        return the absolute filepath to the users directory of the current project
        """
        return os.path.abspath(self._datadict[Environment.USERS_DIR])

    def get_current_username(self):

        return self._current_username

    def get_user_workspace(self, username=None):
        """
        return the given users workspace. If no user is given, return the current user's workspace.
        """
        if username is not None:
            workspace = os.path.join(self.get_users_dir, username)
            if not os.path.exists(workspace):
                pipeline_io.mkdir(workspace)
            return workspace
        else:
            return self._current_user_workspace

    def sendmail(self, dst_addresses, subject, message):
        """
        send an email from the project email account to the given dst_addresses with the given subject and message.
        dst_addresses -- list of strings destination email addresses
        subject -- string subject line of the email
        message -- string body of the email
        """
        if(Environment.EMAIL_ADDRESS in self._datadict and Environment.EMAIL_PASSWORD in self._datadict):
            pipeline_io.sendmail(dst_addresses, subject, message,
                                 self._datadict[Environment.EMAIL_ADDRESS], 
                                 self._datadict[Environment.EMAIL_PASSWORD], 
                                 self.get_project_name()+" Support")


class User:
    """
    The User class holds information about a user, this will be used a lot more for the web site 
    """

    NAME = "name"
    EMAIL = "email"
    CSID = "csid"

    PIPELINE_FILENAME = ".user"

    @staticmethod
    def create_new_dict(username):
        datadict = {}
        datadict[User.CSID] = username
        name = pwd.getpwnam(username).pw_gecos
        datadict[User.NAME] = name
        datadict[User.EMAIL] = ""
        return datadict

    def __init__(self, filepath):
        self._filepath = filepath
        self._pipeline_file = os.path.join(self._filepath, self.PIPELINE_FILENAME)
        if not os.path.exists(self._pipeline_file):
            raise EnvironmentError("invalid user file: " + self._pipeline_file + " does not exist")
        self._datadict = pipeline_io.readfile(self._pipeline_file)
    
    def get_username(self):
        return self._datadict[self.CSID]    
    
    def get_fullname(self):
        return self._datadict[self.NAME]
        
    def get_email(self):
        return self._datadict[self.EMAIL]

    def has_email(self):
        return self._datadict[self.EMAIL] != ""
        
    def update_email(self, new_email): 
        self._datadict[self.EMAIL] =  new_email
        pipeline_io.writefile(self._pipeline_file, self._datadict)
        
    def update_fullname(self, new_name):
        self._datadict[self.NAME] = new_name
        pipeline_io.writefile(self._pipeline_file, self._datadict)


class Department:
    """
    Class describing departments that work on a project.
    """

    DESIGN = "design"
    MODEL = "model"
    RIG = "rig"
    ASSEMBLY = "assembly"
    LAYOUT = "layout"
    ANIM = "anim"
    TEXTURE = "texture"
    MATERIAL = "material"
    CFX = "cfx"
    FX = "fx"
    LIGHTING = "lighting"
    RENDER = "render"
    COMP = "comp"
    FRONTEND = [DESIGN, MODEL, RIG, TEXTURE, MATERIAL, ASSEMBLY]
    BACKEND = [LAYOUT, ANIM, CFX, FX, LIGHTING, RENDER, COMP]
    ALL = [DESIGN, MODEL, RIG, TEXTURE, MATERIAL, ASSEMBLY, LAYOUT, ANIM, CFX, FX, LIGHTING, RENDER, COMP]


class Status:
    """
    Class describing status levels for elements.
    """

    WAIT = "wait"
    READY = "ready"
    STARTED = "started"
    DONE = "done"
    ALL = [WAIT, READY, STARTED, DONE]

    def get_level(name):
        """
        given a status name return the equivalent level
        e.g. WAIT    -> 0
             READY   -> 1
             STARTED -> 2
             DONE    -> 3
        """
        return Status.ALL.index(status)

    def get_name(level):
        """
        given a status level return the equivalent name
        """
        return Status.ALL[level]


class AssetType:
    """
    Class describing types of assets.
    """

    CHARACTER = "character"
    SET = "set"
    PROP = "prop"
    ACCESSORY = "accessory"
    ALL = [CHARACTER, SET, PROP, ACCESSORY]

