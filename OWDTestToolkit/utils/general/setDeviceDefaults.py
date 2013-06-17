from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def setDeviceDefaults(self):
        #
        # Set the device defaults before testing.
        #

        #
        # Default device to 'silent + vibrate'.
        #
        
        self.data_layer.set_setting("vibration.enabled", True)
        self.data_layer.set_setting("audio.volume.notification", 0)
        
        #
        # Default permissions.
        #
        self.apps.set_permission('Camera', 'geolocation', 'deny')
        self.apps.set_permission('Homescreen', 'geolocation', 'deny')

         
        #
        # Default timeout for element searches.
        #
        self.marionette.set_search_timeout(20)
         
        #
        # Set the current time to 'now'.
        #
        self.setTimeToNow()

