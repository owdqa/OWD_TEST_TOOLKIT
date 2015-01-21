import functools
import sys
import importlib
import time
from datetime import datetime
import inspect


def retry(num_retries, delay=2, context=None, aux_func_name=None):
    """Decorator factory for retries.

    This decorator factory will return a decorator that implements
    a retries policy, up to the number given as a parameter, given
    that the target function raises an exception. Otherwise, the
    function return value is returned.
    The time elapsed between consecutive retries is given in seconds
    by the 'delay' parameter.
    """
    def retry_any_function(func_to_retry):
        @functools.wraps(func_to_retry)
        def func_with_retries(*args, **kwargs):
            # Get the self reference to the function to be retried
            retry_self = args[0].__getattribute__(func_to_retry.__name__).im_self
            try:
                utils = retry_self.UTILS
            except:
                utils = retry_self.parent

            for i in range(num_retries):
                try:
                    utils.reporting.debug(
                        ">>>>>> Trying function[{}] for the #{} time".format(func_to_retry.__name__, i + 1))
                    res = func_to_retry(*args, **kwargs)
                    return res
                except Exception, e:
                    utils.reporting.debug(">>>>>> The function to retry failed: {}".format(e))
                    if i < num_retries:
                        pass
                    else:
                        utils.reporting.logResult("info", "############# LANZANDO EXCEPTION. Reise, Reise Seemann Reiseeee")
                        raise

                if aux_func_name is not None:
                    try:
                        module_context, function_context = context
                        try:
                            sys.modules[module_context]
                        except KeyError:
                            utils.reporting.debug(">>>>>> Importing module at runtime")
                            try:
                                importlib.import_module(module_context)
                            except Exception, e:
                                utils.reporting.debug(">>>>>> Importing failed: {}".format(e))

                        try:
                            # We get the context of the aux_func
                            class_context = getattr(sys.modules[module_context], function_context)
                        except Exception, e:
                            utils.reporting.debug(
                                ">>>>>> Failed getting aux_func context: {}".format(e))

                        try:
                            # Get a self reference of the aux_func (it may not be defined in the same
                            # class as func_to_retry)
                            utils.reporting.debug(">>>>>> Executing aux_func.....")

                            aux_func_self = retry_self if class_context.__name__ == retry_self.__class__.__name__ else class_context(
                                retry_self.parent)
                            aux_func_self.__getattribute__(aux_func_name)()
                        except Exception, e:
                            utils.reporting.debug(">>>>>> Failed: {}".format(e))
                            break
                    except:
                        pass
                time.sleep(delay)
        return func_with_retries
    return retry_any_function


def timestamped_log(func):
    """Decorator to add a timestamp at the beginning of a log line.

    Assumes there is a message attribute, which is the log to be shown, and
    that will be manipulated to prefix with the timestamp.
    IMPORTANT: This decorator is ONLY for binding functions, where the first
    argument is always self.
    """
    @functools.wraps(func)
    def log_func(*args, **kwargs):
        msg = args[1]
        d = datetime.now().strftime('%Y-%m-%d %H:%M:%S,') + \
            '{:03d}'.format(datetime.now().microsecond / 1000)
        (frame, filename, line_number, function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[2]
        caller = '{}::{}:{}'.format(filename[filename.rfind('/') + 1:], function_name, line_number)
        msg = u'{} - {} - {} - {}'.format(d, caller, func.__name__.upper(), msg)
        func(args[0], msg)
    return log_func
