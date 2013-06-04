import time
from gaiatest   import GaiaTestCase
from marionette import Marionette
from OWDTestToolkit import *

class AppContacts(GaiaTestCase):
    
    #
    # When you create your instance of this class, include the
    # "self" object so we can access the calling class' objects.
    #
    def __init__(self, p_parent):
        self.apps       = p_parent.apps
        self.data_layer = p_parent.data_layer
        self.parent     = p_parent
        self.marionette = p_parent.marionette
        self.UTILS      = p_parent.UTILS

    def launch(self):
        #
        # Launch the app.
        #
        self.apps.kill_all()
        self.app = self.apps.launch('Contacts')
        self.UTILS.waitForNotElements(DOM.GLOBAL.loading_overlay, "Contacts app - loading overlay")
        
    def countEmailAddressesWhileEditing(self):
        #
        # Count the emails and return the number - assumes you 
        # are currently EDITING the contact (not viewing).
        #
        
        #
        # (for some reason these are flagged as not displayed, so
        # you have to get them as 'present').
        #
        x = self.UTILS.getElements(DOM.Contacts.email_fields, "Email fields", False, 2)
        self.UTILS.logResult("info", 
                             "NOTE: Contact's email addresses:")
        counter = 0
        for i in x:
            if i.get_attribute("value") != "#value#":
                counter = counter + 1
                self.UTILS.logResult("info", "    - " + str(counter) + ": " + i.get_attribute("value"))
            
        return counter

    def getContactFields(self):
        #
        # Return 3-d array of contact details (from view or edit contacts screen
        # - the identifiers should be the same ... *should* ...)
        #
        
        return {
        'givenName' : self.UTILS.getElement(DOM.Contacts.given_name_field, "Given name field", True, 5, False),
        'familyName': self.UTILS.getElement(DOM.Contacts.family_name_field, "Family name field", True, 5, False),
        'tel'       : self.UTILS.getElement(DOM.Contacts.phone_field, "Phone number field", True, 5, False),
        'email'     : self.UTILS.getElement(DOM.Contacts.email_field, "Email field", True, 5, False),
        'street'    : self.UTILS.getElement(DOM.Contacts.street_field, "Street field", True, 5, False),
        'zip'       : self.UTILS.getElement(DOM.Contacts.zip_code_field, "Zip code field", True, 5, False),
        'city'      : self.UTILS.getElement(DOM.Contacts.city_field, "City field", True, 5, False),
        'country'   : self.UTILS.getElement(DOM.Contacts.country_field, "Country field", True, 5, False),
        'comment'   : self.UTILS.getElement(DOM.Contacts.comment_field, "Comment field", True, 5, False)
        }
        
    def replaceStr(self, p_field, p_str):
        #
        # Replace text in a field (as opposed to just appending to it).
        #
        p_field.clear()
        p_field.send_keys(p_str)

    def populateFields(self, p_contact_json_obj):
        #
        # Put the contact details into the fields (assumes you are in the correct
        # screen already since this could be create or edit).
        # <br><br>
        # <b>p_contact_json_obj</b> must be an object in the same format as the
        # one in ./example/tests/mock_data/contacts.py.
        #
        contFields = self.getContactFields()
        
        #
        # Put the contact details into each of the fields (this method
        # clears each field first).
        #
        self.replaceStr(contFields['givenName'  ] , p_contact_json_obj["givenName"])
        self.replaceStr(contFields['familyName' ] , p_contact_json_obj["familyName"])
        self.replaceStr(contFields['tel'        ] , p_contact_json_obj["tel"]["value"])
        self.replaceStr(contFields['email'      ] , p_contact_json_obj["email"]["value"])
        self.replaceStr(contFields['street'     ] , p_contact_json_obj["adr"]["streetAddress"])
        self.replaceStr(contFields['zip'        ] , p_contact_json_obj["adr"]["postalCode"])
        self.replaceStr(contFields['city'       ] , p_contact_json_obj["adr"]["locality"])
        self.replaceStr(contFields['country'    ] , p_contact_json_obj["adr"]["countryName"])
        self.replaceStr(contFields['comment'    ] , p_contact_json_obj["comment"])

    def checkMatch(self, p_el, p_val, p_name):
        #
        # Test for a match between an element and a string
        # (found I was doing this rather a lot so it's better in a function).
        #
        test_str = str(p_el.get_attribute("value"))

        self.UTILS.TEST(
            (test_str == p_val),
            p_name + " = \"" + p_val + "\" (it was \"" + test_str + "\")."
            )

    def verifyFieldContents(self, p_contact_json_obj):
        #
        # Verify the contents of the contact fields in this screen (assumes
        # you are in the correct screen since this could be view or edit).
        # <br><br>
        # <b>p_contact_json_obj</b> must be an object in the same format as the
        # one in ./example/tests/mock_data/contacts.py.
        #
        contFields = self.getContactFields()      # Get the contact's fields again.
        
        self.checkMatch(contFields['givenName' ] , p_contact_json_obj['givenName']            , "Given name")
        self.checkMatch(contFields['familyName'] , p_contact_json_obj['familyName']           , "Family name")
        self.checkMatch(contFields['tel'       ] , p_contact_json_obj['tel']['value']         , "Telephone")
        self.checkMatch(contFields['email'     ] , p_contact_json_obj['email']['value']       , "Email")
        self.checkMatch(contFields['street'    ] , p_contact_json_obj['adr']['streetAddress'] , "Street")
        self.checkMatch(contFields['zip'       ] , p_contact_json_obj['adr']['postalCode']    , "Zip")
        self.checkMatch(contFields['city'      ] , p_contact_json_obj['adr']['locality']      , "City")
        self.checkMatch(contFields['country'   ] , p_contact_json_obj['adr']['countryName']   , "Country")
        self.checkMatch(contFields['comment'   ] , p_contact_json_obj['comment']              , "COMMENTS")


    def addGalleryImageToContact(self, p_num):
        #
        # Adds an image for this contact from the gallery
        # (assumes we're already in the 'new contact' or
        # 'edit conact' screen, and also that we have already
        # added an image to the gallery).
        #
