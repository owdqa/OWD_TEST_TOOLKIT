import functools
import time

def retry(num_retries, delay=2, aux_func=None):
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
            for i in range(num_retries):
                try:
                    res = func_to_retry(*args, **kwargs)
                    return res
                except Exception:
                    if i < num_retries:
                        pass
                    else:
                        raise
                try:
                    func = args[0].__getattribute__(func_to_retry.__name__)
                    self = func.im_self
                    f = self.__getattribute__(aux_func)
                    f()
                except:
                    pass
                time.sleep(delay)
        return func_with_retries
    return retry_any_function