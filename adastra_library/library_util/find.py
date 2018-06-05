def find_one(collection, unique_id):
    return next((x for x in collection if x.unique_id == unique_id), None)


def find_one_in_dicts(collection, unique_id):
    return next((x for x in collection if
                 x['unique_id'] == unique_id), None)
