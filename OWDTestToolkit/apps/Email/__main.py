from OWDTestToolkit.global_imports import *

import  deleteEmail                        ,\
        emailIsInFolder                    ,\
        goto_folder_from_list              ,\
        openMailFolder                     ,\
        openMsg                            ,\
        remove_accounts_and_restart        ,\
        send_new_email                     ,\
        sendTheMessage                     ,\
        setupAccount                       ,\
        switchAccount                      ,\
        waitForDone                        

class Email (
            deleteEmail.main,
            emailIsInFolder.main,
            goto_folder_from_list.main,
            openMailFolder.main,
            openMsg.main,
            remove_accounts_and_restart.main,
            send_new_email.main,
            sendTheMessage.main,
            setupAccount.main,
            switchAccount.main,
            waitForDone.main):
    
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
        self.app = self.apps.launch(self.__class__.__name__)
        self.UTILS.waitForNotElements(DOM.GLOBAL.loading_overlay, self.__class__.__name__ + " app - loading overlay")
        return self.app

