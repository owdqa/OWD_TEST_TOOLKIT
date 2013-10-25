from twilio.rest import TwilioRestClient

from OWDTestToolkit.global_imports import *


class main(GaiaTestCase):

    def createIncomingCall(self, num):

        account_sid = "ACd3d2699e42974fd163129ff8a7530e56"
        auth_token = "0ac68cfbf12aa7e0725da1750da609b7"
        client = TwilioRestClient(account_sid, auth_token)

        client.calls.create(url="http://demo.twilio.com/docs/voice.xml",
                            to=num,
                            from_= "+34518880854")
