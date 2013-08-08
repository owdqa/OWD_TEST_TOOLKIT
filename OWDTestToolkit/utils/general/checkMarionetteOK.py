from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def checkMarionetteOK(self):
        #
        # Sometimes marionette session 'vanishes', so this makes sure we have one still.
        #
        try:
            self.marionette.delete_session()
        except:
            pass

        try:
            self.marionette.start_session()
            self.logResult("info", "<i>(The Marionette session was restarted to avoid a possible crash.)</i>")
        except:
            pass

