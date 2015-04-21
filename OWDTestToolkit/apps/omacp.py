import time
from OWDTestToolkit import DOM


class OMACP(object):

    def __init__(self, p_parent):
        self.apps = p_parent.apps
        self.data_layer = p_parent.data_layer
        self.parent = p_parent
        self.marionette = p_parent.marionette
        self.UTILS = p_parent.UTILS

    def launch(self):
        #
        # Launch the app.
        #
        self.app = self.apps.launch(self.__class__.__name__)
        self.UTILS.element.waitForNotElements(DOM.GLOBAL.loading_overlay, self.__class__.__name__ +
                                              " app - loading overlay")
        return self.app

    def accept_netwpin_message(self):
        #
        # Click on the Accept button
        #
        accept_btn = self.UTILS.element.getElement(DOM.OMACP.CP_Accept_Button, "Accept button")
        accept_btn.tap()

    def cancel_netwpin_message(self):
        #
        # Click on the Close button
        #
        close_btn = self.UTILS.element.getElement(DOM.OMACP.CP_Close_Button, "Close button")
        close_btn.tap()

        screenshot = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult('info', "Screenshot", screenshot)

        cancel_msg = self.UTILS.element.getElement(DOM.OMACP.CP_Cancel_Message, "Cancel Message")
        self.UTILS.test.test(cancel_msg.text == _("The message has not been processed yet, do you really want to quit?"),
                        "Cancel Message Text")

        quit_btn = self.UTILS.element.getElement(DOM.OMACP.CP_Quit_Button, "Quit button")
        quit_btn.tap()

    def cancel_omacp_storage(self, pin):
        #
        # Introduce the PIN number, then click on the Accept button
        #
        self.UTILS.iframe.switchToFrame(*DOM.OMACP.frame_locator)
        self.UTILS.general.typeThis(DOM.OMACP.CP_Windows_Pin, "PIN field", pin, p_no_keyboard=False,
                            p_validate=False, p_clear=False, p_enter=True)

        accept_btn = self.UTILS.element.getElement(DOM.OMACP.CP_Accept_Button, "Accept button")
        accept_btn.tap()

        #
        # Click on Cancel button and finish
        #
        cancel_btn = self.UTILS.element.getElement(DOM.OMACP.CP_Cancel_Button, "Cancel button")
        cancel_btn.tap()

    def store_omacp_settings(self, pin):
        #
        # Introduce the PIN number, then click on the Accept button
        #
        self.UTILS.iframe.switchToFrame(*DOM.OMACP.frame_locator)
        self.UTILS.general.typeThis(DOM.OMACP.CP_Windows_Pin, "PIN field", pin, p_no_keyboard=True,
                            p_validate=False, p_clear=False, p_enter=True)

        accept_btn = self.UTILS.element.getElement(DOM.OMACP.CP_Accept_Button, "Accept button")
        accept_btn.tap()

        #
        # Click on Store button and finish
        #
        store_btn = self.UTILS.element.getElement(DOM.OMACP.CP_Store_Button, "Store button")
        store_btn.tap()

        msg = self.UTILS.element.getElement(DOM.OMACP.CP_OTA_Message, "Message")
        self.UTILS.test.test(msg, "Stored OTA message")

        finish_btn = self.UTILS.element.getElement(DOM.OMACP.CP_Finish_Button, "Finish button")
        finish_btn.tap()
        time.sleep(3)
