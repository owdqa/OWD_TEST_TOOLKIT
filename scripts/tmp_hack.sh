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
        # Work around for IccHelper problem - sleep for 10s before any async js call.
        #
        if ( $0 ~ /self.marionette.execute_async_script/ ){
        	x = match($0, /[^ ]/) - 1
        	while (x > 0){
        		printf " "
        		x = x - 1
        	}
        	print "time.sleep(10)"
        }
        
        #
        # (Always leave this line in or you will get a blank file!)
        #
  		print $0
  		

		
	}
}' > /tmp/gaiatest.tmp

mv /tmp/gaiatest.tmp $GAIATEST