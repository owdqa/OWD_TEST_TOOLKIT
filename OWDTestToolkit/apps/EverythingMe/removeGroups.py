from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):
         
    def removeGroups(self, p_groupArray=False):
        #
        # Removes groups from the EME group page.<br>
        # <b>p_groupArray</p> is an array of group names (default = all groups).<br>
        # <br>
        # For example: <i> removeGroups(["Games","Local"])
        #
        boolOK  = False
        iconPos = -1
        counter = -1
         
        #
        # Put the groups into edit mode.
        #
        x = self.UTILS.getElements(DOM.EME.groups, "Groups")
        self.actions.press(x[0]).wait(2).release().perform()
 
        #
        # Remove all groups in the array.
        #
        _removed = 0
        _index   = 0
        for i in range(0,len(x)):
            _index = i - _removed
            _groupList = self.marionette.find_elements(*DOM.EME.groups)
            _group     = _groupList[_index]
            
            if p_groupArray:
                if _removed >= len(p_groupArray):
                    break
            
                #
                # Caller wants to remove specific groups.
                #
                for _groupSpecified in p_groupArray:
                    if _group.get_attribute("data-query"):
                        if _group.get_attribute("data-query").lower() == _groupSpecified.lower():
                            #
                            # Remove it.
                            #
                            try:
                                x = _group.find_element(*DOM.EME.remove_group_icon)
                                x.tap()
                                _removed = _removed + 1
                            except:
                                pass
                            
                            self.UTILS.logResult("info", "Removed group '%s' ..." % _group.get_attribute("data-query"))
                            break
            else:
                #
                # Caller wants to remove all groups.
                #
                try:
                    x = _group.find_element(*DOM.EME.remove_group_icon)
                    x.tap()
                    _removed = _removed + 1
                except:
                    pass
                self.UTILS.logResult("info", "Removed group '%s' ..." % _group.get_attribute("data-query"))

 
        #
        # Verify that the group has been removed.
        #
        x = self.UTILS.getElements(DOM.EME.groups, "Groups")
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