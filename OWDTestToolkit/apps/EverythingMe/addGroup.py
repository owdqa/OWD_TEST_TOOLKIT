from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

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

