import subprocess32
import time
from argparse import ArgumentParser
import get_latest_build
import zipfile
from utilities import Utilities


def flash(device, targetdir, buildfile):
    """Flash the device

    We must distinguish between hamachi-light and the rest of devices, because
    the flash method is different.
    """

    filedir = buildfile.split('.tgz')[0]
    if device == "hamachi-light":
        subprocess32.check_output('sudo {}/{}/update-gecko-gaia.sh'.format(targetdir, filedir), shell=True)
    else:
        subprocess32.check_output('sudo {}/{}/flash.sh'.format(targetdir, filedir), shell=True)
    print "Device successfully flashed!"


def wait_for_device():
    """Issue an adb command to wait for the device to be online
    """

    subprocess32.check_output('sudo adb wait-for-device', shell=True)


def get_device_build_date():
    """Return the date of the current build in the device."""

    output = subprocess32.check_output('sudo adb shell getprop | grep "build.date.utc]"', shell=True)
    print output
    build_date = output.split(": [")[-1].strip().replace("]", "")
    da = time.localtime(float(build_date))
    return time.strftime("%m-%d-%y", da)


def check_device_build(source, user, passwd, device_buildname):
    """Check if the device has already the latest available build.

    If the device has been already flashed with the latest available build,
    return True. False otherwise.
    """
    print "Checking current build's date in device"
    daf = get_device_build_date()
    print "Current build's date in device: {}".format(daf)

    # Check if the current build in device corresponds to the same Gaia commit (branch) as
    # the build to be flashed
    print "DEVICE_BUILDNAME: {}".format(device_buildname)
    gaia_commit = device_buildname.split("Gaia-")[1]
    print "Gaia version for last build: {}".format(gaia_commit)

    # Get gaia version in device, from resources/gaia_commit.txt inside the Settings application
    # First of all, pull the application from the device
    subprocess32.check_output('sudo adb pull /data/local/webapps/settings.gaiamobile.org/application.zip', shell=True)
    zf = zipfile.ZipFile('application.zip')
    device_gaia = zf.read('resources/gaia_commit.txt')[0:7]
    print "Gaia version in device: {}".format(device_gaia)
    if gaia_commit == device_gaia:
        print "Gaia versions match, no need to flash"
    else:
        print "Gaia versions DO NOT match"
    return gaia_commit == device_gaia


def main():
    parser = ArgumentParser()
    parser.add_argument("-d", "--device", dest="device", action="store", default="flame-KK", help="Target device")
    parser.add_argument("-u", "--username", dest="username", action="store", default="owdmoz",
                        help="Username for the releases server")
    parser.add_argument("-p", "--password", dest="passwd", action="store", default="gaia",
                        help="Password for the releases server")
    parser.add_argument("-s", "--source", dest="source", action="store",
                        default="http://owd.tid.es/releases/DEVELOP/", help="Releases server location")
    parser.add_argument("-t", "--targetdir", dest="targetdir", action="store", help="Directory where the builds are")
    parser.add_argument("-b", "--buildfile", dest="buildfile", action="store", help="Build file")
    options = parser.parse_args()

    # First of all, ensure device is connected
    Utilities.connect_device()

    last_flashed = check_device_build(options.source, options.username, options.passwd, options.buildfile)

    # Flash the device
    if not last_flashed:
        flash(options.device, options.targetdir, options.buildfile)
        # Wait for the device to be available
        wait_for_device()
        # And reconnect to it
        Utilities.connect_device()
    else:
        print "Last build detected on the device. No need to flash."


if __name__ == '__main__':
    main()
