#!/bin/bash
#
# Comments out certain parts of "gaia_test.py" (for various reasons).
#

. $HOME/.OWD_TEST_TOOLKIT_LOCATION
export GAIATEST=$GAIATEST_PATH/gaia_test.py

[ ! -f $GAIATEST ] && exit

awk '
BEGIN{
	GAIATEST   = ENVIRON["GAIATEST"]
	IN_CLEANUP = 0
	IN_WIFI    = 0
	IN_SLEEP1  = 0
	IN_SLEEP2  = 0
	while ( getline < GAIATEST ){
		#
		# We have problems just now with the cleanUp() method of gaia_test.py sometimes, 
		# in the "wifi" section.
		#
	    if ( $0 ~ /def *cleanUp/ ){
            IN_CLEANUP = 1
        }
        if ( IN_CLEANUP == 1 && $0 ~ /if self.device.has_wifi/ ){
			IN_WIFI = 1
			$0 = "#" $0
		}
	    if ( IN_CLEANUP == 1 && IN_WIFI == 1 && $0 ~ /self.data_layer.enable_wifi/ ){
            $0 = "#" $0
        }
	    if ( IN_CLEANUP == 1 && IN_WIFI == 1 && $0 ~ /self.data_layer.forget_all_networks/ ){
            $0 = "#" $0
        }
		if ( IN_CLEANUP == 1 && IN_WIFI == 1 && $0 ~ /self.data_layer.disable_wifi/ ){
            $0 = "#" $0
            IN_WIFI = 0
            IN_CLEANUP = 0
		}
		
        #
        # We do not need the timezone to be reset to USA.
        #
        if ( IN_CLEANUP == 1 && $0 ~ /self.data_layer.set_setting/ && $0 ~ /timezone/ ){
            $0 = "#" $0
        }
        
        #
        # This is to work around a problem caused by the js returning an exception.
        #
        if ( $0 ~ /def start_b2g/ ){
            IN_SLEEP1 = 1
        }
        if ( $0 ~ /def launch/ ){
            IN_SLEEP2 = 1
        }
        
  		print $0
  		
  		if ( IN_SLEEP1 == 1 && $0 ~ / if self.is_android_build/ ){
  			print "            time.sleep(10)"
  			IN_SLEEP1 = 0
  		}
        if ( IN_SLEEP2 == 1 && $0 ~ /self.marionette.switch_to_frame/ ){
            print "        time.sleep(10)"
            IN_SLEEP2 = 0
        }
		
	}
}' > /tmp/gaiatest.tmp

mv /tmp/gaiatest.tmp $GAIATEST