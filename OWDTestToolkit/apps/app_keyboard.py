# -*- coding: UTF-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from gaiatest.apps.base import Base
from marionette.marionette import Actions


class Keyboard(Base):

    name = "Keyboard"

    # special characters look-up table in English standard keyboard
    lookup_table = {'0': 'º',
                    '?': '¿',
                    '$': '€£¥',
                    '!': '¡',
                    'a': 'áàâäåãāæ',
                    'c': 'çćč',
                    'e': 'éèêëēę€ɛ',
                    'i': 'įīîìíï',
                    'l': '£ł',
                    'n': 'ńñ',
                    'o': 'ɵøœōôòóö',
                    's': 'ßśš$',
                    'u': 'ūûùúü',
                    'y': '¥ÿ',
                    'z': 'žźż',
                    'A': 'ÁÀÂÄÅÃĀÆ',
                    'C': 'ÇĆČ',
                    'E': 'ÉÈÊËĒĘ€Ɛ',
                    'I': 'ĮĪÎÌÍÏ',
                    'L': '£Ł',
                    'N': 'ŃÑ',
                    'O': 'ƟØŒŌÔÒÓÖ',
                    'S': 'ŚŠŞ',
                    'U': 'ŪÛÙÚÜ',
                    'Y': '¥Ÿ',
                    'Z': 'ŽŹŻ'}

    # special keys locators
    _language_key = '-3'
    _numeric_sign_key = '-2'
    _alpha_key = '-1'
    _backspace_key = '8'
    _enter_key = '13'
    _alt_key = '18'
    _upper_case_key = '20'
    _space_key = '32'

    # keyboard app locators
    _keyboard_frame_locator = ('css selector', '#keyboard-frame iframe')
    _keyboard_locator = ('css selector', '#keyboard')
    _button_locator = ('css selector', 'button.keyboard-key[data-keycode="%s"]')
    _highlight_key_locator = ('css selector', 'div.highlighted button')

    # find the key to long press and return
    def _find_key_for_longpress(self, input_value):
        for key_to_press, extended_values in self.lookup_table.iteritems():
            if input_value in extended_values:
                return key_to_press

    # trying to switch to right layout
    def _switch_to_correct_layout(self, val):
        # alpha is in on keyboard
        if val.isalpha():
            if self.is_element_present(*self._key_locator(self._alpha_key)):
                self._tap(self._alpha_key)
            if not self.is_element_present(*self._key_locator(val)):
                self._tap(self._upper_case_key)
        # numbers and symbols are in another keyboard
        else:
            if self.is_element_present(*self._key_locator(self._numeric_sign_key)):
                self._tap(self._numeric_sign_key)
            if not self.is_element_present(*self._key_locator(val)):
                self._tap(self._alt_key)

    # this is to switch to the frame of keyboard
    def _switch_to_keyboard(self):
        self.marionette.switch_to_frame()
        keybframe = self.marionette.find_element(*self._keyboard_frame_locator)
        self.marionette.switch_to_frame(keybframe, focus=False)

    # this is to get the locator of desired key on keyboard
    def _key_locator(self, val):
        if len(val) == 1:
            val = ord(val)
        return (self._button_locator[0], self._button_locator[1] % val)

    # this is to tap on desired key on keyboard
    def _tap(self, val):
        self.wait_for_element_displayed(*self._key_locator(val))
        key = self.marionette.find_element(*self._key_locator(val))
        key.tap()

    # This is for selecting special characters after long pressing
    # "selection" is the nth special element you want to select (n>=1)
    def choose_extended_character(self, long_press_key, selection, movement=True):
        self._switch_to_keyboard()
        action = Actions(self.marionette)

        # after switching to correct keyboard, set long press if the key is there
        self._switch_to_correct_layout(long_press_key)
        key = self._key_locator(long_press_key)
        if self.is_element_present(*key):
            keyobj = self.marionette.find_element(*key)
            action.press(keyobj).wait(2).perform()
        else:
            assert False, 'Key %s not found on the keyboard' % long_press_key

        # find the extended key and perform the action chain
        extend_keys = self.marionette.find_elements(*self._highlight_key_locator)
        if movement == True:
            action.move(extend_keys[selection - 1]).perform()
        action.release().perform()
        time.sleep(0.8)

        self.marionette.switch_to_frame()

    def enable_caps_lock(self):
        self._switch_to_keyboard()
        if self.is_element_present(*self._key_locator(self._alpha_key)):
            self._tap(self._alpha_key)
        key_obj = self.marionette.find_element(*self._key_locator(self._upper_case_key))
        self.marionette.double_tap(key_obj)
        self.marionette.switch_to_frame()

    # this is to detect if the element is present in a shorter time
    # default timeout to 600 and allow people to set a higher timeout
    def is_element_present(self, by, locator, timeout=600):
        try:
            self.marionette.set_search_timeout(timeout)
            self.marionette.find_element(by, locator)
            return True
        except:
            return False
        finally:
            # set the search timeout to the default value
            self.marionette.set_search_timeout(10000)

    # do a long press on a character
    def long_press(self, key, timeout=2000):
        if len(key) == 1:
            self._switch_to_keyboard()
            key_obj = self.marionette.find_element(*self._key_locator(key))
            action = Actions(self.marionette)
            action.press(key_obj).wait(timeout/1000).release().perform()
            self.marionette.switch_to_frame()

    # this would go through fastest way to tap/click through a string
    def send(self, string):
        self._switch_to_keyboard()
        for val in string:
            if ord(val) > 127:
                # this would get the right key to long press and switch to the right keyboard
                middle_key_val = self._find_key_for_longpress(val.encode('UTF-8'))
                self._switch_to_correct_layout(middle_key_val)
  
                # find the key to long press and press it to get the extended characters list
                middle_key = self.marionette.find_element(*self._key_locator(middle_key_val))
                action = Actions(self.marionette)
                action.press(middle_key).wait(2).perform()
  
                # find the targeted extended key to send
                target_key = self.marionette.find_element(*self._key_locator(val))
                action.move(target_key).release().perform()
            else:
                # after switching to correct keyboard, tap/click if the key is there
                self._switch_to_correct_layout(val)
                if self.is_element_present(*self._key_locator(val)):
                    self._tap(val)
                else:
                    assert False, 'Key %s not found on the keyboard' % val
 
            # after tap/click space key, it might get screwed up due to timing issue. adding 0.8sec for it.
            if ord(val) == int(self._space_key):
                time.sleep(0.8)
        self.marionette.switch_to_frame()

    # switch to keyboard with numbers and special characters
    def switch_to_number_keyboard(self):
        self._switch_to_keyboard()
        self._tap(self._numeric_sign_key)
        self.marionette.switch_to_frame()

    # switch to keyboard with alphabetic keys
    def switch_to_alpha_keyboard(self):
        self._switch_to_keyboard()
        self._tap(self._alpha_key)
        self.marionette.switch_to_frame()

    # following are "5 functions" to substitute finish switch_to_frame()s and tap() for you
    def tap_shift(self):
        self._switch_to_keyboard()
        if self.is_element_present(*self._key_locator(self._alpha_key)):
            self._tap(self._alpha_key)
        self._tap(self._upper_case_key)
        self.marionette.switch_to_frame()

    def tap_backspace(self):
        self._switch_to_keyboard()
        bs = self.marionette.find_element(self._button_locator[0], self._button_locator[1] % self._backspace_key)
        bs.tap()
        self.marionette.switch_to_frame()

    def tap_space(self):
        self._switch_to_keyboard()
        self._tap(self._space_key)
        self.marionette.switch_to_frame()

    def tap_enter(self):
        self._switch_to_keyboard()
        self._tap(self._enter_key)
        self.marionette.switch_to_frame()

    def tap_alt(self):
        self._switch_to_keyboard()
        if self.is_element_present(*self._key_locator(self._numeric_sign_key)):
            self._tap(self._numeric_sign_key)
        self._tap(self._alt_key)
        self.marionette.switch_to_frame()
