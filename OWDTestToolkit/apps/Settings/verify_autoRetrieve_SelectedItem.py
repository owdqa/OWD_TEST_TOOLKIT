from OWDTestToolkit.global_imports import *
from OWDTestToolkit.apps.Settings import *
from OWDTestToolkit.apps.Messages import *
	
class main(GaiaTestCase):

    def verify_autoRetrieve_SelectedItem(self, value):

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


        elif value=="on_with_r":
            x = self.UTILS.getElement(DOM.Settings.auto_retrieve_select_roaming, "On with roaming option in Auto Retireve Select")

        elif value=="on_without_r":
            x = self.UTILS.getElement(DOM.Settings.auto_retrieve_select_no_roaming, "On without roaming option in Auto Retireve Select")

        else:
            self.UTILS.logResult("info", "incorrect value received")
            self.UTILS.quitTest("FAILED: Incorrect parameter received in verify_autoRetrieve_SelectedItem()")


        #
        #Get option
        #
        y = x.get_attribute("aria-selected")

        #
        #Verifyin if the option is selected using the value true
        #
        self.UTILS.logResult("info", "Obtaining Selected option in Auto Retrieve select", y)
        self.UTILS.TEST( y=="true", "Checking value")

        #
        #Pressing ok button to leave select option
        #
        x = self.UTILS.getElement(DOM.Settings.ok_btn, "Messaging Settings button")
        x.tap()