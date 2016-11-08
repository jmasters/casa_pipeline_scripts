import pipeline

# ----------------------------------------------
#   set data, package and task name for testing
# ----------------------------------------------
vis = '/lustre/naasc/users/jmasters/pipeline_test_data/VLAT003/rawdata/13A-537.sb24066356.eb24324502.56514.05971091435'
area = 'hsd'
task_name = 'googoo'

# ---------------------------
#  prepare to check the task
# ---------------------------
h_init()
h_save()
hifv_importdata(vis=[vis], session=['session_1'], overwrite=False)
h_save()

context = pipeline.Pipeline(context='last').context

# ---------------------------
#  execute the task
# ---------------------------
inputs = eval('pipeline.{area}.tasks.{task}.{captask}.Inputs(context)'.format(area=area, task=task_name, captask=task_name.capitalize()))
task = eval('pipeline.{area}.tasks.{task}.{captask}(inputs)'.format(area=area, task=task_name, captask=task_name.capitalize()))
result = task.execute(dry_run=False)
result.accept(context)
context.save()

# --------------------------------
#   run as a registered CASA task
# --------------------------------
try:
    eval('{area}_{task}()'.format(area=area, task=task_name))
    h_save()
except NameError as ee:
    print('ERROR: {msg}'.format(msg=ee.message))
    print('\tTry using runsetup to register the new task with CASA first.')
