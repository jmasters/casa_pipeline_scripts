import os

casapath = '/users/jmasters/lustre/casa-unittests'
os.environ['SCIPIPE_ROOTDIR'] = '/lustre/naasc/users/jmasters/pipeline_test_data'
os.environ['SCIPIPE_HEURISTICS'] = '/lustre/naasc/users/jmasters/casapipeline'

os.environ['CASAPATH'] = casapath
os.environ['PATH'] = '{casapath}:{casapath}/bin:{path}'.format(casapath=casapath, path=os.environ['PATH'])

print('CASAPATH = {cp}'.format(cp=casapath))


def run_all_tests():
    os.system('time $CASAPATH/bin/casa --nogui --nologger -c '
              '$CASAPATH/lib/python2.7/regressions/admin/runUnitTest.py '
              '--datadir ~/lustre/unittests/data/ --file ~/lustre/unittests/tests/unittests_list.txt')

if __name__ == '__main__':
    run_all_tests()