#         self.UTILS.addFileToDevice(p_file, destination='DCIM/100MZLLA')
#         AppGallery(self).launch()

        #
        # Click the 'add picture' link.
        #
        x = self.UTILS.getElement(DOM.Contacts.add_photo, "'Add picture' link")
        x.tap()
        time.sleep(2)
        
        # Switch to the 'make a choice' iframe.
        self.marionette.switch_to_frame()
        
        # Choose to get a picture from the Gallery.
        x = self.UTILS.getElement(DOM.Contacts.photo_from_gallery, "Gallery link")
        x.tap()
        
        # Switch to Gallery iframe.
        time.sleep(2)
        self.UTILS.switchToFrame(*DOM.Gallery.frame_locator)
        
        # Select the thumbnail (assume it's the only one).
        x = self.UTILS.getElements(DOM.Contacts.picture_thumbnails, "Thumbnails for pictures")
        if x:
            x[p_num].tap()
            
            time.sleep(1)
            
            # Tap 'crop done' button.
            boolOK = True
            try:
                x = self.UTILS.getElement(DOM.Contacts.picture_crop_done_btn, "Crop 'done' button")
                x.tap()
            except:
                boolOK = False
    
            self.UTILS.TEST(boolOK, "Can finish cropping the picture and return to Contacts app.")
                
            time.sleep(1)
        
        # Back to contacts app iframe.
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
         
    def createNewContact(self, p_contact_json_obj, p_imgSource=False):
        #
        # Create a new contact with a image (if specified).
        # p_imgSource is either "gallery" or "camera" (or left undefined).
        # <br><br>
        # <b>p_contact_json_obj</b> must be an object in the same format as the
        # one in ./example/tests/mock_data/contacts.py.
        #
        self.startCreateNewContact()
        
        if p_imgSource == "gallery":
            self.addGalleryImageToContact(0)
            
        self.populateContactFields(p_contact_json_obj)

    def startCreateNewContact(self):
        #
        # Open the screen to add a contact.
        #
        
        #
        # First make sure we're in the right place.
        #
        viewAllHeader = self.UTILS.getElement(DOM.Contacts.view_all_header, "'View all contacts' header", False)
        if not viewAllHeader.is_displayed():
            #
            # Header isn't present, so we're not running yet.
            #
            self.launch()
            
        #
        # Click Create new contact from the view all screen.
        #
        self.UTILS.waitForElements(DOM.Contacts.view_all_header, "View all contacts header")
        add_new_contact = self.UTILS.getElement(DOM.Contacts.add_contact_button, "'Add new contact' button")
        
        add_new_contact.tap()
        
        #
        # Enter details for new contact.
        #
        self.UTILS.waitForElements(DOM.Contacts.add_contact_header, "Add contact header")
        
    def populateContactFields(self,p_contact_json_obj):
        #
        # Put the contact details into each of the fields.
        # <br><br>
        # <b>p_contact_json_obj</b> must be an object in the same format as the
        # one in ./example/tests/mock_data/contacts.py.
        #
        self.populateFields(p_contact_json_obj)
        
        # Press the 'done' button and wait for the 'all contacts' page to load.
        done_button = self.UTILS.getElement(DOM.Contacts.done_button, "'Done' button")
        done_button.tap()
        
        # Wait for the 'view all contacts' header to be displayed.
        self.UTILS.waitForElements(DOM.Contacts.view_all_header, "View all contacts header")
        
        # Now check the contact's name is displayed here too.
        x = ("xpath", DOM.Contacts.view_all_contact_xpath % p_contact_json_obj['name'].replace(" ",""))
        self.UTILS.waitForElements(x, "Contact '" + p_contact_json_obj['name'] + "'")

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
                


    def viewContact(self, p_contact_name):
        #
        # Navigate to the 'view details' screen for a contact (assumes we are in the
        # 'view all contacts' screen).
        #
        
        #
        # Find the name of our contact in the contacts list.
        #
