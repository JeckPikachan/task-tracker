import inspect
import logging


LIBRARY_LOGGER_NAME = 'adastra_library'


def log_func(logger_name):
    logger = logging.getLogger(logger_name)

    def _log_func(func):
        def _log(self, *args, **kwargs):
            try:
                logger.info("Called function: {}".format(func.__name__))
                logger.debug("\n\tSelf type: {0}, \n\tArgs: {1}, \n\tKwargs: {2}".format(type(self), args, kwargs))
                result = func(self, *args, **kwargs)
                logger.debug("{0} returned: {1}".format(func.__name__, result))
                return result
            except Exception as e:
                logger.error(e)
                raise e
        return _log
    return _log_func


def init_logging(level, filename, log_format, log_datefmt):
    if level is not None:
        logging.basicConfig(
            filename=filename,
            level=logging.getLevelName(level),
            format=log_format,
            datefmt=log_datefmt)
