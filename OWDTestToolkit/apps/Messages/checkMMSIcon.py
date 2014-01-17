from OWDTestToolkit.global_imports import *


class main(GaiaTestCase):

    def checkMMSIcon(self):
        #
        # Checks for the presence of the MMS icon
        #
        x = self.UTILS.getElement(DOM.Messages.mms_icon, "MMS Icon", True, 5, False)
        if x:
            self.UTILS.logResult("info", "MMS icon detected")

