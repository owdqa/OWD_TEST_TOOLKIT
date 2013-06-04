#!/bin/bash
#
# Pushes the current project to git (from the folder you're in when you execute this script).
#


CURRDIR=$(pwd)
THISDIR=$(dirname $0)
PARAMFILE=parameters

#
# Is this the toolkit?
#
x=$(basename $CURRDIR)
if [ "$x" = "OWD_TEST_TOOLKIT" ]
then
	# Refresh the READMEs ...
	echo "Rebuilding the READMEs for the toolkit apis ..."
	$THISDIR/rebuild_toolkit_READMEs.sh
fi

#
# If this contains some tests, then rebuild the test list in the readme.
#
if [ -d "./tests" ]
then
    x=$(grep testcoverage README.md)
    if [ "$x" ]
    then
       $THISDIR/refresh_README.sh
    fi
fi

#
# Move the parameters file out of the way.
#
if [ -f ./tests/$PARAMFILE ]
then
    mv ./tests/$PARAMFILE /tmp
fi
   

echo "
NOTE: THIS WILL COMPLETELY OVERWRITE THE GIT REPO. WITH THE CONTENTS OF THIS FOLDER!

Press ENTER to continue, or CTRL+C to quit."
read ans

f_getName(){
    if [ ! "$GIT_NAME" ]
    then
	    printf "Your name     : "
	    read GIT_NAME
    fi
}
f_getEmail(){
    if [ ! "$GIT_EMAIL" ]
    then
        printf "Your email    : "
        read GIT_EMAIL
    fi
}

if [ -f "$HOME/.gitparams" ]
then
	. $HOME/.gitparams
fi

if [ ! "$GIT_NAME" ] || [ ! "$GIT_EMAIL" ]
then
    echo ""
    echo "(To stop being prompted for this, create a $HOME/.gitparams file"
    echo "and add \"export GIT_NAME=<your name>\" and \"export GIT_EMAIL=<your email>\".)" 
    echo ""
fi

f_getName
f_getEmail

printf "Commit massage: "
read MSG

#git remote add origin https://github.com/roydude/OWD_TEST_TOOLKIT.git
git config --global user.name "$GIT_NAME"
git config --global user.email $GIT_EMAIL
git rm -r --cached .
git add -A
git commit -m "$MSG"
git push origin master

#
# Put the parameters file back.
#
if [ -f /tmp/$PARAMFILE ]
then
	mv /tmp/$PARAMFILE ./tests
fi
