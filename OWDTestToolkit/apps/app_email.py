import time
from gaiatest   import GaiaTestCase
from marionette import Marionette
from OWDTestToolkit import *

class AppEmail(GaiaTestCase):
    
    #
    # When you create your instance of this class, include the
    # "self" object so we can access the calling class' objects.
    #
    def __init__(self, p_parent):
        self.apps       = p_parent.apps
        self.data_layer = p_parent.data_layer
        self.marionette = p_parent.marionette
        self.UTILS      = p_parent.UTILS
        self.parent     = p_parent
            
    def launch(self):
        #
        # Launch the app.
        #
        self.apps.kill_all()
        self.app = self.apps.launch('Email')
        self.UTILS.waitForNotElements(DOM.GLOBAL.loading_overlay, "Email app - loading overlay");
        
    def waitForDone(self):
        #
        # Wait until any progress icon goes away.
        #
        self.UTILS.waitForNotElements(('tag name', 'progress'), "Progress icon", True, 60);
        time.sleep(2) # (just to be sure!)

    def goto_folder_from_list(self, p_name):
        #
        # Goto a specific folder in the folder list screen.
        #
        x = self.UTILS.getElement(('xpath', DOM.Email.folderList_name_xpath % p_name), "Link to folder '" + p_name + "'")
        x.tap()
        
        self.UTILS.waitForElements(("xpath", DOM.GLOBAL.app_head_specific % p_name), "Header for '" + p_name + "' folder")
        
    
    def switchAccount(self, p_address):
        #
        # Add a new account.
        #
        x = self.UTILS.getElement(DOM.Email.settings_menu_btn, "Settings menu button")
        x.tap()
        
        #
        # Are we already in this account?
        #
        x = self.UTILS.getElement(DOM.GLOBAL.app_head, "Header")
        if x.text == p_address:
            # Already here - just go to the Inbox.
            self.goto_folder_from_list("Inbox")
            return True
        
        #
        # We're not in this account already, so let's look for it.
        #
        x = self.UTILS.getElement(DOM.Email.goto_accounts_btn, "Accounts button")
        x.tap()
        
        
        x = ('xpath', DOM.GLOBAL.app_head_specific % "Accounts")
        self.UTILS.waitForElements(x, "Accounts header", True, 20, False)
        
        #
        # Check if it's already set up (this may be empty, so don't test for this element).
        #
        x = self.marionette.find_elements(*DOM.Email.accounts_list_names)
        for i in x:
            if i.text != "":
                if i.text == p_address:
                    i.tap()
                    
                    self.goto_folder_from_list("Inbox")
                    return True
        
        #
        # It's not setup yet, so we couldn't switch.
        #
        return False


    def remove_accounts_and_restart(self):
        #
        # Remove current email accounts via the UI and restart the application.
        # <br><br>
        # <b>NOTE:</b> Currently broken due to https://bugzilla.mozilla.org/show_bug.cgi?id=849183
        # so it's been set to do nothing!
        #
        return

        
        try:
            #
            # Make sure we're starting from the beginning ...
            # (it might not be running, so ignore any errors here).
            #
            self.marionette.kill("Email")
        except:
            pass
        
        self.launch()

        try:
            x = self.UTILS.waitForElements(("xpath", "//h1[text()='Inbox']"), "Inbox header", 10)
        except:
            #
            # We have no accounts set up (or the app would default to
            # the inbox of one of them).
            #
            self.UTILS.logResult("info", "(No email accounts set up yet.)")
            return
                
        x = self.UTILS.getElement(DOM.Email.settings_menu_btn, "Settings button")
        x.tap()
        
        x = self.UTILS.getElement(DOM.Email.settings_set_btn, "Set settings button")
        x.tap()
        
        x=('xpath', DOM.GLOBAL.app_head_specific % "Mail Settings")
        self.UTILS.waitForElements(x, "Mail settings", True, 20, False)
        
        #
        # Remove each email address listed ...
        #
        x = self.UTILS.getElements(DOM.Email.email_accounts_list,
                                   "Email accounts list", False, 20, False)
        for i in x:
            if i.text != "":
                # This isn't a placeholder, so delete it.
                self.UTILS.logComment("i: " + i.text)
                i.tap()
                
                x = ('xpath', DOM.GLOBAL.app_head_specific % i.text)
                self.UTILS.waitForElements(x, i.text + " header", True, 20, False)
                
                # Delete.
                delacc = self.UTILS.getElement(DOM.Email.settings_del_acc_btn, "Delete account button")
                delacc.tap()
                time.sleep(2)
                
                # Confirm.  <<<< PROBLEM (on forums)!
                delconf = self.UTILS.getElement(DOM.Email.settings_del_conf_btn, "Confirm delete button")
                delconf.tap()
                
                # Wait for this dialog to go away, then sleep for 1s.
        
        #
        # Now relaunch the app.
        #
        self.launch()
    
    def setupAccount(self, p_user, p_email, p_pass):
        #
        # Set up a new email account in the email app and login.
        #

        #
        # If we've just started out, email will open directly to "New Account").
        #
        x = self.UTILS.getElement(DOM.GLOBAL.app_head, "Application header")
        if x.text.lower() != "new account":
            #
            # We have at least one emali account setup,
            # check to see if we can just switch to ours.
            #
            if self.switchAccount(p_email):
                return
        
            #
            # It's not setup already, so prepare to set it up!
            #
            x = self.UTILS.getElement(DOM.Email.settings_set_btn, "Settings set button")
            x.tap()
            
            x = self.UTILS.getElement(DOM.Email.settings_add_account_btn, "Add account button")
            x.tap()

        #
        # (At this point we are now in the 'New account' screen by one path or
        # another.)
        #
