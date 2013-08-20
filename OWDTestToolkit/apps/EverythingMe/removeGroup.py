from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

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
        if not boolOK:
			self.UTILS.logResult("info", 
								 "(Group '" + p_group + "' not found in Everything.Me, so no need to remove it.)")
		
			return

        self.UTILS.logResult("info", "(Removing group '" + p_group + "'.)")
        x = self.UTILS.getElements(DOM.EME.groups, "Groups")[iconPos]
        y = x.find_element(*DOM.EME.remove_group_icon)
        y.tap()
        
        #
        # Deactivate edit mode  (just tap the search field).
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
        
