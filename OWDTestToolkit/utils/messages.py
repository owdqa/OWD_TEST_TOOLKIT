import json
import requests
import binascii
from pigeon import pigeonpdu


class Messages(object):

    def __init__(self, parent):
        self.parent = parent
        self.api_key = parent.general.get_os_variable("PIGEON_API_KEY")
        self.api_secret = parent.general.get_os_variable("PIGEON_API_SECRET")
        self.url = parent.general.get_os_variable("PIGEON_URL")

    def create_incoming_cp(self, phone_number, pintype, ota_filename, pin_number=None):
        """Create incoming client provisioning message

        Description: This method send an incoming OTA CP notification
        phone_number: phone number used to receive the notification
        pin_type: Specifies the type of PIN specified in the OTAPIN variable.
            Can either be a value of USERPIN, NETWPIN, or USERNETWPIN.
            The value must be Uppercase, if not will be converted.
        pin_number: short pin code (often 4 digits)
        ota_filename: The file name contained the OTA XML configuration.
        """
        headers = {"api_key": self.api_key, "api_secret": self.api_secret,
                   "content-type": "application/x-www-form-urlencoded"}

        pigeon = pigeonpdu.PigeonPDU()
        user_data = pigeon.getXMLPushUserdata(ota_filename, pintype, pin_number)
        pdu_data = binascii.hexlify(user_data)
        self.parent.test.TEST(True, "Sending CP message to {} from file {}".format(phone_number, ota_filename))

        data = {"dataCodingScheme": "F5", "protocolId": "00", "pduType": "41", "sourcePort": 9200,
                "destinationPort": 2948, "pduData": "{}".format(pdu_data)}
        payload = {"to": [phone_number], "binaryMessage": data}

        response = requests.post(self.url, headers=headers, data=json.dumps(payload))
        result = response.status_code == requests.codes.ok
        self.parent.test.TEST(result, "The provisioning message could {}be sent. Status code: {}. Body: {}".\
                              format("not " if not result else "", response.status_code, response.text))
        return result

    def create_incoming_sms(self, phone_number, message):
        """Create Incoming SMS

        Use Pigeon API to send a SMS to the given number and with the specified text.
        """
        headers = {"api_key": self.api_key, "api_secret": self.api_secret}
        payload = {"to": [phone_number], "message": message}
        requests.post(self.url, headers=headers, data=json.dumps(payload))

    def create_incoming_wap_push(self, phone_number, wap_url, message=""):
        """Create an incoming WAP Push message

        This method sends a WAP Push message to the specified phone number
        phone_number: phone number used to receive the notification
        wap_url: the URL we want to open
        message: alert text
        """
        # if text == "":
        #    url = 'http://10.95.193.226:8800/?PhoneNumber=' + phoneNumber + '&WAPURL=' + WAPURL
        #    requests.get(url, auth=('owd', 'owdqa'))
        # else:
        #    url = 'http://10.95.193.226:8800/?PhoneNumber=' + phoneNumber + '&WAPURL=' + WAPURL + '&Text=' + text
        #    requests.get(url, auth=('owd', 'owdqa'))
        headers = {"api_key": self.api_key, "api_secret": self.api_secret}
        payload = {"to": [phone_number], "message": message}
        requests.post(self.url, headers=headers, data=json.dumps(payload))
