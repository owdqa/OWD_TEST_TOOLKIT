from OWDTestToolkit.global_imports import *

import  disableAllNetworkSettings,\
        getNetworkConnection,\
        isNetworkTypeEnabled,\
        waitForNetworkItemEnabled,\
        waitForNetworkItemDisabled
        
class main ( 
            disableAllNetworkSettings.main,
            getNetworkConnection.main,
            isNetworkTypeEnabled.main,
            waitForNetworkItemEnabled.main,
            waitForNetworkItemDisabled.main):

    def __init__(self):
        return

