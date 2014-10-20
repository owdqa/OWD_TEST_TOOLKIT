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

    def acceptNETWPINMessage(self):
        #
        # Click on the Accept button
        #
        x = self.UTILS.element.getElement(DOM.OMACP.CP_Accept_Button, "Accept button")
        x.tap()

    def cancelNETWPINMessage(self):
        #
        # Click on the Close button
        #
        x = self.UTILS.element.getElement(DOM.OMACP.CP_Close_Button, "Close button")
        x.tap()

        screenshot = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult('info', "Screenshot", screenshot)

        x = self.UTILS.element.getElement(DOM.OMACP.CP_Cancel_Message, "Cancel Message")
        self.UTILS.test.TEST(x.text == "The message has not been processed yet, do you really want to quit?",
                        "Cancel Message Text")

        x = self.UTILS.element.getElement(DOM.OMACP.CP_Quit_Button, "Quit button")
        x.tap()

    def cancelOMACPStorage(self, CP_PinNumber):
        #
        # Introduce the PIN number, then click on the Accept button
        #
        self.UTILS.iframe.switchToFrame(*DOM.OMACP.frame_locator)
        self.UTILS.general.typeThis(DOM.OMACP.CP_Windows_Pin, "PIN field", CP_PinNumber, p_no_keyboard=False,
                            p_validate=False, p_clear=False, p_enter=True)

        x = self.UTILS.element.getElement(DOM.OMACP.CP_Accept_Button, "Accept button")
        x.tap()

        #
        # Click on Cancel button and finish
        #
        x = self.UTILS.element.getElement(DOM.OMACP.CP_Cancel_Button, "Cancel button")
        x.tap()

    def clickOMACPNotification(self, p_num):
        #
        # Click new sms in the home page status bar notificaiton.
        #
        self.UTILS.reporting.logResult("info", "Clicking statusbar notification of new CP from " + p_num + " ...")

        #
        # Switch to the 'home' frame to click the notifier.
        #
        self.marionette.switch_to_frame()
        self.UTILS.statusbar.displayStatusBar()
        x = (DOM.Messages.statusbar_new_sms[0], DOM.Messages.statusbar_new_sms[1].format(p_num))
        x = self.UTILS.element.getElement(x, "Statusbar notification for " + p_num)
        x.tap()

        #
        # Switch back to the messaging app.
        #
        time.sleep(2)

        self.marionette.switch_to_frame(self.apps.displayed_app.frame_id)

    def storeOMACPSettings(self, pin):
        #
        # Introduce the PIN number, then click on the Accept button
        #
        self.UTILS.iframe.switchToFrame(*DOM.OMACP.frame_locator)
        self.UTILS.general.typeThis(DOM.OMACP.CP_Windows_Pin, "PIN field", pin, p_no_keyboard=True,
                            p_validate=False, p_clear=False, p_enter=True)

        x = self.UTILS.element.getElement(DOM.OMACP.CP_Accept_Button, "Accept button")
        x.tap()

        #
        # Click on Store button and finish
        #
        x = self.UTILS.element.getElement(DOM.OMACP.CP_Store_Button, "Store button")
        x.tap()

        x = self.UTILS.element.getElement(DOM.OMACP.CP_OTA_Message, "Message")
        self.UTILS.test.TEST(x, "Stored OTA message")

        x = self.UTILS.element.getElement(DOM.OMACP.CP_Finish_Button, "Finish button")
        x.tap()
        time.sleep(3)