#        try:
#            contact_found = self.marionette.find_element("xpath", DOM.Contacts.view_all_contact_xpath % p_contact['name'].replace(" ",""))
#        except:
#            self.UTILS.logResult(False, "'" + p_contact['name'] + "' is found in the contacts list!")
#            return 0 # (leave the function)

        #
        # TEST: try to click the contact name in the contacts list.
        #
        x = ("xpath", DOM.Contacts.view_all_contact_xpath % p_contact_name.replace(" ",""))
        contact_found = self.UTILS.getElement(x, "Contact '" + p_contact_name + "'")
        contact_found.tap()
        
        self.UTILS.waitForElements(DOM.Contacts.view_details_title, "'View contact details' title")

        # 
        # TEST: Correct contact name is in the page header.
        #
        self.UTILS.headerCheck(p_contact_name)
            
        time.sleep(2)
    
    def tapSettingsButton(self):
        #
        # Tap the settings button.
        #
        x = self.UTILS.getElement(DOM.Contacts.settings_button, "Settings button")
        x.tap()
        
        self.UTILS.waitForElements(DOM.Contacts.settings_header, "Settings header")
        
    def checkViewContactDetails(self, p_contact_json_obj, p_imageCheck = False):
        #
        # Validate the details of a contact in the 'view contact' screen.
        # <br><br>
        # <b>p_contact_json_obj</b> must be an object in the same format as the
        # one in ./example/tests/mock_data/contacts.py.
        #
        
        #
        # Go to the view details screen for this contact.
        #
        self.viewContact(p_contact_json_obj['name'])
        
        if p_imageCheck:
            #
            # Verify that an image is displayed.
            #
            x = self.marionette.find_element("id", "cover-img")
            x_style = x.get_attribute("style")
            self.UTILS.TEST("blob" in x_style, "Contact's image contains 'something' in contact details screen.")

        #
        # Correct details are in the contact fields.
        #
        self.verifyFieldContents(p_contact_json_obj)
        
    def pressEditContactButton(self):
        #
        # Presses the Edit contact button when vieweing a contact.
        #
        editBTN = self.UTILS.getElement(DOM.Contacts.edit_details_button, "Edit details button")
        editBTN.tap()
        self.UTILS.waitForElements(DOM.Contacts.edit_contact_header, "'Edit contact' screen header")

    def pressCancelEditButton(self):
        #
        # Presses the Edit contact button when vieweing a contact.
        #
        editCnclBTN = self.UTILS.getElement(DOM.Contacts.edit_cancel_button, "Cancel edit button")
        editCnclBTN.tap()
        self.UTILS.waitForElements(DOM.Contacts.view_details_title, "'View contact details' title")

    def checkEditContactDetails(self, p_contact_json_obj):
        #
        # Validate the details of a contact in the 'view contact' screen.
        #
        # p_contact_json_obj must be an object in the same format as the
        # one in ./example/tests/mock_data/contacts.py.
        #
        self.pressEditContactButton()

        #
        # Correct details are in the contact fields.
        #
        self.verifyFieldContents(p_contact_json_obj)

    def editContact(self, p_contact_curr_json_obj, p_contact_new_json_obj):
        #
        # Replace the details of one contact with another via the edit screen.
        # <br><br>
        # <b>p_contact_curr_json_obj</b> and <b>p_contact_new_json_obj</b> must 
        # be objects in the same format as the one in 
        # ./example/tests/mock_data/contacts.py (however, only needs the 
        # 'name' component is used from the p_contact_curr_json_obj).
        #
        
        #
        # Go to the view details screen for this contact.
        #
        self.viewContact(p_contact_curr_json_obj['name'])
                
        #
        # Tap the Edit button to go to the edit details page.
        #
        editBTN = self.UTILS.getElement(DOM.Contacts.edit_details_button, "Edit details button")
        editBTN.tap()
        self.UTILS.waitForElements(DOM.Contacts.edit_contact_header, "'Edit contacts' screen header")

        #
        # Enter the new contact details.
        #
        self.populateFields(p_contact_new_json_obj)
        
        #
        # Save the changes
        #
        updateBTN = self.UTILS.getElement(DOM.Contacts.edit_update_button, "Edit 'update' button")
        updateBTN.tap()

        #
        # Return to the contact list screen.
        #
        backBTN = self.UTILS.getElement(DOM.Contacts.details_back_button, "Details 'back' button")
        backBTN.tap()
        
        self.UTILS.waitForElements(DOM.Contacts.view_all_header, "'View all contacts' screen header")

    def switchToFacebook(self):
        #
        # <i>Private</i> function to handle the iframe hop-scotch involved in 
        # finding the facebook app launched via contacts app.
        #
        time.sleep(2)
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)        
        self.UTILS.switchToFrame(*DOM.Contacts.settings_fb_frame)        

        #
        # Wait for the fb page to start.
        #
        self.UTILS.waitForElements(DOM.Facebook.friends_header, "Facebook friends header")
        time.sleep(2)

    def tapLinkContact(self):
        #
        # Press the 'Link contact' button in the view contact details screen.
        #
        
        #
        # NOTE: there is more than one button with this ID, so make sure we use the right one!
        # (One of them isn't visible, so we need to check for visibility this way or the
        # 'invisible' one will cause 'getElements()' to fail the test).
        #
        time.sleep(2)
        x = self.UTILS.getElements(DOM.Contacts.link_button, "Link contact button", False)
        for i in x:
            if i.is_displayed():
                i.tap()
                break
            
        self.switchToFacebook()
        
    def enableFBImport(self):
        #
        # Enable fb import.
        #
        x = self.UTILS.getElement(DOM.Contacts.settings_fb_enable, "Enable facebook button")
        x.tap()
        time.sleep(1)

        #
        # Were we already connected to facebook?
        #
        try:
            self.parent.wait_for_element_displayed('xpath', "//button[text()='Remove']", timeout=5)
            x = self.marionette.find_element('xpath', "//button[text()='Remove']")
            x.tap()
            self.UTILS.waitForElements(DOM.Contacts.settings_fb_logout_wait, "FB logout message", True, 5)
            self.UTILS.waitForNotElements(DOM.Contacts.settings_fb_logout_wait, "FB logout message", True, 60)
            
            self.marionette.switch_to_frame()
            self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)

            x = self.UTILS.getElement(DOM.Contacts.settings_done_button, "Settings Done button")
            x.tap()
            time.sleep(1)

            #
            # Now click the 'enable facebook' button again.
            #
            # For some reason I need to relaunch the Contacts app first.
            # If I don't then after I log in again the 'Please hold on ...'
            # message stays forever.
            # (This is only a problem when automating - if you do this
            # manually it works fine.)
            #
            self.launch()
            self.tapSettingsButton()

            self.marionette.switch_to_frame()
            self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)

            x = self.UTILS.getElement(DOM.Contacts.settings_fb_enable, "Enable facebook button")
            x.tap()

        except:
            #
            # We weren't logged into facebook, so continue.
            #
            pass

        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)

        time.sleep(2) # Just to be sure!

    def verifyLinked(self, p_contact_name, p_fb_email):
        #
        # Verifies that this contact is linked
        # (assumes we're in the 'all contacts' screen).
        #
        
        #
        # Check that our contact is now listed as a facebook contact (icon by the name in 'all contacts' screen).
        #
        x = self.UTILS.getElements(DOM.Contacts.social_network_contacts, "Social network contacts")
        self.UTILS.TEST(len(x) > 0, "Contact is listed as a facebook contact after linking.")

        #
        # View the details for this contact.
        #
        self.viewContact(p_contact_name)
        
        #
        # Check the expected elements are now visible. 
        #
        # I'm having serious problems finding buttons based on 'text' directly, so here's
        # the 'brute-force' method ...
        boolViewFbProfile   = False
        boolWallPost        = False
        boolLinkedEmail     = False
        boolUnLink          = False
        x = self.UTILS.getElements(("tag name", "button"), "All buttons on this page")
        for i in x:
            if i.text == "View Facebook profile": boolViewFbProfile = True
            if i.text == "Wall post"            : boolWallPost      = True
            if i.text == p_fb_email             : boolLinkedEmail   = True
            if i.text == "Unlink contact"       : boolUnLink        = True
            
        self.UTILS.TEST(boolViewFbProfile   , "'View Facebook profile' button is displayed after contact linked to fb contact.")
        self.UTILS.TEST(boolWallPost        , "'Wall post' button is displayed after contact linked to fb contact.")
        self.UTILS.TEST(boolUnLink          , "'Unlink contact' button is displayed after contact linked to fb contact.")
        self.UTILS.TEST(boolLinkedEmail     , "Linked facebook email address is displayed after contact linked to fb contact.")
        

    def changeVal(self, p_contact_name, p_field, p_newVal):
        #
        # Change a value for a contact (assumes we're looking at the 'all contacts' screen
        # currently).
        #
        
        #
        # View our contact.
        #
        self.viewContact(p_contact_name)
         
        #
        # Press the edit button.
        #
        self.pressEditContactButton()
         
        #
        # Change the name to "aaaaabbbbbccccaaaa"
        #
        contFields = self.getContactFields()
        self.replaceStr(contFields[p_field] , p_newVal)
 
        #
        # Save the changes
        #
        updateBTN = self.UTILS.getElement(DOM.Contacts.edit_update_button, "Edit 'update' button")
        updateBTN.tap()
 
        #
        # Return to the contact list screen.
        #
        backBTN = self.UTILS.getElement(DOM.Contacts.details_back_button, "Details 'back' button")
        backBTN.tap()
         
        self.UTILS.waitForElements(DOM.Contacts.view_all_header, "'View all contacts' screen header")
        
    def search(self, p_val):
        #
        # Searches the 'all contacts' screen for p_val
        # (assumes we're currently in the 'all contacts' screen).
        #
        
        #
        # Tap the search area.
        #
        x = self.UTILS.getElement(DOM.Contacts.search_field, "Search field")
        x.tap()
         
        # problems with this just now - seems to mess up marionette somehow ...
