import subprocess32
import time
from argparse import ArgumentParser
import get_latest_build
from utilities import Utilities


def flash(device):
    """Flash the device

    We must distinguish between hamachi-light and the rest of devices, because
    the flash method is different.
    """

    if device == "hamachi-light":
        subprocess32.check_call(['sudo', './update-gecko-gaia.sh'])
    else:
        subprocess32.check_call(['sudo', './flash.sh'])
    print "Device successfully flashed!"


def wait_for_device():
    """Issue an adb command to wait for the device to be online
    """

    subprocess32.check_output(['sudo', 'adb', 'wait-for-device'])


def get_device_build_date():
    output = subprocess32.check_output('sudo adb shell getprop | grep "build.date.utc]"', shell=True)
    build_date = output.split(": [")[-1].strip().replace("]", "")
    da = time.localtime(float(build_date))
    return time.strftime("%m-%d-%y", da)


def check_device_build(source, user, passwd):
    """Check if the device has already the latest available build.

    If the device has been already flashed with the latest available build,
    return True. False otherwise.
    """
    daf = get_device_build_date()
    print "Current build's date in device: {}".format(daf)
    last_date = get_latest_build.detect_latest_date(source, user, passwd)
    return daf == last_date


def main():
    parser = ArgumentParser()
    parser.add_argument("-d", "--device", dest="device", action="store", default="flame-KK", help="Target device")
    parser.add_argument("-u", "--username", dest="username", action="store", default="owdmoz",
                        help="Username for the releases server")
    parser.add_argument("-p", "--password", dest="passwd", action="store", default="gaia",
                        help="Password for the releases server")
    parser.add_argument("-s", "--source", dest="source", action="store",
                        default="http://ci-owd-misc-02/releases/DEVELOP/", help="Releases server location")
    options = parser.parse_args()

    # First of all, ensure device is connected
    Utilities.connect_device()

    last_flashed = check_device_build(options.source, options.username, options.passwd)

    # Flash the device
    if not last_flashed:
        flash(options.device)
        # Wait for the device to be available
        wait_for_device()
        # And reconnect to it
        Utilities.connect_device()
    else:
        print "Last build detected on the device. No need to flash."


if __name__ == '__main__':
    main()
