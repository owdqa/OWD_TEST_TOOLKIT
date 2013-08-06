from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def checkMarionetteOK(self):
        #
        # Sometimes marionette session 'vanishes', so this makes sure we have one still.
        #
        try:
#             self.marionette.delete_session()
            if self.marionette.check_for_crash():
                self.marionette.start_session()
                self.logResult("info", "<i>(<b>NOTE:</b> The Marionette session crashed but was restarted successfully.)</i>")
        except:
            pass

