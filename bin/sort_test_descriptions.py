import json
import csv
import os
import re
import sys

class TestDescriptions():
    def __init__(self, args):
        if len(args) != 2:
            raise Exception("You need to pass as parameters the JSON file containing the descriptions and the path to the tests")
                
        self.file_to_parse = args[0]
        self.tests_path = args[1]
        self.descriptions_by_suite = {}
        self.file_descriptions = self._parse_file(self.file_to_parse)
#         print "file descriptions: {}".format(self.file_descriptions)
    
    def _parse_file(self, file_name):
        """ Generic JSON parser.
            It takes a JSON file as an input and returns a dictionary containing all
            its properties.
        """
        the_file = open(file_name)
        data = json.load(the_file)
        the_file.close()
        return data
    
    def generate_csv_file(self):
        pass
    
    def get_test_descriptions_by_suite(self, sort=True):
        if os.path.isdir(self.tests_path):
            for root, dirs, files in os.walk(self.tests_path):
                root = root.split("/")[-1]
#                 print "Root: {}".format(root)
                for filename in files:
                    m = re.search('^test_(\d+).py$', filename)
                    if m:
                        test_number = m.group(1)                       
                        if not self.descriptions_by_suite.has_key(root):
                            if self.file_descriptions.has_key(test_number):
                                self.descriptions_by_suite[root] = [(test_number, self.file_descriptions[test_number])]
                        else:
                            if self.file_descriptions.has_key(test_number):
                                self.descriptions_by_suite[root].append((test_number, self.file_descriptions[test_number]))
        else:
            raise Exception
        
        if sort:
            import collections
            self.descriptions_by_suite = collections.OrderedDict(sorted(self.descriptions_by_suite.items(), key=lambda t: t[0])) 
    
    def display(self):
        for key, value in self.descriptions_by_suite.items():
            print "*********** {} ************".format(key)
            for test_data in value:
                print "{}: {}".format(test_data[0], test_data[1].encode("utf-8"))

if __name__ == "__main__":
    td = TestDescriptions(sys.argv[1:])
    td.get_test_descriptions_by_suite()
    td.display()