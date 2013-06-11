from OWDTestToolkit.global_imports import *

import  clearGeolocPermission,\
        typeThis,\
        setTimeToNow,\
        get_os_variable,\
        addFileToDevice,\
        selectFromSystemDialog,\
        switch_24_12
        
class main ( 
            clearGeolocPermission.main,
            typeThis.main,
            setTimeToNow.main,
            get_os_variable.main,
            addFileToDevice.main,
            selectFromSystemDialog.main,
            switch_24_12.main):

    def __init__(self):
        return

