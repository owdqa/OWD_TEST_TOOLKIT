from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def waitForNewSMSPopup_by_number(self, p_num):
        #
        # Waits for a new SMS popup notification which
        # is from this 'p_num' number.
        #
        self.marionette.switch_to_frame()
        x = (DOM.Messages.new_sms_popup_num[0], DOM.Messages.new_sms_popup_num[1] % str(p_num))
        self.UTILS.waitForElements( x,
									"Popup message saying we have a new sms from " + str(p_num),
									True,
									30)

