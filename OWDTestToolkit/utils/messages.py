import binascii
import json
import requests
from pigeon import pigeonpdu


class Messages(object):

    def __init__(self, parent):
        self.parent = parent
        self.api_key = parent.general.get_os_variable("PIGEON_API_KEY")
        self.api_secret = parent.general.get_os_variable("PIGEON_API_SECRET")
        self.url = parent.general.get_os_variable("PIGEON_URL")

    def create_incoming_cp(self, phone_number, pin_type, ota_filename, pin_number=None):
        """Create incoming client provisioning message

        Description: This method send an incoming OTA CP notification
        phone_number: phone number used to receive the notification
        pin_type: Specifies the type of PIN specified in the OTAPIN variable.
            Can either be a value of NONE, USERPIN, NETWPIN, or USERNETWPIN.
            The value must be Uppercase, it not will be converted.
        pin_number: short pin code (often 4 digits)
        ota_filename: The file name contained the OTA XML configuration.
        """
        headers = {"api_key": self.api_key, "api_secret": self.api_secret,
                   "content-type": "application/x-www-form-urlencoded"}

        pigeon = pigeonpdu.PigeonPDU()
        user_data = pigeon.getXMLPushUserdata(ota_filename, pin_number)
        pdu_data = binascii.hexlify(user_data)
        # If no security is used, we must extract that part from the PDU.
        if pin_type is "NONE":
            pdu_data = pdu_data[0:4] + "01b6" + pdu_data[pdu_data.index("030b6a2f"):]
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

    def create_incoming_wap_push(self, phone_number, typ, wap_url, message="", action='signal-medium'):
        """Create an incoming WAP Push message

        This method sends a WAP Push message to the specified phone number
        phone_number: phone number used to receive the notification
        typ: type of the WAP Push message. Valid values are 'si' and 'sl'
        wap_url: the URL we want to open
        message: alert text
        """
        headers = {"api_key": self.api_key, "api_secret": self.api_secret}
        pigeon = pigeonpdu.PigeonPDU()
        pdu_data = pigeon.generate_wap_push_pdu(typ, wap_url, message)
        self.parent.test.TEST(True, "PDU_DATA: {}".format(binascii.hexlify(pdu_data)))
        data = {"dataCodingScheme": "F5", "protocolId": "00", "pduType": "41", "sourcePort": 9200,
                "destinationPort": 2948, "pduData": "{}".format(binascii.hexlify(pdu_data))}
        payload = {"to": [phone_number], "binaryMessage": data}
        response = requests.post(self.url, headers=headers, data=json.dumps(payload))
        result = response.status_code == requests.codes.ok
        self.parent.test.TEST(result, "The WAP PUSH message could {}be sent. Status code: {}. Body: {}".\
                              format("not " if not result else "", response.status_code, response.text))
        return result

    def create_incoming_cp_nowsms(self, phoneNumber, pinType, otaFilename, pinNumber=None):
        """Send an incoming OTA CP notification.

        phoneNumber: phone number used to receive the notification
        pinType: Specifies the type of PIN specified in the OTAPIN variable. Can either be a value of USERPIN,
        NETWPIN, or USERNETWPIN.
        The value must be uppercase, if not will be converted.
        pinNumber: short pin code (often 4 digits)
        otaFilename: The file name contained the OTA XML configuration. This file must be saved in OTA folder
        of nowSMS.
        """

        if (pinNumber != None):
            url = 'http://10.95.193.226:8800/?PhoneNumber=' + phoneNumber + '&OTAPINTYPE=' + pinType.upper() + \
                    '&OTAPIN=' + pinNumber + '&OTA=' + otaFilename
        else:
            url = 'http://10.95.193.226:8800/?PhoneNumber=' + phoneNumber + '&OTA=' + otaFilename

        self.logResult("URL", "Current url is: " + url)

        requests.get(url, auth=('owd', 'owdqa'))
