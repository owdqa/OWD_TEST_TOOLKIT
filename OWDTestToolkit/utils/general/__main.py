from OWDTestToolkit.global_imports import *

import  clearGeolocPermission,\
        createIncomingCall,\
        typeThis,\
        get_os_variable,\
        insertContact,\
        addFileToDevice,\
        selectFromSystemDialog,\
        setupDataConn,\
        setSetting,\
        checkMarionetteOK
        
class main ( 
            clearGeolocPermission.main,
            createIncomingCall.main,
            typeThis.main,
            get_os_variable.main,
            insertContact.main,
            addFileToDevice.main,
            selectFromSystemDialog.main,
            setupDataConn.main,
            setSetting.main,
            checkMarionetteOK.main):

    def __init__(self):
        return

