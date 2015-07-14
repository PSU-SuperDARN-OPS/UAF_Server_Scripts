
# Python tools:

Copy of ak_data ${HOME}/python

Tools useful for accessing dmap files and generting rti plots.

##Note:
This is not based on davitpy code. This python implementation pre-dates pydavit and was spun up specifically to provide UAF rti.plots. This should be replaced with pydavit constructs in the future.

##Note
When recovering this directory you will to repopulate the following binary files using the the appriopriate Makefiles and setup.py for python wrapper modules which wrap over the corresponding rst C library.

./lib64/dmap/pydmap.so
./lib64/rpos/pyrpos.so
./lib64/aacgm/pyaacgm.so
./lib32/dmap/pydmap.so
./lib32/rpos/pyrpos.so
./lib32/aacgm/pyaacgm.so

##Note:
.bash_profile in this repo is configured to setup everything necessary for build environment for the python wrapper modules using available rst install. 


#Bash script: python/scripts/generate_rti.sh

This script is run as a cronjob and generates rti plots for specified radars and channels based on fitacf data archive. 


