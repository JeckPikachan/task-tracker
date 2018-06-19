import copy
import time

from library_util.enum_json import serialize_enum


def transform_object(obj):
    new_dict = obj.__dict__ or obj
    return new_dict


def transform_project(project):
    return copy.deepcopy(project.__dict__)


def transform_upr_collection(uprs_collection):
    uprs_collection = copy.deepcopy(uprs_collection)
    uprs_collection.uprs = [transform_object(upr) for upr in
                            uprs_collection.uprs]
    return uprs_collection.__dict__


def transform_plan(plan):
    plan = copy.deepcopy(plan)
    plan.task_pattern = transform_object(plan.task_pattern)
    if plan.start_date is not None:
        plan.start_date = time.mktime(plan.start_date.timetuple())
    if plan.end_date is not None:
        plan.end_date = time.mktime(plan.end_date.timetuple())
    if plan.last_created is not None:
        plan.last_created = time.mktime(plan.last_created.timetuple())
    return transform_object(plan)


def transform_task(task):
    task = copy.deepcopy(task)
    task_dict = transform_object(task)
    task_dict['status'] = serialize_enum(task_dict['_status'])
    task_dict['priority'] = serialize_enum(task_dict['_priority'])
    task_dict['expiration_date'] = '{0:%Y-%m-%d %H:%M}' \
        .format(task_dict['_expiration_date']) if \
        task_dict['_expiration_date'] is not None else None
    del task_dict['_expiration_date']
    del task_dict['_status']
    del task_dict['_priority']
    task_dict['related_tasks_list'] = [transform_object(x) for
                                       x in task_dict['related_tasks_list']]

    return task_dict