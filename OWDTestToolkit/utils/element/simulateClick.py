
from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def simulateClick(self, element):
        self.marionette.execute_script("""
            /**
            * Helper method to simulate clicks on iFrames which is not currently
            *  working in the Marionette JS Runner.
            * @param {Marionette.Element} element The element to simulate the click on.
            **/

            var event = new MouseEvent('click', {
             'view': window,
             'bubbles': true,
             'cancelable': true
             });
            arguments[0].dispatchEvent(event);
        """, script_args=[element])