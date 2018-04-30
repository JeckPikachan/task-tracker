from database.db import DataBase
from model.project import Project

project = Project(name="Some test project")

print(project.__dict__)

db = DataBase()
error = db.load()

if error is not None:
    print("ERROR!")
    print(error)
    exit(1)

error = db.add(project)


if error is not None:
    print("ERROR!")
    print(error)
    exit(2)

error = db.load(project.unique_id)

if error is not None:
    print("ERROR!")
    print(error)
    exit(3)

print(db.project.__dict__)
