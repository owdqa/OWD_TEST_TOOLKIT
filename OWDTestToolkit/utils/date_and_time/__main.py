from OWDTestToolkit.global_imports import *

import  getEpochSecsFromDateTime,\
        setTimeToNow,\
        switch_24_12,\
        setTimeToSpecific,\
        getDateTimeFromEpochSecs,\
        waitForDeviceTimeToBe,\
        waitForDisplayedTimeToBe
        
class main ( 
            getEpochSecsFromDateTime.main,
            setTimeToNow.main,
            switch_24_12.main,
            setTimeToSpecific.main,
            getDateTimeFromEpochSecs.main,
            waitForDeviceTimeToBe.main,
            waitForDisplayedTimeToBe.main):

    def __init__(self):
        return

