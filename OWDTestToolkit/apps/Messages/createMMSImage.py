from OWDTestToolkit.global_imports import *


class main(GaiaTestCase):

    def createMMSImage(self):

        attach = self.UTILS.getElement(DOM.Messages.attach_button, "Attach button")
        attach.tap()

        self.marionette.switch_to_frame()

        gallery = self.UTILS.getElement(DOM.Messages.mms_from_gallery, "From gallery")
        gallery.tap()

        self.UTILS.switchToFrame(*DOM.Gallery.frame_locator)