from app.app import App
from database.db import DataBase
from model.project import Project
from model.task import Task

app = App()

# app.add_list('some test task list')
# app.change_task_list_name('70ee354d-a325-405e-98fd-7c09ea53fd56', 'The To Do task list')
app.add_task('70ee354d-a325-405e-98fd-7c09ea53fd56', 'Do Labs')
task_lists = app.get_task_lists()
for task_list in task_lists:
    print(task_list.get('name') + "\t: " + task_list.get('unique_id'))

# task = Task(name="name")