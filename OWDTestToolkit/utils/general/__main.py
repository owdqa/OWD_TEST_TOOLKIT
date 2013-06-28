from OWDTestToolkit.global_imports import *

import  clearGeolocPermission,\
        typeThis,\
        setTimeToNow,\
        get_os_variable,\
        addFileToDevice,\
        selectFromSystemDialog,\
        setupDataConn,\
        switch_24_12,\
        setSetting
        
class main ( 
            clearGeolocPermission.main,
            typeThis.main,
            setTimeToNow.main,
            get_os_variable.main,
            addFileToDevice.main,
            selectFromSystemDialog.main,
            setupDataConn.main,
            switch_24_12.main,
            setSetting.main):

    def __init__(self):
        return

