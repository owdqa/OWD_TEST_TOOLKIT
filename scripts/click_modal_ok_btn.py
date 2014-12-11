#!/usr/bin/python2.7
#
# Script to work around Marionette bug 879816 (cannot click the modal 'ok' button
# following clicking something else).
#
from marionette import Marionette
marionette = Marionette(host='localhost', port=2828)
marionette.start_session()
marionette.switch_to_frame()
marionette.execute_script("document.getElementById('modal-dialog-prompt-ok').click();")
