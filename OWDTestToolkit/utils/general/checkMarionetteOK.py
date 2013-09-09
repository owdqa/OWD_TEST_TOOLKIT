from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def checkMarionetteOK(self):
        #
        # Sometimes marionette session 'vanishes', so this makes sure we have one still.
        # <b>NOTE: </b>This leaves you in the 'top -level' iframe, so you'll need to navigate back
        # to your frame after running this. 
        #
#         try:
#             self.marionette.delete_session()
#         except:
#             pass

        try:
            self.marionette.start_session()
            self.logResult("info", "<i>(*** The Marionette session was restarted due to a possible crash. ***)</i>")
        except:
            pass

