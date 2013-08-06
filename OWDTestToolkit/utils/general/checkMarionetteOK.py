from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def checkMarionetteOK(self):
        #
        # Sometimes marionette session 'vanishes', so this makes sure we have one still.
        #
        try:
            self.marionette.start_session()
            self.logResult("info", "<i>(<b>NOTE:</b> Marionette session crashed, but it was restarted successfully.)</i>")
        except:
            pass

