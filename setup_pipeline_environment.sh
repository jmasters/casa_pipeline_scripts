# To use this script:
#
#    source ./setup_pipeline_environment.sh
#


# Set the version of casa that 'runsetup.sh' will use to
#  build pipeline tasks

CASAVERSION=current
#CASAVERSION=casa-prerelease-5.0.0-150

#export CASAPATH=/home/casa/packages/RHEL6/test/$CASAVERSION/
export CASAPATH=/home/casa/packages/RHEL6/prerelease/$CASAVERSION/

export PATH=$CASAPATH:$CASAPATH/bin:$PATH

# set locations of
#    1) pipeline source code (SCIPIPE_HEURISTICS)
#    2) pipeline data directories (SCIPIPE_ROOTDIR)

TOPDIR=/lustre/naasc/users/jmasters
export SCIPIPE_HEURISTICS=$TOPDIR/casapipeline
#export SCIPIPE_HEURISTICS=$TOPDIR/image_refactor_pipeline
export SCIPIPE_ROOTDIR=$TOPDIR/pipeline_test_data

showenv
