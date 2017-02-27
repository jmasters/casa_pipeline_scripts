#! /bin/bash

cd ~/lustre/unittests/

rm -r ./casa-latest*

cp `ls -t /home/casa/distro/linux/test/el6/*.gz | head -1` ./casa-latest.tar.gz
mkdir -p ./casa-latest
tar xzf casa-latest.tar.gz -C ./casa-latest

CASAPATH=`pwd`/casa-latest/`ls casa-latest`
cd $CASAPATH/lib/python2.7/tests/

for d in `ls ~/lustre/unittests/tests/*.py`
do
ln -s ${d} .
done
