from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def getThreadText(self, p_num):
        #
        # Returns the preview text for the thread for this number (if it exists),
        # or False if either the thread doesn't exist or can't be found.
        #
        if self.threadExists(p_num):
 			x = self.UTILS.getElements(DOM.Messages.threads_list, "Threads")
 			
 			for i in x:
 				try:
 					y = i.find_element("xpath", ".//p[text()='%s']" % p_num)
					z = i.find_element("xpath", ".//span[@class='body-text']")
					return z.text
				except:
					pass

        return False
        
