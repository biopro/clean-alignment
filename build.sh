#!/usr/bin/env bash

# check if the bin/ dir exists

if [ ! -d bin ]; then

	'bin/ dir not found!';
	exit

fi

# enter the bin dir

cd bin/

# prepare EvalMSA

chmod +x evalmsa-linux

if [ -d EvalMSA ]; then

	rm -r EvalMSA

fi

./evalmsa-linux

# prepare trimAl

cd trimAl/source
make
cd ../../

# finish

echo DONE!

