import os
import sys

if os.path.expandvars("$SCIPIPE_HEURISTICS") not in sys.path:
    sys.path.insert(0, os.path.expandvars("$SCIPIPE_HEURISTICS"))

import pipeline

with open(os.environ["SCIPIPE_HEURISTICS"] + "/pipeline/h/cli/h.py") as fd:
    exec (fd.read())

with open(os.environ["SCIPIPE_HEURISTICS"] + "/pipeline/hif/cli/hif.py") as fd:
    exec (fd.read())

with open(os.environ["SCIPIPE_HEURISTICS"] + "/pipeline/hifa/cli/hifa.py") as fd:
    exec (fd.read())

with open(os.environ["SCIPIPE_HEURISTICS"] + "/pipeline/hifv/cli/hifv.py") as fd:
    exec (fd.read())

vis = '/lustre/naasc/users/jmasters/pipeline_test_data/VLAT003/rawdata/13A-537.sb24066356.eb24324502.56514.05971091435'

h_init()
h_save()
hifv_importdata(vis=[vis], session=['session_1'], overwrite=False)
h_save()

context = pipeline.Pipeline(context='last').context

print('checking pipeline.hif.tasks.foobar.Foobar(inputs).execute()')
inputs = pipeline.hif.tasks.foobar.Foobar.Inputs(context)
task = pipeline.hif.tasks.foobar.Foobar(inputs)
result = task.execute(dry_run=False)
result.accept(context)
context.save()

print('checking hif_foobar()')
hif_foobar()
h_save()