#         self.parent.keyboard.send(p_val)
#         self.marionette.switch_to_frame()
#         self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)

#         # ... so using this instead:
#         self.marionette.switch_to_frame()
#         self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
#         x = self.UTILS.getElement(DOM.Contacts.search_contact_input, "Search input")
#         x.send_keys(p_val)

        self.UTILS.typeThis(DOM.Contacts.search_contact_input, "Search input", p_val, 
                            p_no_keyboard=True,
                            p_validate=False,
                            p_clear=False,
                            p_enter=False)

         
    def checkSearchResults(self, p_contactName, p_present=True):
        #
        # Checks the results of a search() to see
        # if the contact is present or not (depending
        # on the 'p_present' setting).
        #
        
        #
        # Verify our contact is all that's displayed in the result list.
        #
        y = self.marionette.find_elements(*DOM.Contacts.search_results_list)
        boolContact=False
        for i in y:
            if p_contactName in i.text:
                boolContact = True
                
        if p_present:
            comment = " is "
        else:
            comment = " is not "
        
        comment2 = comment + "displayed in the result list."
                 
        self.UTILS.TEST(p_present == boolContact, 
                        "Contact '" + p_contactName + "'" + comment2)


    def pressDeleteContactButton(self):
        #
        # In it's own function just to save time figuring out
        # that you have to get the button into view before you
        # can press it, then re-align the screen again.
        #
        self.marionette.execute_script("document.getElementById('" + \
                                       DOM.Contacts.delete_contact_btn[1] + \
                                       "').scrollIntoView();")
        self.marionette.execute_script("document.getElementById('settings-button').scrollIntoView();")
        x = self.UTILS.getElement(DOM.Contacts.delete_contact_btn, "Delete contacts button", False) 
        x.tap()

    def deleteContact(self, p_fullName):
        #
        # Deletes a contact.<br>
        # p_fullName must match the name displayed
        # in the 'view all contacts' screen (including spaces).
        #
        
        #
        # Make sure we are in the contacts app.
        #
        try:
            x = self.marionette.find_element("xpath", "//h1[text() = 'Contacts']")
            if not x.is_displayed():
                self.launch()
        except:
            self.launch()
        
        #
        # View our contact.
        #
        self.viewContact(p_fullName)
           
        #
        # Edit our contact.
        #
        self.pressEditContactButton()
         
        #
        # Delete our contact.
        #
        self.pressDeleteContactButton()
         
        #
        # Confirm deletion.
        #
        x = self.UTILS.getElement(DOM.Contacts.confirm_delete_btn, "Confirm deletion button")
        x.tap()
         
        #
        # Now verify that this contact is no longer present (or no search field if
        # this was the only contact).
        #
        contact_el = x = ("xpath", DOM.Contacts.view_all_contact_xpath % p_fullName.replace(" ",""))
        self.UTILS.waitForNotElements(contact_el, "Contact name in 'all contacts' screen")
 
    def addAnotherEmailAddress(self, p_email_address):
        #
        # Add a new email address to the contact currnetly being viewed in Edit mode.
        #
        x = self.UTILS.getElement(DOM.Contacts.add_email_button, "Add email button")
        x.tap()
        
        # (Marionette currently messes up the screen, so correct this.)
        self.marionette.execute_script("document.getElementsByTagName('h1')[0].scrollIntoView();")
        
        #
        # Add the email.
        #
        x = self.UTILS.getElements(DOM.Contacts.email_fields, "Email fields", False, 2)
        for i in x:
            if i.get_attribute("value") == "":
                i.send_keys(p_email_address)
                
                # (if there's a "_" in the email address, the screen will lock.)
                if "_" in p_email_address:
                    orig_frame = self.UTILS.currentIframe()
                    self.lockscreen.unlock()
                    self.marionette.switch_to_frame()
                    self.UTILS.switchToFrame("src", orig_frame)

                break
            