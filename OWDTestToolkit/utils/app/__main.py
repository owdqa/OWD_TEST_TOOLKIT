from OWDTestToolkit.global_imports import *

import  findAppIcon,\
        launchAppViaHomescreen,\
        isAppInstalled,\
        uninstallApp,\
        setPermission,\
        killApp,\
        switchToApp, \
        _getAppDOM
        
class main ( 
            findAppIcon.main,
            launchAppViaHomescreen.main,
            isAppInstalled.main,
            uninstallApp.main,
            setPermission.main,
            killApp.main,
            switchToApp.main,
            _getAppDOM.main):

    def __init__(self):
        return


