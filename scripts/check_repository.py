# This script receives a Git repository URL and the directory where it has to be installed,
# should it doesn't exist or it is not fully updated to the last version

from argparse import ArgumentParser
import os
import subprocess32


def main():
    parser = ArgumentParser()
    parser.add_argument("-n", "--name", dest="name", action="store", help="Repository name")
    parser.add_argument("-u", "--url", dest="url", action="store", help="Repository URL")
    parser.add_argument("-b", "--branch", dest="branch", action="store", help="Branch")
    parser.add_argument("-c", "--command", dest="command", action="store", help="Command(s) to execute after update")
    options = parser.parse_args()
    check(options.name, options.url, options.branch, options.command)


def check(name, url, branch, cmd=None):
    logfile = os.environ['LOGFILE']

    # cloned is set to True if the repository does not exist and has to be cloned
    cloned = False
    if not os.path.exists(name):
        subprocess32.call('git clone {} >> {} 2>&1'.format(url, logfile), shell=True)
        cloned = True

    with open(logfile, 'a') as f:
        os.chdir(name)
        f.write('Switching to branch {} of {}'.format(branch, name))
        subprocess32.call('git checkout {} >> {} 2>&1'.format(branch, logfile), shell=True)

        if not cloned:
            # If the test repository existed, compare last commit in local and remote repositories
            local_commit = subprocess32.check_output('git log -n 1 --format="%H"', shell=True).strip()
            print "Last local commit:  [{}]".format(local_commit)
            cmd = 'git ls-remote --heads {} {}'.format(name, branch)
            remote_commit = subprocess32.check_output(cmd, shell=True).split()[0]
            print "Last remote commit: [{}]".format(remote_commit)

            # If commits do not match, pull the latest changes
            if local_commit != remote_commit:
                print "Updating repository"
                f.write('\n\nUpdating {} repository....'.format(name))
                f.write('\n=======================================\n')
                subprocess32.check_output('git pull', shell=True)
                if cmd is not None:
                    print "Executing after update commands:\n{}\n".format(cmd)
                    f.write('Executing after update commands:\n{}\n".format(cmd)')
                    subprocess32.check_output(cmd, shell=True)
            else:
                print "Repository {} already updated, no need to pull".format(name)
                f.write("Repository {} already updated, no need to pull\n".format(name))

    os.chdir('..')

if __name__ == '__main__':
    main()
