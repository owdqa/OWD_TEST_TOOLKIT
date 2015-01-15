frame_locator = ('src', 'app://wappush')

CP_Windows_Pin = ("xpath", '//input[@data-l10n-id="cp-pin"]')
CP_Accept_Button = ("xpath", '//button[@id="accept"]')
CP_Store_Button = ("xpath", '//form[@id="cp-store-confirm"]//button[@data-l10n-id="store"]')

CP_OTA_Message = ("xpath", "//form[@id='cp-finish-confirm']//p/strong[@data-l10n-id='cp-finish-confirm-dialog-message']")
CP_Finish_Button = ("xpath", '//form[@id="cp-finish-confirm"]//button[@data-l10n-id="finish"]')

CP_Close_Button = ('id', 'close')
CP_Cancel_Button = ("xpath", '//form[@id="cp-store-confirm"]//button[@data-l10n-id="cancel"]')
CP_Cancel_Message = ("xpath", '//form[@id="cp-quit-app-confirm"]//strong[@data-l10n-id="cp-quit-app-confirm-dialog-message"]')
CP_Quit_Button = ("xpath", '//form[@id="cp-quit-app-confirm"]//button[@data-l10n-id="quit"]')
CP_Confirm_Cancel = ("xpath", '//form[@id="cp-quit-app-confirm"]//button[@data-l10n-id="cancel"]')