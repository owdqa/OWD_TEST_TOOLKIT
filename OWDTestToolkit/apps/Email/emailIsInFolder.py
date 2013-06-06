from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def emailIsInFolder(self, p_subject):
        #
        # Verify an email is in this folder with the expected subject.
        #

        #
        # Because this can take a while, try to "wait_for_element..." several times (5 mins).
        #
        loops = 60
        while loops > 0:
            try:
                #
                # Look through any entries found in the folder ...
                #
                self.wait_for_element_displayed(*DOM.Email.folder_subject_list)
                z = self.marionette.find_elements(*DOM.Email.folder_subject_list)
                pos=0
                for i in z:
                    #
                    # Do any of the folder items match our subject?
                    #
                    if i.text == p_subject:
                        # Yes! But it might be off the screen, so scroll it into view.
                        # This is a bit of a hack since marionette.tap() doesn't do it
                        # (and I haven't figured out how to get the action chain to do it yet).
                        self.marionette.execute_script("document.getElementsByClassName('" + \
                                                       DOM.Email.folder_headers_list[1] + \
                                                       "')[" + str(pos) + "].scrollIntoView();")
                        self.marionette.execute_script("document.getElementsByTagName('h1')[0].scrollIntoView();")
                        time.sleep(1)
                             
                        return i
                    
                    pos = pos + 1
                    
            except:
                #
                # Nothing is in the folder yet, just ignore and loop again.
                #
                pass
            
            #
            # Either the folder is still empty, or none of the items in it match our
            # subject yet.
            # Wait a couple for seconds and try again.
            # 
            # (don't validate because this could go on for a while...)
            self.UTILS.logResult("info", 
                                 "'" + p_subject + "' not found yet - refreshing the folder and looking again ...")
            x = self.marionette.find_element(*DOM.Email.folder_refresh_button)
            x.tap()
            
            time.sleep(5)
            
            loops = loops - 1
        
        return False

