from app.app import App

app = App()

# app.add_list('some test task list')
app.change_task_list_name('70ee354d-a325-405e-98fd-7c09ea53fd56', 'The To Do task list')
app.add_task('ea4a6c5a-488b-478e-a0c9-1ea58b3c77f3', 'Do Labs')
task_lists = app.get_task_lists()
for task_list in task_lists:
    print(task_list.name + "\t: " + task_list.unique_id)

tasks = app.get_tasks('70ee354d-a325-405e-98fd-7c09ea53fd56')
tasks = [{'unique_id': task.unique_id, 'name': task.name} for task in tasks]
print(tasks)
# task = Task(name="name")