#         u = self.UTILS.getElement(DOM.Email.username, "Username field")
#         e = self.UTILS.getElement(DOM.Email.email_addr, "Email address field")
#         p = self.UTILS.getElement(DOM.Email.password, "Password field")
# 
#         if p_user != "":
#             u.send_keys(p_user)
#         if p_email != "":
#             e.send_keys(p_email)
#         if p_pass != "":
#             p.send_keys(p_pass)

        self.UTILS.typeThis(DOM.Email.username  , "Username field", p_user , True, True)
        self.UTILS.typeThis(DOM.Email.email_addr, "Address field" , p_email, True, True)
        self.UTILS.typeThis(DOM.Email.password  , "Password field", p_pass , True, True)
            
        self.parent.lockscreen.unlock()
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame(*DOM.Email.frame_locator)

        btn = self.UTILS.getElement(DOM.Email.login_next_btn, "Login - 'next' button")
        btn.tap()
        
#         time.sleep(5)
#         self.UTILS.switchToFrame(*DOM.Email.frame_locator)
        
        self.UTILS.waitForElements(DOM.Email.sup_header, "Email header", True, 20, False)
        
        #
        # Click the 'continue ...' button.
        #
        x = self.UTILS.getElement(DOM.Email.sup_next_btn, "'Next' button")
        x.tap()
        
#         self.waitForDone()
        time.sleep(5)
        
        #
        # Click the 'continue to mail' button.
        #
        time.sleep(1)
        x = self.UTILS.getElement(DOM.Email.login_cont_to_email_btn, "'Continue to mail' button", True, 60)
        x.tap()
        
        self.UTILS.waitForNotElements(DOM.Email.login_cont_to_email_btn, "'Continue to mail' button")
        
        self.UTILS.waitForElements(("xpath", "//h1[text()='Inbox']"), "Inbox")
        time.sleep(2)
        
    
    def send_new_email(self, p_target, p_subject, p_message):
        #
        # Compose and send a new email.
        #
        x = self.UTILS.getElement(DOM.Email.compose_msg_btn, "Compose message button")
        x.tap()

        #
        # Wait for 'compose message' header.
        #
        x = self.UTILS.getElement(('xpath', DOM.GLOBAL.app_head_specific % "Compose message"),
                                  "Compose message header")
        
        #
        # Put items in the corresponsing fields.
        #
