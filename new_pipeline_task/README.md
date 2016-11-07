# Create a pipeline task

The purpose of this script is to make it easy to create
a generic pipeline task, save time and not miss any
essential steps.

* To create the task, simply execute create_pipeline_task.py either from the
command line with casa, or within a casa session.

    Command line:
    ```
    casa --nogui --nologger -c $SCIPIPE_HEURISTICS/pipeline/infrastructure/create_pipeline_task/create_pipeline_task.py
    ```
    
    Within a casa session:
    ```python
    with open(os.environ["SCIPIPE_HEURISTICS"] + "/pipeline/infrastructure/create_pipeline_task/create_pipeline_task.py") as fd:
        exec(fd.read())
    ```

* To see if the task was added correctly, you can check manually or
run verify_new_pipeline_task.py like the previous task creation script.

    Command line:
    ```
    casa --nogui --nologger -c $SCIPIPE_HEURISTICS/pipeline/infrastructure/create_pipeline_task/verify_new_pipeline_task.py
    ```
    
    Within a casa session:
    ```python
    with open(os.environ["SCIPIPE_HEURISTICS"] + "/pipeline/infrastructure/create_pipeline_task/verify_new_pipeline_task.py") as fd:
        exec(fd.read())
    ```
