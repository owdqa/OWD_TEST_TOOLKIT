from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def _getAppDOM(self, p_name):
        #
        # Private function that returns the frame_locator for an app by name.
        #
        if   p_name == "Browser"    : app_dom = DOM.Browser.frame_locator
        elif p_name == "Calculator" : app_dom = DOM.Calculator.frame_locator
        elif p_name == "Calendar"   : app_dom = DOM.Calendar.frame_locator
        elif p_name == "Camera"     : app_dom = DOM.Camera.frame_locator
        elif p_name == "Clock"      : app_dom = DOM.Clock.frame_locator
        elif p_name == "Contacts"   : app_dom = DOM.Contacts.frame_locator
        elif p_name == "Phone"      : app_dom = DOM.Dialer.frame_locator
        elif p_name == "Email"      : app_dom = DOM.Email.frame_locator
        elif p_name == "Facebook"   : app_dom = DOM.Facebook.frame_locator
        elif p_name == "FTU"        : app_dom = DOM.FTU.frame_locator
        elif p_name == "Gallery"    : app_dom = DOM.Gallery.frame_locator
        elif p_name == "Home"       : app_dom = DOM.Home.frame_locator
        elif p_name == "Keyboard"   : app_dom = DOM.Keyboard.frame_locator
        elif p_name == "Marketplace": app_dom = DOM.Market.frame_locator
        elif p_name == "Messages"   : app_dom = DOM.Messages.frame_locator
        elif p_name == "Settings"   : app_dom = DOM.Settings.frame_locator
        elif p_name == "Video"      : app_dom = DOM.Video.frame_locator
        
        return app_dom