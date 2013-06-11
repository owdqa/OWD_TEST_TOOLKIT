from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def setTimezone(self, p_continent, p_city):
        #
        # Set the timezone.
        #
        self.UTILS.waitForElements(DOM.FTU.timezone, "Timezone area")
        
        # Continent.
        tz_buttons = self.UTILS.getElements(DOM.FTU.timezone_buttons, "Timezone buttons (for continent)")
        tz_buttons[0].click() # Must be 'clicked' not 'tapped'
        self.UTILS.selectFromSystemDialog(p_continent)

        # City.
        tz_buttons = self.UTILS.getElements(DOM.FTU.timezone_buttons, "Timezone buttons (for city)")
        tz_buttons[1].click() # Must be 'clicked' not 'tapped'
        self.UTILS.selectFromSystemDialog(p_city)

        self.UTILS.TEST(
            p_continent + "/" + p_city in self.UTILS.getElement(DOM.FTU.timezone_title, "Timezone title").text,
            "Locality is set up correctly")
