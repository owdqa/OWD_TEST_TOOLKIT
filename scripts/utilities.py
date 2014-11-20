import json
import os


class Utilities():

    @staticmethod
    def parse_file(file_name):
        """ Generic JSON parser.

        It takes a JSON file as an input and returns a dictionary containing all
        its properties.
        """
        the_file = open(file_name)
        data = json.load(the_file)
        the_file.close()
        return data

    @staticmethod
    def detect_device(testvars):
        """Customize parameters based on the DuT.
        """
        # Ensure device is connected and ports forwarded properly
        Utilities.connect_device()

        current_dut = os.popen("adb shell grep ro.product.name /system/build.prop").read().split("=")[-1].rstrip()
        devices_path = "{}/{}".format(testvars['toolkit_location'], testvars['toolkit_cfg']['devices_cfg'])
        devices_map = Utilities.parse_file(devices_path)

        if not current_dut in devices_map:
            print "No specific section for device [{}] was found. Falling down to [generic] device options.".\
                format(current_dut)
            current_dut = "generic"

        device_config = {}
        for item in devices_map[current_dut].keys():
            device_config["OWD_DEVICE_" + item.upper()] = devices_map[current_dut][item]

        for key in device_config.keys():
            testvars[key] = device_config[key]

    @staticmethod
    def connect_device():
        """Force connection to device and forward ports, just in case.
        """
        os.popen("adb kill-server")
        os.popen("adb devices")
        os.popen("adb forward tcp:2828 tcp:2828")
