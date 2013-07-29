from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def _GaiaApp(self, origin, name, frame, src):
        #
        # Private function to return a 'GaiaApp' object to use in UTILS.killApp() calls.
        #
        class GaiaApp(object):
            def __init__(self, origin, name, frame, src):
                self.frame = frame
                self.frame_id = frame
                self.src = src
                self.name = name
                self.origin = origin
            def __eq__(self, other):
                return self.__dict__ == other.__dict__
        
        x = GaiaApp(origin, name, frame, src)
        
        return x

    def killApp(self, p_name):
        #
        # Kills the app specified by p_name.
        #
        
        # Because these app aren't consistently named, or may be 'guessed'
        # incorrectly ...
        if p_name == "Dialer" or p_name == "Dialer" : p_name = "Phone"
        if p_name == "SMS"                          : p_name = "Messages"
        if p_name == "Market"                       : p_name = "Marketplace"
        
        self.logResult("info", "Killing app '%s' ..." % p_name)
        
        # Get the right DOM frame def. for this app.
        app_dom = self._getAppDOM(p_name)
        
        self.marionette.switch_to_frame()
        _frame = self.marionette.find_element("xpath", "//iframe[contains(@%s, '%s')]" % (app_dom[0], app_dom[1]))
        _src   = _frame.get_attribute("src")
        _origin= _src
        
        myApp = self._GaiaApp(_origin, p_name, _frame, _src)
        
        self.apps.kill(myApp)


        