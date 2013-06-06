from OWDTestToolkit.global_imports import *

import  choose_extended_character          ,\
        enable_caps_lock                   ,\
        _find_key_for_longpress            ,\
        is_element_present                 ,\
        _key_locator                       ,\
        long_press                         ,\
        send                               ,\
        switch_to_alpha_keyboard           ,\
        _switch_to_correct_layout          ,\
        _switch_to_keyboard                ,\
        switch_to_number_keyboard          ,\
        tap_alt                            ,\
        tap_backspace                      ,\
        tap_enter                          ,\
        _tap                               ,\
        tap_shift                          ,\
        tap_space                          

class Keyboard (
            choose_extended_character.main,
            enable_caps_lock.main,
            _find_key_for_longpress.main,
            is_element_present.main,
            _key_locator.main,
            long_press.main,
            send.main,
            switch_to_alpha_keyboard.main,
            _switch_to_correct_layout.main,
            _switch_to_keyboard.main,
            switch_to_number_keyboard.main,
            tap_alt.main,
            tap_backspace.main,
            tap_enter.main,
            _tap.main,
            tap_shift.main,
            tap_space.main):
    
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

