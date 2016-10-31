#! /bin/bash

testname=$1

echo CASAPATH=$CASAPATH
echo Making a unit test called: ${testname}
read -r -p "Are you sure? [y/N] " response
echo

make_test () {
    cp ~/lustre/unittests/tests/test_template.py ~/lustre/unittests/tests/test_${testname}.py
    echo Created ~/lustre/unittests/tests/test_${testname}.py

    cd $CASAPATH/lib/python2.7/tests/
    ln -s ~/lustre/unittests/tests/test_${testname}.py .
    echo Linked to $CASAPATH/lib/python2.7/tests/test_${testname}.py

    echo test_${testname}       jmasters@nrao.edu >> ~/lustre/unittests/tests/unittests_list.txt
    echo Added test_${testname} to ~/lustre/unittests/tests/unittests_list.txt
}

case $response in
    [yY][eE][sS]|[yY])
        make_test
        ;;
    *)
        exit
        ;;
esac
