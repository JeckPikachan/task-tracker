import unittest

from app.model.project import Project
from app.model.projectcontainer import ProjectContainer
from app.model.task import Task, TaskRelation
from app.model.tasklist import TaskList


class TestProjectContainer(unittest.TestCase):
    def setUp(self):
        project = Project()
        self.container = ProjectContainer(project=project)

    def tearDown(self):
        self.container = None

    def test_project(self):
        self.assertIsInstance(self.container.project, Project)

    def test_lists(self):
        self.assertListEqual(self.container.lists, [])

    def test_tasks(self):
        self.assertListEqual(self.container.tasks, [])

    def test_add_list(self):
        task_list = TaskList(name="Name")
        self.container.add_list(task_list)
        self.assertIn(task_list, self.container.lists)
        self.assertIn(task_list.unique_id,
                      self.container.project.lists)

    def test_add_task(self):
        task_list = TaskList(name="Name")
        self.container.add_list(task_list)
        task = Task(name="Task name")
        self.container.add_task(task_list.unique_id, task)
        self.assertIn(task, self.container.tasks)
        self.assertIn(task.unique_id, task_list.tasks_list)

    def test_remove_task(self):
        task_list = TaskList(name="Name")
        self.container.add_list(task_list)
        task = Task(name="Task name")
        self.container.add_task(task_list.unique_id, task)
        self.container.remove_task(task.unique_id)
        self.assertNotIn(task.unique_id, task_list.tasks_list)
        self.assertNotIn(task, self.container.tasks)

    def test_remove_list(self):
        task_list = TaskList(name="Name")
        self.container.add_list(task_list)
        task = Task(name="Task name")
        self.container.add_task(task_list.unique_id, task)
        self.container.remove_list(task_list.unique_id)
        self.assertNotIn(task_list, self.container.lists)
        self.assertNotIn(task, self.container.tasks)
        self.assertNotIn(task_list.unique_id,
                         self.container.project.lists)

    def test_add_relation(self):
        task_list = TaskList(name="Name")
        self.container.add_list(task_list)
        task = Task(name="Task name")
        task2 = Task(name="Task2 name")
        self.container.add_task(task_list.unique_id, task)
        self.container.add_task(task_list.unique_id, task2)
        task_relation = self.container.add_relation(
            task.unique_id,
            task2.unique_id,
            "Some description")
        self.assertIn(task_relation, task.related_tasks_list)
        self.assertIsInstance(task_relation, TaskRelation)
        with self.assertRaises(NameError):
            self.container.add_relation("asd", "fgh")

    def test_get_tasks(self):
        task_list = TaskList(name="Name")
        task_list2 = TaskList(name="Name2")
        self.container.add_list(task_list)
        self.container.add_list(task_list2)
        task = Task(name="Task name")
        task2 = Task(name="Task2 name")
        self.container.add_task(task_list.unique_id, task)
        self.container.add_task(task_list2.unique_id, task2)
        tasks = self.container.get_tasks(task_list.unique_id)
        for task in tasks:
            self.assertIsInstance(task, Task)
            self.assertIn(task.unique_id, task_list.tasks_list)

    def test_get_task_by_id(self):
        task_list = TaskList(name="Name")
        self.container.add_list(task_list)
        task = Task(name="Task name")
        self.container.add_task(task_list.unique_id, task)
        got_task = self.container.get_task_by_id(task.unique_id)
        self.assertEqual(got_task, task)