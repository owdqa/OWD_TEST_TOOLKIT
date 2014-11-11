from pyquery import PyQuery as pq
from lxml import etree
import re

if __name__ == '__main__':
    d = pq(filename="/tmp/tests/results.html")
    print d.find('.col-class')[0].text
    test_names = [re.search('^test_(\d+).*$', testname.text).group(1) for testname in d('.col-class')]
    print test_names
    links = d('.col-links')
    
    i = 0
    for link in links:
        pq(link).append(etree.fromstring('<a class="details" href="test_123/{}_detail" target="_blank">Details</a>'.format(test_names[i])))
        i += 1
        
    print len(test_names)
    print len(links)