from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def _getAppFrame(self, p_name):
        #
        # Private function that returns the frame_locator for an app by name.
        #
        if   p_name == "Browser"    : app_frame = DOM.Browser.frame_locator
        elif p_name == "Calculator" : app_frame = DOM.Calculator.frame_locator
        elif p_name == "Calendar"   : app_frame = DOM.Calendar.frame_locator
        elif p_name == "Camera"     : app_frame = DOM.Camera.frame_locator
        elif p_name == "Clock"      : app_frame = DOM.Clock.frame_locator
        elif p_name == "Contacts"   : app_frame = DOM.Contacts.frame_locator
        elif p_name == "Phone"      : app_frame = DOM.Dialer.frame_locator
        elif p_name == "Email"      : app_frame = DOM.Email.frame_locator
        elif p_name == "Facebook"   : app_frame = DOM.Facebook.frame_locator
        elif p_name == "FTU"        : app_frame = DOM.FTU.frame_locator
        elif p_name == "Gallery"    : app_frame = DOM.Gallery.frame_locator
        elif p_name == "Home"       : app_frame = DOM.Home.frame_locator
        elif p_name == "Keyboard"   : app_frame = DOM.Keyboard.frame_locator
        elif p_name == "Marketplace": app_frame = DOM.Market.frame_locator
        elif p_name == "Messages"   : app_frame = DOM.Messages.frame_locator
        elif p_name == "Settings"   : app_frame = DOM.Settings.frame_locator
        elif p_name == "Video"      : app_frame = DOM.Video.frame_locator
        
        return app_frame