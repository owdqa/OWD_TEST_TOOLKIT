from OWDTestToolkit.global_imports import *

import  getEpochSecsFromDateTime,\
        convertDay_NumToStr,\
        convertMonth_NumToStr,\
        setTimeToNow,\
        switch_24_12,\
        setTimeToSpecific,\
        getDateTimeFromEpochSecs,\
        waitForDeviceTimeToBe
        
class main ( 
            getEpochSecsFromDateTime.main,
            convertDay_NumToStr.main,
            convertMonth_NumToStr.main,
            setTimeToNow.main,
            switch_24_12.main,
            setTimeToSpecific.main,
            getDateTimeFromEpochSecs.main,
            waitForDeviceTimeToBe.main):

    def __init__(self):
        return

