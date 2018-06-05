from comand_line_interface.handlers.printers import print_plan, print_plans


ACTIONS = {
    'add': lambda app, args: add_plan(app, args),
    'remove': lambda app, args: remove_plan(app, args),
    'show': lambda app, args: show_plan(app, args),
}


def add_plan(app, args):
    app.add_plan(name=args.name,
                 task_list_id=args.list_id,
                 delta=args.delta,
                 status=args.status,
                 priority=args.priority,
                 description=args.description,
                 start_date=args.start_date,
                 end_date=args.end_date)


def remove_plan(app, args):
    app.remove_plan(args.plan_id)


def show_plan(app, args):
    if args.id is not None:
        plan = app.get_plan_by_id(args.id)
        print_plan(plan)
    else:
        plans = app.get_plans()
        print_plans(plans)
