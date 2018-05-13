import inspect
import logging


def log_func(func):
    def _log(self, *args, **kwargs):
        try:
            logging.info("Called function: {}".format(func.__name__))
            logging.debug("\n\tSelf type: {0}, \n\tArgs: {1}, \n\tKwargs: {2}".format(type(self), args, kwargs))
            result = func(self, *args, **kwargs)
            logging.debug("{0} returned: {1}".format(func.__name__, result))
            return result
        except Exception as e:
            logging.error(e)
            raise e
    return _log
