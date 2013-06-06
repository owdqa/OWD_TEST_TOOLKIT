from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def verifyImageInAllContacts(self, p_contact_name):        
        #
        # Verify that the contact's image is displayed.
        #
        x = self.UTILS.getElements(DOM.Contacts.view_all_contact_list, "Contact list", False)
        for i in x:
            try:
                i.find_element("xpath", "//p[@data-order='%s']" % p_contact_name.replace(" ",""))
            except:
                pass
            else:
                #
                # This is our contact - try and get the image.
                #
                boolOK = True
                try:
                    x = i.find_element("xpath", "//img")
                    self.UTILS.TEST("blob" in x.get_attribute("src"), "Contact image present in 'all contacts' screen.")
                except:
                    boolOK = False
                
                self.UTILS.TEST(boolOK, "An image is present for this contact in all contacts screen.")
                
