from OWDTestToolkit.global_imports import *

import  clearGeolocPermission,\
        typeThis,\
        get_os_variable,\
        addFileToDevice,\
        selectFromSystemDialog,\
        setupDataConn,\
        setSetting
        
class main ( 
            clearGeolocPermission.main,
            typeThis.main,
            get_os_variable.main,
            addFileToDevice.main,
            selectFromSystemDialog.main,
            setupDataConn.main,
            setSetting.main):

    def __init__(self):
        return

