import requests
import re
from bs4 import BeautifulSoup
from argparse import ArgumentParser
import os

def detect_latest_date(source, user, passwd):
    """Detect the latest date for build available"""

    params = "?C=M&O=D"
    url = source + params
    response = requests.get(url, auth=(user, passwd))
    html = response.text
    soup = BeautifulSoup(html)
    dates = [d.text[:-1] for d in soup.find_all("a", href=re.compile("..-..-.."))]
    last_date = dates[0]
    print "Latest date: {}".format(last_date)
    return last_date

def detect_build_file(source, user, passwd, device, typ, branch, last_date):
    """Detect the build filename based on the last date directory contents"""

    params = "?C=M&O=D"
    url = source + last_date + params
    print "Retrieving url: {}".format(url)
    response = requests.get(url, auth=(user, passwd))
    html = response.text
    soup = BeautifulSoup(html)
    elem = soup.find("a", href=re.compile("{}.*{}.*{}.*AutomationVersion.*".format(device, typ, branch)))
    print "Release file: {}".format(elem.text)
    return elem.text

def download_build(source, user, passwd, last_date, filename, outdir):
    """Download the build file"""

    print "Downloading build file: {}".format(filename)
    url = source + last_date + '/' + filename
    print "Url: {}".format(url)
    r = requests.get(url, stream=True, auth=(user, passwd))
    with open(outdir + '/' + filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=16384): 
            if chunk:
                f.write(chunk)
                f.flush()

def main():
    parser = ArgumentParser()
    parser.add_argument("-d", "--device", dest="device", action="store", default="flame-KK", help="Target device")
    parser.add_argument("-t", "--type", dest="build_type", action="store", default="eng", help="Build type (eng or user)")
    parser.add_argument("-b", "--branch", dest="branch", action="store", default="v2.1", help="Branch")
    parser.add_argument("-u", "--username", dest="username", action="store", default="owdmoz", help="Username for the releases server")
    parser.add_argument("-p", "--password", dest="passwd", action="store", default="gaia", help="Password for the releases server")
    parser.add_argument("-s", "--source", dest="source", action="store", default="http://ci-owd-misc-02/releases/DEVELOP/",
                        help="Releases server location")

    home = os.environ['HOME']
    default_dir = "{}/Downloads/device_flash_files".format(home)
    if not os.path.exists(default_dir):
        os.makedirs(default_dir)
    parser.add_argument("-o", "--outdir", dest="outdir", action="store", default=default_dir,
                        help="Destination directory for downloaded build files")
    options = parser.parse_args()

    last_date = detect_latest_date(options.source, options.username, options.passwd)
    f = detect_build_file(options.source, options.username, options.passwd, options.device, options.build_type, options.branch, last_date)
    download_build(options.source, options.username, options.passwd, last_date, f, options.outdir)

if __name__ == '__main__':
    main()
