from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def checkStatusbarIcon(self):
        #
        # Check for the little alarm bell icon in the statusbar of the
        # homescreen.
        #
        self.marionette.switch_to_frame()
        boolOK = True
        try:
            self.UTILS.waitForElements(DOM.Clock.alarm_notifier, "Alarm notification", True, 20, False)
        except:
            boolOK = False
        
        return boolOK
                
