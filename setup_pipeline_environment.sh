# To use this script:
#
#    source ./setup_pipeline_environment.sh
#


# Set the version of casa that 'runsetup.sh' will use to
#  build pipeline tasks

#CASAVERSION=casa-test-5.0.49

CASAVERSION=current
export CASAPATH=/home/casa/packages/RHEL6/test/$CASAVERSION/
export PATH=$CASAPATH:$CASAPATH/bin:$PATH

# set locations of
#    1) pipeline source code (SCIPIPE_HEURISTICS)
#    2) pipeline data directories (SCIPIPE_ROOTDIR)

TOPDIR=/lustre/naasc/users/jmasters
export SCIPIPE_HEURISTICS=$TOPDIR/casapipeline
export SCIPIPE_ROOTDIR=$TOPDIR/pipeline_test_data
