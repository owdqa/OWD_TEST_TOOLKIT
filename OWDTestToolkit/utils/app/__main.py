from OWDTestToolkit.global_imports import *

import  findAppIcon,\
        launchAppViaHomescreen,\
        isAppInstalled,\
        uninstallApp,\
        setPermission,\
        killApp,\
        switchToApp, \
        _getAppFrame,\
        addAppToDock
        
class main ( 
            findAppIcon.main,
            launchAppViaHomescreen.main,
            isAppInstalled.main,
            uninstallApp.main,
            setPermission.main,
            killApp.main,
            switchToApp.main,
            _getAppFrame.main,
            addAppToDock.main):

    def __init__(self):
        return


