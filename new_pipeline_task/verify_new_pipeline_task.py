from pipeline.infrastructure.new_pipeline_task import new_pipeline_task

if __name__ == '__main__':

    new_task = new_pipeline_task.NewTask()
    area, task_name = new_task.parse_command_line(sys.argv)
    new_task.verify(area, task_name)
