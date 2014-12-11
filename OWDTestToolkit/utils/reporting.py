from bs4 import BeautifulSoup
import time
import datetime
import logging
import re

class reporting(object):

    def __init__(self, parent):
        self.parent = parent
        self.result_array = []
        self.comment_array = []
        self.init_time = time.time()
        self.test_num = self.parent.parent.__module__[5:]
        self.detail_file = "{}/{}_detail.html".format(self.parent.general.get_config_variable('result_dir', 'output'),
                                                      self.test_num)
        self.logger = logging.getLogger('OWDTestToolkit')

    def log_to_file(self, message, level='info'):
        if level in ('critical', 'error', 'warn', 'info', 'debug'):
            f = self.logger.__getattribute__(level)
            f(message)
        else:
            self.logger.info(message)

    def critical(self, message):
        self.logger.critical(message)

    def error(self, message):
        self.logger.error(message)

    def warn(self, message):
        self.logger.warn(message)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def logComment(self, comment):
        #
        # Add a comment to the comment array.
        #
        self.comment_array.append(comment)
        self.logger.info("Adding comment: {}".format(comment))

    def _get_timestamp(self):
        time_now = round(time.time() - self.init_time, 0)
        time_now = str(datetime.timedelta(seconds=time_now))
        return "[{}]".format(time_now)

    def logResult(self, msg_type, msg, details=False):
        self.logger.info(u"Logging result: [{}] with message [{}]. p_fnam: {}".format(msg_type, msg, details))
        log = {'msg_type': str(msg_type),
               'timestamp': self._get_timestamp(),
               'msg': "DEBUG NOTE: " + msg if msg_type is 'debug' else msg,
               }
        if details:
            log['details'] = details

        self.result_array.append(log)

    def _extract_html_from_log(self, soup, parent_node, log):
            def _fill_detail(outer_class, inner_tag_type, content):
                outer_tag = soup.new_tag('div', **{'class': outer_class})
                inner_tag = soup.new_tag(inner_tag_type, href=content, target="_blank") if inner_tag_type == "a" else\
                            soup.new_tag(inner_tag_type)
                inner_tag.string = "Link to {}".format(outer_class) if inner_tag_type == "a" else content
                outer_tag.append(inner_tag)
                return outer_tag

            new_log_tag = soup.new_tag("li", **{'class': 'log {}'.format(log['msg_type'])})

            timestamp_tag = soup.new_tag('span', **{'class': 'timestamp'})
            timestamp_tag.string = log['timestamp']
            new_log_tag.append(timestamp_tag)

            msg_tag = soup.new_tag('span', **{'class': 'message'})
            
            results = re.search("^(.*)(<[b|i]>)(.*)</\w>(.*)", log['msg'])
            if results: # If match, this will always have 4 groups
                if results.group(2) == '<b>':
                    msg_rich_tag = soup.new_tag('span', **{'class': 'bold'})
                    msg_rich_tag.string = results.group(3)
                elif results.group(2) == '<i>':
                    msg_rich_tag = soup.new_tag('span', **{'class': 'italic'})
                    msg_rich_tag.string = results.group(3)
                else:
                    msg_rich_tag = soup.new_tag('span')
                    msg_rich_tag.string = results.group(3)
                    
                msg_tag.append(results.group(1))
                msg_tag.append(msg_rich_tag)
                msg_tag.append(soup.new_string(results.group(4)))
            else:
                msg_tag.string = log['msg']

            new_log_tag.append(msg_tag)

            if 'details' in log:
                details = log['details']
                details_tag = soup.new_tag('div', **{'class': 'details'})

                # Different scenarios here:
                #    a) 3 elements: DOM_locator, screenshot, html_dump
                #    b) 2 elements: screenshot, html_dump
                #    c) 1 element: just a detail

                if len(details) == 3:
                    details_tag.append(_fill_detail('locator', 'p', details[2]))
                    details_tag.append(_fill_detail('screenshot', 'a', details[1]))
                    details_tag.append(_fill_detail('html-dump', 'a', details[0]))
                elif len(details) == 2:
                    details_tag.append(_fill_detail('screenshot', 'a', details[1]))
                    details_tag.append(_fill_detail('html-dump', 'a', details[0]))
                elif len(details) == 1:
                    details_tag.append(_fill_detail('detail', 'p', details[0]))

                new_log_tag.append(details_tag)

            return new_log_tag

    def reportResults(self):
        detail_html_template = open("{}/{}".format(self.parent.data_layer.testvars['toolkit_cfg']['toolkit_location'],
                                      self.parent.data_layer.testvars['toolkit_cfg']['results_template']))
        soup = BeautifulSoup(detail_html_template)
        detail_html_template.close()

        soup.title.string = "{} {}".format(self.test_num, soup.title.string)

        test_number = soup.find("span", id="test-number")
        test_number.string = self.test_num

        if len(self.comment_array) > 0:
            comments_title = soup.find("span", id="comments-title")
            comments_title.string = "Comments"

            comment_list = soup.find("ul", id="comments-list")
            for comment in self.comment_array:
                new_comment_tag = soup.new_tag("li", **{"class": "comment"})
                new_comment_tag.string = comment
                comment_list.append(new_comment_tag)

        logs = soup.find("ul", id="logs-list")

        for result in self.result_array:
            logs.append(self._extract_html_from_log(soup, logs, result))

        the_file = open(self.detail_file, 'w')
        the_file.write(soup.prettify(encoding="utf8"))
        the_file.close()
