from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def goBack(self):
        #
        # Tap the back icon (gets a bit complicated sometimes, because
        # there's sometimes more than one match for this icon DOM reference).
        #
        time.sleep(0.5)
        x = self.UTILS.getElements(DOM.Settings.back_button, "Back buttons", False)
        boolOK = False
        for i in x:
        	try:
        		i.tap()
        		boolOK = True
        		break
        	except:
        		pass
        	
        if not boolOK:
        	self.UTILS.logResult(False, "Tap the 'back' icon to return to the parent screen.")
        	return False
        
        time.sleep(1)
        return True