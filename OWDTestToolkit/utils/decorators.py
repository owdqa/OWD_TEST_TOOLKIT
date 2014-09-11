import functools
import sys
import importlib
import time


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
            for i in range(num_retries):
                try:
                    retry_self.UTILS.reporting.debug(
                        ">>>>>> Trying function[{}] for the #{} time".format(func_to_retry, i + 1))
                    res = func_to_retry(*args, **kwargs)
                    return res
                except Exception, e:
                    retry_self.UTILS.reporting.debug(">>>>>> The function to retry failed: {}".format(e))
                    if i < num_retries:
                        pass
                    else:
                        raise

                if aux_func_name is not None:
                    try:
                        module_context, function_context = context
                        try:
                            sys.modules[module_context]
                        except KeyError:
                            retry_self.UTILS.reporting.debug(">>>>>> Importing module at runtime")
                            try:
                                importlib.import_module(module_context)
                            except Exception, e:
                                retry_self.UTILS.reporting.debug(">>>>>> Importing failed: {}".format(e))

                        try:
                            # We get the context of the aux_func
                            class_context = getattr(sys.modules[module_context], function_context)
                            f = getattr(class_context, aux_func_name)
                        except Exception, e:
                            retry_self.UTILS.reporting.debug(
                                ">>>>>> Failed getting aux_func context: {}".format(e))

                        try:
                            # Get a self reference of the aux_func (it may not be defined in the same
                            # class as func_to_retry)
                            retry_self.UTILS.reporting.debug(">>>>>> Executing aux_func.....")

                            aux_func_self = retry_self if class_context.__name__ == retry_self.__class__.__name__ else class_context(
                                retry_self.parent)
                            aux_func_self.__getattribute__(aux_func_name)()
                        except Exception, e:
                            retry_self.UTILS.reporting.debug(">>>>>> Failed: {}".format(e))
                            break
                    except:
                        pass
                time.sleep(delay)
        return func_with_retries
    return retry_any_function
