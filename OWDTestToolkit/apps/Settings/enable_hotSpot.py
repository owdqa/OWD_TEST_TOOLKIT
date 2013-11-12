from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def enable_hotSpot(self):
    #
    # Enable hotspot (internet sharing) - asusmes Settings app is already open.
    #
        self.UTILS.logResult("info", "<u>Enabling hotspot ...</u>")

        #
        # Is it already enabled?
        #
        x = self.UTILS.getElement(DOM.Settings.hotspot_settings, "Hotspot settings")
        if x.get_attribute("disabled") == "true":
            self.UTILS.logResult("info", "Hotspot is already enabled.")
            return True

        x = self.UTILS.getElement(DOM.Settings.hotspot_switch, "Hotspot switch")
        x.tap()
        time.sleep(1)

        #
        # Wait for the hotspot to begin.
        #
        boolOK1 = False
        _tries = 10
        for i in range(0,_tries):
            x = self.marionette.find_element(*DOM.Settings.hotspot_settings)
            if x.get_attribute("disabled") == "true":
                #
                # It's done.
                #
                boolOK1 = True
                break
            time.sleep(0.5)

        boolOK2 = self.UTILS.isIconInStatusBar(DOM.Statusbar.hotspot)

        self.UTILS.TEST(boolOK1, "Hotspot settings are disabled (because 'hotspot' is now running).")
        self.UTILS.TEST(boolOK2, "Hotspot icon is present in the status bar.")
