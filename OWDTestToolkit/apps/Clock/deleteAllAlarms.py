from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def deleteAllAlarms(self):
        #
        # Deletes all current alarms.
        #
        
        #
        # "self.data_layer.delete_all_alarms()" isn't workng at the moment, so...
        #
        while True:
            try:
            	self.wait_for_element_present(*DOM.Clock.alarm_preview_alarms, timeout=3)
                x = self.marionette.find_elements(*DOM.Clock.alarm_preview_alarms)
            except:
                #
                # No alarms returned, so just move on...
                #
                break
            else:
                if len(x) <= 0: break
                
                #
                # Some alarms - delete the first one (we need to reload the
                # list each time because it changes everytime we delete
                # an alarm).
                #
                x[0].tap()
                x = self.UTILS.getElement(DOM.Clock.alarm_delete_button, "Alarm delete button")
                x.tap()
                time.sleep(1)
        
