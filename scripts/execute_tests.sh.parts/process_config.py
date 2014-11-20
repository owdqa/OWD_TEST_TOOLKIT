from argparse import ArgumentParser
from ConfigParser import ConfigParser
import os


def main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument('files', metavar='N', type=str, nargs='+', help='config file names')
    options = arg_parser.parse_args()
    config_parser = ConfigParser()
    files = options.files
    ok_files = config_parser.read(files)
    if len(ok_files) == len(files):
        print "All configuration files read successfully."
    else:
        print "Some configuration files could not be processed:"
        nok = filter(lambda name: name not in ok_files, files)
        for f in nok:
            print "    * {}".format(f)
    for section in config_parser.sections():
        print "Section: {}".format(section)
        for (name, value) in config_parser.items(section):
            print "    {}: {}".format(name, value)
        os.environ[name.upper()] = value
        os.system("export {}={}".format(name.upper(), value))
    print os.environ.keys()

if __name__ == '__main__':
    main()
