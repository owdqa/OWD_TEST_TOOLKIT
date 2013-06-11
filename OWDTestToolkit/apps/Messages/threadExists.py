from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def threadExists(self, p_num):
		#
		# Verifies that a thread exists for this number (just return True or False).
		#
		boolOK=False
		try:
			thread_el = ("xpath", DOM.Messages.thread_selector_xpath % p_num)
			x = self.marionette.find_element(*thread_el)
			boolOK=x
		except:
			boolOK=False
		    
		return boolOK

