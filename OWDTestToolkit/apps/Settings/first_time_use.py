from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def first_time_use(self):
        #
        # Open First Time Experience
        #
        self.UTILS.waitForElements(DOM.Settings.device_info, "Waiting settings")
        x = self.UTILS.getElement(DOM.Settings.device_info, "Device information")
        x.tap()

        self.UTILS.waitForElements(DOM.Settings.device_info_header, "Waiting device information")
        x = self.UTILS.getElement(DOM.Settings.device_info_moreInfo, "Device more information")
        x.tap()

        self.UTILS.waitForElements(DOM.Settings.device_moreInfo_header, "Waiting device more information")
        x = self.UTILS.getElement(DOM.Settings.device_moreInfo_developer, "Device developers")
        x.tap()

        self.UTILS.waitForElements(DOM.Settings.device_developer_header, "Waiting device developer")
        x = self.UTILS.getElement(DOM.Settings.device_developer_FTU, "Launch first time use")
        x.tap()
