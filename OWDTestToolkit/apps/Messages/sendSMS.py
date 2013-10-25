from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def sendSMS(self):
		#
		# Just presses the 'send' button (assumes everything else is done).
		#
		sendBtn = self.UTILS.getElement(DOM.Messages.send_message_button, "Send sms button")
		sendBtn.tap()

		time.sleep(2) # (Give the spinner time to appear.)
		self.UTILS.waitForNotElements(DOM.Messages.message_sending_spinner, "'Sending' icon", True, 120)

		#
		# Check if we received the 'service unavailable' message.
		#
		try:
			self.wait_for_element_displayed(*DOM.Messages.service_unavailable_msg, timeout=2)
			x = self.UTILS.screenShotOnErr()
			self.UTILS.logResult("info", "'Service unavailable' message detected - unable to send sms!", x)
			return False
		except:
			pass

		return True