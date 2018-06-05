from comand_line_interface.handlers.printers import print_projects


ACTIONS = {
    'add': lambda app, args: add_project(app, args),
    'edit': lambda app, args: edit_project(app, args),
    'remove': lambda app, args: remove_project(app, args),
    'show': lambda app, args: show_project(app, args),
}


def add_project(app, args):
    app.add_project(args.name)


def edit_project(app, args):
    app.edit_project(args.name)


def remove_project(app, args):
    app.remove_project(args.project_id)


def show_project(app, args):
    if args.all:
        projects_info, current_project_id = app.get_projects_info()
        print_projects(projects_info, current_project_id)
    else:
        project = app.get_current_project()
        print("name: " + str(project.name))
        print("id: " + str(project.unique_id))
        if args.verbose:
            print("lists: " + str(project.lists))
