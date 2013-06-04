import time
from gaiatest   import GaiaTestCase
from marionette import Marionette
from marionette import Actions
from OWDTestToolkit import *

class AppEverythingMe(GaiaTestCase):
    
    #
    # When you create your instance of this class, include the
    # "self" object so we can access the calling class' objects.
    #
    def __init__(self, p_parent):
        self.apps       = p_parent.apps
        self.data_layer = p_parent.data_layer
        self.marionette = p_parent.marionette
        self.UTILS      = p_parent.UTILS
        self.actions    = Actions(self.marionette)
                


    def launch(self):
        #
        # Go to the homescreen.
        #
        self.UTILS.goHome()
        
        #
        # Scroll to the left to expose the 'everything.me' screen.
        #
        self.UTILS.scrollHomescreenLeft()
        self.UTILS.waitForElements(DOM.EME.groups, "EME groups", True, 30)

    def searchForApp(self, p_name):
        #
        # Uses the search field to find the app (waits for the
        # result to appear etc...).<br>
        # Returns the element for the icon (or False if it's not found).
        #
        self.UTILS.typeThis(DOM.EME.search_field, "Search field", p_name, p_no_keyboard=True)
        
        boolOK = True
        
        try:
            self.wait_for_element_displayed("xpath", 
                                            DOM.EME.search_result_icon_xpath % p_name,
                                            timeout=60)
        except:
            boolOK = False
            
        return boolOK

    def pickGroup(self, p_name):
        #
        # Pick a group from the main icons.
        #
        x = self.UTILS.getElements(DOM.EME.groups, "EME group list")
        boolOK = False
        for groupLink in x:
            if groupLink.get_attribute("data-query") == p_name:
                groupLink.tap()
                time.sleep(10)
                boolOK = True
                break
        
        #
        # At this point the geolocation sometimes wants to know
        # if it can remember our location.
        #
        self.UTILS.clearGeolocPermission()
        
        return boolOK
    
    def removeGroup(self, p_group):
        #
        # Removes a group from the EME group page.
        #
        x = self.UTILS.getElements(DOM.EME.groups, "Groups")
        boolOK  = False
        iconPos = -1
        counter = -1
        for i in x:
            counter = counter + 1
            if i.get_attribute("data-query") == p_group:
                boolOK = True
                
                #
                # Long press to activate edit mode.
                #
                self.actions.press(i).wait(2).release()
                self.actions.perform()
                
                iconPos = counter
                break
        
        #
        # If the group was present, remove it.
        #
        if boolOK:
            self.UTILS.logResult("info", "(Removing group '" + p_group + "'.)")
            x = self.UTILS.getElements(DOM.EME.groups, "Groups")[iconPos]
            y = x.find_element(*DOM.EME.remove_group_icon)
            y.tap()
            
            #
            # Disactivate edit mode  (just tap the search field).
            #
            x = self.marionette.find_element(*DOM.EME.search_field)
            x.tap()
            
            #
            # Verify that the group has been removed.
            #
            x = self.UTILS.getElements(DOM.EME.groups, "Groups")
            boolOK = True
            for i in x:
                if i.get_attribute("data-query") == p_group:
                    boolOK = False
                    break
                
            self.UTILS.TEST(boolOK, "Group is no longer present in Everything.Me.")
        else:
            self.UTILS.logResult("info", 
                                 "(Group '" + p_group + "' not found in Everything.Me, so no need to remove it.)")

        return
        
    def addGroup(self, p_group):
        #
        # Adds a group to EME (assumes you're already in the EME group screen).
        #
        self.UTILS.logResult("info", "(Adding group '" + p_group + "'.)")
        
        #
        # Click the 'More' icon.
        #
        x = self.UTILS.getElement(DOM.EME.add_group_button, "'More' icon")
        x.tap()
        
        #
        # Wait for the 'loading' spinner to go away (can take a while!).
        #
        self.UTILS.waitForNotElements(DOM.EME.loading_groups_message, "'Loading' message", True, 120)
        
        #
        # Chose an item from the groups list...
        #
        self.UTILS.selectFromSystemDialog(p_group)
        
        #
        # Verify the new group is in the groups list.
        #
        x = self.UTILS.getElements(DOM.EME.groups, "Groups")
        boolOK = False
        for i in x:
            if i.get_attribute("data-query") == p_group:
                boolOK = True
                break
            
        self.UTILS.TEST(boolOK, "New group '" + p_group + "' is now present in the EME groups.")
        
        return boolOK

    def addAppToHomescreen(self, p_name):
        #
        # Pick an app from the apps listed in this group.
        #
        x = self.UTILS.getElements(DOM.EME.apps, "Apps list", True, 30)
        for appLink in x:
            if appLink.get_attribute("data-name") == p_name:
                from marionette import Actions
                actions = Actions(self.marionette)
                actions.press(appLink).wait(2).release()
                actions.perform()
                
                self.marionette.switch_to_frame()
                x = self.UTILS.getElement(DOM.EME.add_app_to_homescreen, "Add app to homescreen button")
                x.tap()
                
                #
                # Might need to do this again for Geoloc. ...
                #
                try:
                    x = self.marionette.find_element(*DOM.EME.add_app_to_homescreen)
                    x.tap()
                except:
                    pass
                
                # This isn't obvious, but you need to scroll the screen right
                # to reset the position for finding the app later, so I'm
                # doing it here.
                time.sleep(2)
                self.UTILS.goHome()
                self.UTILS.scrollHomescreenRight()

                return True
        
        return False