#         msg_to      = self.UTILS.getElement(DOM.Email.compose_to, "'To' field")
#         msg_subject = self.UTILS.getElement(DOM.Email.compose_subject, "'Subject' field")
#         msg_msg     = self.UTILS.getElement(DOM.Email.compose_msg, "Message field")
#         msg_to.send_keys(p_target)
#         time.sleep(1)
#         msg_subject.send_keys(p_subject)
#         time.sleep(1)
#         msg_msg.send_keys(p_message)
#         time.sleep(1)
            
        self.UTILS.typeThis(DOM.Email.compose_to     , "'To' field"     , p_target , True, False)
        self.UTILS.typeThis(DOM.Email.compose_subject, "'Subject' field", p_subject, True, False)
        self.UTILS.typeThis(DOM.Email.compose_msg    , "Message field"  , p_message, True, False, False)

        self.sendTheMessage()

    def sendTheMessage(self):        
        #
        # Hits the 'Send' button to send the message (handles
        # waiting for the correct elements etc...).
        #
        x = self.UTILS.getElement(DOM.Email.compose_send_btn, "Send button")
        x.tap()
        time.sleep(2)
                
        #
        # Wait for inbox to re-appear (give it a BIG wait time because sometimes
        # it just needs it).
        #
        self.UTILS.waitForNotElements(DOM.Email.compose_sending_spinner, "Sending email spinner", True, 60, False)

        x = ('xpath', DOM.GLOBAL.app_head_specific % "Inbox")
        y = self.UTILS.waitForElements(x, "Inbox", True, 120)
        
        
    def openMailFolder(self, p_folderName):
        #
        # Open a specific mail folder (must be called from "Inbox").
        #
        x = self.UTILS.getElement(DOM.Email.settings_menu_btn, "Settings menu button")        
        x.tap()        
        
        #
        # When we're looking at the folders screen ...
        #
        self.UTILS.waitForElements(DOM.Email.folderList_header, "Folder list header", True, 20, False)
        
        #
        # ... click on the folder were after.
        #
        self.goto_folder_from_list(p_folderName)
        
        #
        # Wait a while for everything to finish populating.
        #
        self.UTILS.waitForNotElements(DOM.Email.folder_sync_spinner,
                                       "Loading messages spinner", True, 60, False)
        
    def openMsg(self, p_subject):
        #
        # Opens a specific email in the current folder
        # (assumes we're already in the folder we want).
        #

        myEmail = self.emailIsInFolder(p_subject)
        self.UTILS.TEST(myEmail != False, "Found email with subject '" + p_subject + "'.")
        if myEmail:
            #
            # We found it - open the email.
            #
            myEmail.tap()
            
            #
            # Check it opened.
            #
            boolOK = True
            try:
                self.wait_for_element_displayed(*DOM.Email.open_email_from)
                boolOK=True
            except:
                boolOK=False
                
            return boolOK
            
        else:
            return False

    
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

    def deleteEmail(self, p_subject):
        #
        # Deletes the first message in this folder with this subject line.
        #
        
        #
        # Open the message.
        #
        self.openMsg(p_subject)

        #
        # Press the delete button and confirm deletion.
        #
        x = self.UTILS.getElement(DOM.Email.delete_this_email_btn, "Delete button")
        x.tap()
        
        #
        # Horrific, but there's > 1 button with this id and > 1 button with this text.
        # For some reason, I can't wait_for_displayed() here either, so I have to wait for the buttons
        # to be 'present' (not 'displayed'), then look through them until I find the one I want.
        #
        x = self.UTILS.getElements(DOM.Email.delete_confirm_buttons, "Confirmation buttons", False, 2, False)
        for i in x:
            if i.is_displayed() and i.text == "Delete":
                self.UTILS.logResult("info", "Clicking confirmation button.")
                # (click, not tap!)
                i.click()
                break
            
        #
        # "1 message deleted" displayed.
        #
        x = self.UTILS.getElement(DOM.Email.deleted_email_notif, "Email deletion notifier")
        
        #
        # Refresh and check that the message is no longer in the inbox.
        #
        x = self.marionette.find_element(*DOM.Email.folder_refresh_button)
        x.tap()
        time.sleep(5)
        x = self.UTILS.getElements(DOM.Email.folder_subject_list, "Email messages in this folder")

        self.UTILS.TEST(x[0].text != p_subject,
                        "Email '" + p_subject + "' no longer found in this folder.", False)
