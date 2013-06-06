from OWDTestToolkit.global_imports import *

import  countEmailAddressesWhileEditing , \
        getContactFields                , \
        replaceStr                      , \
        populateFields                  , \
        checkMatch                      , \
        verifyFieldContents             , \
        addGalleryImageToContact        , \
        createNewContact                , \
        startCreateNewContact           , \
        populateContactFields           , \
        verifyImageInAllContacts        , \
        viewContact                     , \
        tapSettingsButton               , \
        checkViewContactDetails         , \
        pressEditContactButton          , \
        pressCancelEditButton           , \
        checkEditContactDetails         , \
        editContact                     , \
        switchToFacebook                , \
        tapLinkContact                  , \
        enableFBImport                  , \
        verifyLinked                    , \
        changeVal                       , \
        search                          , \
        checkSearchResults              , \
        pressDeleteContactButton        , \
        deleteContact                   , \
        addAnotherEmailAddress


class Contacts(  countEmailAddressesWhileEditing.main,
                    getContactFields.main,
                    replaceStr.main,
                    populateFields.main, 
                    checkMatch.main,
                    verifyFieldContents.main,
                    addGalleryImageToContact.main,
                    createNewContact.main,
                    startCreateNewContact.main,
                    populateContactFields.main,
                    verifyImageInAllContacts.main,
                    viewContact.main,
                    tapSettingsButton.main,
                    checkViewContactDetails.main,
                    pressEditContactButton.main,
                    pressCancelEditButton.main,
                    checkEditContactDetails.main,
                    editContact.main,
                    switchToFacebook.main,
                    tapLinkContact.main,
                    enableFBImport.main,
                    verifyLinked.main,
                    changeVal.main,
                    search.main,
                    checkSearchResults.main,
                    pressDeleteContactButton.main,
                    deleteContact.main,
                    addAnotherEmailAddress.main):
    
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
        self.app = self.apps.launch(self.__class__.__name__)
        self.UTILS.waitForNotElements(DOM.GLOBAL.loading_overlay, self.__class__.__name__ + " app - loading overlay")
        
