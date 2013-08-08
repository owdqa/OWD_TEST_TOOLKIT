from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def threadExists(self, p_num):
		#
		# Verifies that a thread exists for this number (returns True or False).
		#
		boolOK=False
		try:
			self.wait_for_element_present("xpath", DOM.Messages.thread_selector_xpath % p_num, 1)
			boolOK=True
		except:
			boolOK=False
		    
		return boolOK

