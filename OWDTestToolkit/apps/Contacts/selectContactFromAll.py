from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def selectContactFromAll(self, p_contactName):
        #
        # Select the result of a search 
        #
        y = self.UTILS.getElements(DOM.Contacts.view_all_contact_list, "All contacts list", False)
        time.sleep(1)
        i_count=-1
        for i in y:
            i_count = i_count + 1
            self.UTILS.logResult("info", "'%s'" % i.text)
            if p_contactName in i.text:
                self.UTILS.logResult("info", "Contact '%s' found in all contacts." % p_contactName)
                self.marionette.execute_script("document.getElementsByClassName('contact-item')[%s].click()" %\
                                               i_count)
#                 i.tap()
                return
                
        self.UTILS.logResult("info", "Contact '%s' was <b>not</b> found in the contacts list." % p_contactName)



        self.UTILS.waitForElements(DOM.Contacts.view_details_title, "'View contact details' title")
