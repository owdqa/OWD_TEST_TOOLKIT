from OWDTestToolkit.global_imports import *
from OWDTestToolkit.apps.Settings import *
from OWDTestToolkit.apps.Messages import *
	
class main(GaiaTestCase):

    def configureMMSAutoRetrieve(self, value):

        #
        # Received value
        #
        #off = off option
        #on_with_r = On with roaming option
        #on_without_r = On without roaming

        #
        # Launch messages app.
        #
        self.launch()

        #
        # Tap on Messaging Settings button
        #
        x = self.UTILS.getElement(DOM.Settings.msg_settings, "Messaging Settings button")
        x.tap()

        #
        # Tap on Auto Retireve Select
        #
        x = self.UTILS.getElement(DOM.Settings.auto_retrieve_select_btn, "Auto Retireve Select")
        x.tap()

        #
        # Changing to top level frame
        #
        time.sleep(2)
        self.marionette.switch_to_frame()


        #
        # Selecting the specific option using que received parameter
        #
        if value=="off":
            x = self.UTILS.getElement(DOM.Settings.auto_retrieve_select_off, "Off option in Auto Retireve Select")
            x.tap()

        elif value=="on_with_r":
            x = self.UTILS.getElement(DOM.Settings.auto_retrieve_select_roaming, "On with roaming option in Auto Retireve Select")
            x.tap()

        elif value=="on_without_r":
            x = self.UTILS.getElement(DOM.Settings.auto_retrieve_select_no_roaming, "On without roaming option in Auto Retireve Select")
            x.tap()

        else:
             #self.UTILS.logResult("info", "incorrect value received")
            self.UTILS.quitTest("FAILED: Incorrect parameter received in configureMMSAutoRetrieve()")


        #
        #Tapping on OK button in auto Retrieve select
        #
        x = self.UTILS.getElement(DOM.Settings.ok_btn, "Tapping on OK button in auto Retrieve select")
        x.tap()

        #
        #Verifying if the option value has been selected
        #
        self.verify_autoRetrieve_SelectedItem(value)