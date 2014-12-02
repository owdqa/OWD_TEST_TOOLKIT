import os
from datetime import datetime
from csv import DictWriter


class CsvWriter(object):

    def __init__(self, device, version):
        self.device = device
        self.version = version

    def create_report(self, fieldnames, row, outfile, daily=True):
        """Create a new entry in the CSV report file.

        Write a new row in the CSV report file given by outfile, corresponding to the
        fields in fieldnames. If daily is True, it will generate a different header, if the
        file is not found.
        """
        write_header = False
        if not os.path.isfile(outfile):
            write_header = True
        with open(outfile, 'a+') as csvfile:
            csvwriter = DictWriter(csvfile, fieldnames=fieldnames, delimiter=',', lineterminator='\n')
            headers = dict((h, h) for h in fieldnames)
            # If the file is new, let's write the required header
            if write_header:
                # Write the week number, in the ISO 8601 format
                header = self.generate_header(daily)
                csvfile.write(header)
                # Write the CSV header row
                csvwriter.writerow(headers)
            # Write the data
            csvwriter.writerow(row)

    def generate_header(self, daily=True):
        header = ""
        if daily:
            header = "Last test executions, DATE: {}\n".format(datetime.now().strftime("%d/%m/%Y %H:%M"))
            header += "Device: {}\n".format(self.device)
            header += "Version: {}\n".format(self.version)
        else:
            header = "WEEK NUMBER: {}\n".format(datetime.now().isocalendar()[1])
        return header
