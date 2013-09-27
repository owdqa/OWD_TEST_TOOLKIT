from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def getAwesomeList(self, p_tabName):
        #
        # Retrns a list of elements from the awesomescreen tabs
        # (<b>p_tabName</b> must be one of: "top sites", "bookmarks", "history").
        # Theses elements have some handy attributes:<br>
        # <br>
        # href: containing the url (may have 'extra' info in it, so use 'x in y').<br>
        # .find_element("tag name","h5"): contains the title of this page.
        #
        _details={}
        _details["top_sites"] = {"tab":DOM.Browser.awesome_top_sites_tab, "links":DOM.Browser.awesome_top_sites_links}
        _details["bookmarks"] = {"tab":DOM.Browser.awesome_bookmarks_tab, "links":DOM.Browser.awesome_bookmarks_links}
        _details["history"]   = {"tab":DOM.Browser.awesome_history_tab  , "links":DOM.Browser.awesome_history_links  }

        #
        # Make sure the input is correct.
        #        
        _tab = p_tabName.lower().replace(" ", "_")
        try:
            _blah = _details[_tab]
        except:
            self.UTILS.TEST(False, "(failing because an unknown tab name ('%s') was passed to \"getAwesomeList()\".)" % p_tabName)
            return False
        
        self.UTILS.logResult("info", "Examining the list of sites for the <b>%s</b> tab ..." % p_tabName)
        rc
        self.UTILS.switchToFrame(*DOM.Browser.frame_locator)
        x = self.UTILS.getElement(DOM.Browser.url_input, "Search input field")
        x.tap()
        
        x = self.UTILS.getElement(_details[_tab]["tab"], "<b>%s</b> tab" % p_tabName)
        x.tap()
        self.UTILS.TEST(x.get_attribute("class") == "selected", "<b>%s</b> tab is selected" % p_tabName)
        
        try:
            self.wait_for_element_displayed(*_details[_tab]["links"], timeout=2)
            x = self.UTILS.getElements(_details[_tab]["links"], "%s links" % p_tabName)
        except:
            self.UTILS.logResult("info", "<i>(No list items found for <b>%s</b> tab.)</i>" % p_tabName)
            x = ""
            
        return x

