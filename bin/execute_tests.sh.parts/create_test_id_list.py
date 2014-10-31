import os
import re
import sys


def find_test_ids(user_stories):
    """
    Locate the tests corresponding to the given user stories.
    
    If a user story exists as a directory, locate the tests under it.
    Return the list of test ids.
    """
    result = []
    for user_story in user_stories:
        tests_dir = os.getenv("owd_test_cases_DIR", False) + '/tests'
        d = "{}/{}".format(tests_dir, user_story)
        if os.path.isdir(d):
            for f in os.listdir(d):
                res = re.search('^(test_)(\w+)(\.py)$', f)
                if res:
                    result.append(res.group(2))
        else:
            f = "{}/test_{}.py".format(tests_dir, user_story)
            if os.path.isfile(f):
                result.append(user_story)
    return " ".join(result)

def main():
    print find_test_ids(sys.argv[1:])

if __name__ == "__main__":
    main()
    