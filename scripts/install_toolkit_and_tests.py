# This script will install the toolkit and the test cases, if required.
# It checks for the latest commit in the local and remote repositories, and, if
# they match, the clone / pull process is not done, thus saving a huge amount of time.

import os
import subprocess32
from subprocess32 import CalledProcessError


def main():
    scripts_dir = os.environ['PWD']
    tkdir = os.path.dirname(scripts_dir)
    branch = os.environ['BRANCH']
    integration = os.environ['INTEGRATION']
    logfile = os.environ['LOGFILE']
    tests_repo = 'https://github.com/owdqa/owd_test_cases.git'
    os.chdir(tkdir)

    try:
        subprocess32.check_output('{}/install.sh {} >> {} 2>&1'.format(tkdir, branch, logfile), shell=True)
    except CalledProcessError as e:
        print "================================================================="
        print "Error code: {}".format(e.returncode)
        print "Output: {}".format(e.output)

    # Check if test cases repository exists. If not, clone it
    os.chdir(tkdir + '/..')

    # cloned is set to True if the tests repository does not exist and has to be cloned
    cloned = False
    if not os.path.exists('owd_test_cases'):
        subprocess32.call('git clone {} >> {} 2>&1'.format(tests_repo, logfile), shell=True)
        cloned = True

    with open(logfile, 'a') as f:
        os.chdir('owd_test_cases')
        f.write('Switching to branch {}{} of owd_test_cases'.format(integration, branch))
        subprocess32.call('git checkout {}{} >> {} 2>&1'.format(integration, branch, logfile), shell=True)

        if not cloned:
            # If the test repository existed, compare last commit in local and remote repositories
            local_commit = subprocess32.check_output('git log -n 1 --format="%H"', shell=True).strip()
            print "Last local commit:  [{}]".format(local_commit)
            cmd = 'git ls-remote --heads {} {}{}'.format(tests_repo, integration, branch)
            remote_commit = subprocess32.check_output(cmd, shell=True).split()[0]
            print "Last remote commit: [{}]".format(remote_commit)

            # If commits do not match, pull the latest changes
            if local_commit != remote_commit:
                print "Updating repository"
                f.write('\n\nUpdating owd_test_cases repository...')
                f.write('\n=======================================\n')
                subprocess32.check_output('git pull', shell=True)
            else:
                print "Tests repository already updated, no need to pull"
                f.write("\nTests repository already updated, no need to pull")

    os.chdir(scripts_dir)

if __name__ == '__main__':
    main()
