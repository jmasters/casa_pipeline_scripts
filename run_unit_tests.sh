#! /bin/bash

echo CASAPATH=$CASAPATH
read -r -p "Are you sure? [y/N] " response
echo

run_all_tests () {
    time $CASAPATH/bin/casa --nogui --nologger -c $CASAPATH/lib/python2.7/regressions/admin/runUnitTest.py \
    --datadir ~/lustre/unittests/data/ --file ~/lustre/unittests/tests/unittests_list.txt
}

case $response in
    [yY][eE][sS]|[yY])
        run_all_tests
        ;;
    *)
        exit
        ;;
esac
