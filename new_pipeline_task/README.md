# Create a pipeline task

The purpose of this module is to bootstrap the creation of a task, thus 
saving time and making it easier to not miss essential steps.

* To create a task, simply execute new_pipeline_task.py from the command
 line or use the new_pipeline_task module within a CASA session.  For 
 example, if I want to create task "foo" in the package "hif", I could 
 do one of the following.

    Command line:
    ```
    casa --nogui --nologger -c $SCIPIPE_HEURISTICS/pipeline/infrastructure/new_pipeline_task/new_pipeline_task.py --package hif --task foo
    ```
    
    Within CASA:
    ```python
     from pipeline.infrastructure.new_pipeline_task import new_pipeline_task
       newtask = new_pipeline_task.NewTask()
       newtask.create('hif', 'foo')
    ```
