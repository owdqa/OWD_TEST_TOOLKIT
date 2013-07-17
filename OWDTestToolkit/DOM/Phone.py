frame_locator          = ('src', 'dialer')
frame_locator_calling  = ('name', 'call_screen0')

# Beware:
# 1. this number may have a country code prefix on it.
# 2. It's VERY weird ...
#
#    You can find it but not read it in any way, so use it like this:
#
#         x = self.UTILS.getElement( ("xpath", 
#                                     DOM.Phone.phone_number_xpath % self.NUMBER),
#                                 "The phone number '%s'" % self.NUMBER,
#                                 False)
phone_number_xpath     = "//div[@id='fake-phone-number-view' and contains(text(),'%s')]"

add_to_contacts_button = ("id", "keypad-callbar-add-contact")
create_new_contact_btn = ("id", "create-new-contact-menuitem")
call_number_button     = ("id", "keypad-callbar-call-action")

outgoing_call_locator  = ('css selector', 'div.direction.outgoing')
hangup_bar_locator     = ('id', 'callbar-hang-up-action')

