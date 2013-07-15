from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def waitForNewSMSPopup_by_msg(self, p_msg):
        #
        # Waits for a new SMS popup notification which
        # matches this 'p_msg' string.
        #
        myIframe = self.UTILS.currentIframe()

        self.marionette.switch_to_frame()
        x = (DOM.Messages.new_sms_popup_msg[0], DOM.Messages.new_sms_popup_msg[1] % p_msg)
        self.UTILS.waitForElements( x,
									"Popup message saying we have a new sms containing '" + p_msg + "'",
									True,
									30)

        self.UTILS.switchToFrame("src", myIframe)
