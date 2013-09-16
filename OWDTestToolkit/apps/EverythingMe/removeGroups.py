from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):
         
    def removeGroups(self, p_groupArray=False, p_validate=True):
        #
        # Removes groups from the EME group page.<br>
        # <b>p_groupArray</p> is an array of group names (default = all groups).<br>
        # <b>p_validate</p> check that the groups were removed (default = True).<br>
        # <br>
        # For example: <i> removeGroups(["Games","Local"])
        #
        boolOK  = False
        iconPos = -1
        counter = -1
         
        #
        # Put the groups into edit mode.
        # Sometimes this takes a while to happen, so increase the length
        # of time you press the icon until it works!
        #
        _boolOK = False
        for i in range(0,5):
            self.wait_for_element_present(*DOM.EME.groups, timeout=2)
            x = self.marionette.find_elements(*DOM.EME.groups)
            self.actions.press(x[0]).wait(3 + i).release().perform()
            
            try:
	            if x[0].find_element(*DOM.EME.remove_group_icon).is_displayed():
	                _boolOK = True
	                break
            except:
            	pass
               
            time.sleep(2)
               
 
        self.UTILS.TEST(_boolOK, "Enabled EDIT mode.")
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot of app in EDIT mode:", x)
 
        #
        # Remove all groups in the array.
        #
        x          = self.marionette.find_elements(*DOM.EME.groups)
        _removed   = 0
        _groupCNT  = len(x)
        
        if not p_groupArray:
            self.UTILS.logResult("info", "Removing all %s groups ..." % _groupCNT)
        else:
            self.UTILS.logResult("info", "Removing groups: %s" % str(p_groupArray))
            
        for i in range(0,_groupCNT):
            _groupList = self.marionette.find_elements(*DOM.EME.groups)
            _group     = _groupList[i - _removed]
            _groupName = _group.get_attribute("data-query")
            
            if p_groupArray:
                if _removed >= len(p_groupArray):
                    break
            
                #
                # Caller wants to remove specific groups.
                #
                for _groupSpecified in p_groupArray:
                    if _groupName:
                        if _groupName.lower() == _groupSpecified.lower():
                            #
                            # Remove it.
                            #
                            try:
                                x = _group.find_element(*DOM.EME.remove_group_icon)
                                x.tap()
                                _removed = _removed + 1
                                self.UTILS.logResult("info", "Removed group '%s' ..." % _groupName)
                            except:
                                pass
                            
                            break
            else:
                #
                # Caller wants to remove all groups.
                #
                try:
                    x = _group.find_element(*DOM.EME.remove_group_icon)
                    self.UTILS.logResult("debug", "x2")
                    x.tap()
                    self.UTILS.logResult("debug", "x3")
                    _removed = _removed + 1
                    self.UTILS.logResult("info", "Removed group '%s' ..." % _groupName)
                except:
                    pass


        #
        # Turn off edit mode.
        #
        self.UTILS.logResult("info", "Disabling edit mode ...")
        x = self.marionette.find_element(*DOM.EME.search_field)
        x.tap()
 
        #
        # Verify that the groups have been removed.
        #
        if p_validate:
            x = self.UTILS.getElements(DOM.EME.groups, "Groups (after editing)")
            if not p_groupArray:
                self.UTILS.TEST(len(x) == 1, "All groups were removed.")
            else:
                for groupName in p_groupArray:
                    _boolOK = True
                    for i in x:
                        if i.get_attribute("data-query"):
                            if i.get_attribute("data-query").lower() == groupName.lower():
                                _boolOK = False
                                break
                    
                    self.UTILS.TEST(_boolOK, "'%s' removed from groups." % groupName)