#! /bin/bash

# The following steps assume we are on a machine with access to
#   /home/casa/packages/RHEL6/test/
#   builds of casa.
#   'beefy' is one of those machines.
#   cv lustre nodes like 'cvpost004' can also see it.

TOPLEVEL_DIR=/lustre/naasc/users/jmasters
DATA_DIR=$TOPLEVEL_DIR/pipeline_test_data/VLAT003
cd $TOPLEVEL_DIR

# checkout the pipeline
svn co https://svn.cv.nrao.edu/svn/casa/branches/project/pipeline casapipeline 

# setup the environment
#  This sets the following environment variables:
#     CASAVERSION
#     CASAPATH
#     PATH
#     LD_LIBRARY_PATH
#     LD_PRELOAD
#     SCIPIPE_HEURISTICS
#     SCIPIPE_ROOTDIR
source $TOPLEVEL_DIR/setup_pipeline_environment.sh
cd $TOPLEVEL_DIR/casapipeline
./runsetup

#  create input, output and working directories if they don't exist
cd $TOPLEVEL_DIR
mkdir -p $DATA_DIR/products
mkdir -p $DATA_DIR/working
mkdir -p $DATA_DIR/rawdata

# get data to put in the rawdata directory
cd $DATA_DIR/rawdata
rsync -a /lustre/naasc/users/bkent/evlapipeline/pipetest/VLAT003/rawdata/13A-537.sb24066356.eb24324502.56514.05971091435 .

# get a pipeline processing request (PPR) that determines which pipeline tasks to run
cd $DATA_DIR/working
rsync -a /lustre/naasc/users/bkent/evlapipeline/pipetest/VLAT003/working/PPRnew_VLAT003.xml PPR_VLAT003.xml 

# run the vla pipeline using the PPR as input
casa --nologger --nogui -c $SCIPIPE_HEURISTICS/pipeline/runvlapipeline.py PPR_VLAT003.xml

#casa

## execute a pipeline processing request (PPR)
#import pipeline.infrastructure.executevlappr as eppr
#eppr.executeppr('PPR_VLAT003.xml', importonly=False)

# view output through the Log Message Viewer and
#  the HTML Web Log at
#  /export/data_1/jmasters/pipeline_test_data/VLAT003/working/pipeline-20161004T123130/html/index.html

