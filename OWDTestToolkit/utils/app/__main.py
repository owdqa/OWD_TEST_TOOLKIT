from OWDTestToolkit.global_imports import *

import  findAppIcon,\
        launchAppViaHomescreen,\
        isAppInstalled,\
        uninstallApp,\
        setPermission
        
class main ( 
            findAppIcon.main,
            launchAppViaHomescreen.main,
            isAppInstalled.main,
            uninstallApp.main,
            setPermission.main):

    def __init__(self):
        return

